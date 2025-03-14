import numpy as np
import gym
from gym.spaces import Discrete, MultiDiscrete
from typing import Dict, List, Union

from ray.rllib.models.modelv2 import ModelV2
from ray.rllib.models.torch.misc import SlimFC
from ray.rllib.models.torch.torch_modelv2 import TorchModelV2
from ray.rllib.policy.rnn_sequencing import add_time_dimension
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.policy.view_requirement import ViewRequirement
from ray.rllib.utils.annotations import override, DeveloperAPI
from ray.rllib.utils.framework import try_import_torch
from ray.rllib.utils.torch_utils import one_hot
from ray.rllib.utils.typing import ModelConfigDict, TensorType

torch, nn = try_import_torch()


@DeveloperAPI
class RecurrentNetwork(TorchModelV2):
    """Helper class to simplify implementing RNN models with TorchModelV2.

    Instead of implementing forward(), you can implement forward_rnn() which
    takes batches with the time dimension added already.

    Here is an example implementation for a subclass
    ``MyRNNClass(RecurrentNetwork, nn.Module)``::

        def __init__(self, obs_space, num_outputs):
            nn.Module.__init__(self)
            super().__init__(obs_space, action_space, num_outputs,
                             model_config, name)
            self.obs_size = _get_size(obs_space)
            self.rnn_hidden_dim = model_config["lstm_cell_size"]
            self.fc1 = nn.Linear(self.obs_size, self.rnn_hidden_dim)
            self.rnn = nn.GRUCell(self.rnn_hidden_dim, self.rnn_hidden_dim)
            self.fc2 = nn.Linear(self.rnn_hidden_dim, num_outputs)

            self.value_branch = nn.Linear(self.rnn_hidden_dim, 1)
            self._cur_value = None

        @override(ModelV2)
        def get_initial_state(self):
            # Place hidden states on same device as model.
            h = [self.fc1.weight.new(
                1, self.rnn_hidden_dim).zero_().squeeze(0)]
            return h

        @override(ModelV2)
        def value_function(self):
            assert self._cur_value is not None, "must call forward() first"
            return self._cur_value

        @override(RecurrentNetwork)
        def forward_rnn(self, input_dict, state, seq_lens):
            x = nn.functional.relu(self.fc1(input_dict["obs_flat"].float()))
            h_in = state[0].reshape(-1, self.rnn_hidden_dim)
            h = self.rnn(x, h_in)
            q = self.fc2(h)
            self._cur_value = self.value_branch(h).squeeze(1)
            return q, [h]
    """

    @override(ModelV2)
    def forward(self, input_dict: Dict[str, TensorType],
                state: List[TensorType],
                seq_lens: TensorType) -> (TensorType, List[TensorType]):
        """Adds time dimension to batch before sending inputs to forward_rnn().

        You should implement forward_rnn() in your subclass."""
        flat_inputs = input_dict["obs_flat"].float()
        if isinstance(seq_lens, np.ndarray):
            seq_lens = torch.Tensor(seq_lens).int()
        max_seq_len = flat_inputs.shape[0] // seq_lens.shape[0]
        self.time_major = self.model_config.get("_time_major", False)
        inputs = add_time_dimension(
            flat_inputs,
            max_seq_len=max_seq_len,
            framework="torch",
            time_major=self.time_major,
        )
        output, new_state = self.forward_rnn(inputs, state, seq_lens)
        output = torch.reshape(output, [-1, self.num_outputs])
        return output, new_state

    def forward_rnn(self, inputs: TensorType, state: List[TensorType],
                    seq_lens: TensorType) -> (TensorType, List[TensorType]):
        """Call the model with the given input tensors and state.

        Args:
            inputs (dict): Observation tensor with shape [B, T, obs_size].
            state (list): List of state tensors, each with shape [B, size].
            seq_lens (Tensor): 1D tensor holding input sequence lengths.
                Note: len(seq_lens) == B.

        Returns:
            (outputs, new_state): The model output tensor of shape
                [B, T, num_outputs] and the list of new state tensors each with
                shape [B, size].

        Examples:
            def forward_rnn(self, inputs, state, seq_lens):
                model_out, h, c = self.rnn_model([inputs, seq_lens] + state)
                return model_out, [h, c]
        """
        raise NotImplementedError("You must implement this for an RNN model")


class LSTMWrapper(RecurrentNetwork, nn.Module):
    """An LSTM wrapper serving as an interface for ModelV2s that set use_lstm.
    """

    def __init__(self, obs_space: gym.spaces.Space,
                 action_space: gym.spaces.Space, num_outputs: int,
                 model_config: ModelConfigDict, name: str):

        nn.Module.__init__(self)
        super(LSTMWrapper, self).__init__(obs_space, action_space, None,
                                          model_config, name)

        # At this point, self.num_outputs is the number of nodes coming
        # from the wrapped (underlying) model. In other words, self.num_outputs
        # is the input size for the LSTM layer.
        # If None, set it to the observation space.
        if self.num_outputs is None:
            self.num_outputs = int(np.product(self.obs_space.shape))

        self.cell_size = model_config["lstm_cell_size"]
        self.time_major = model_config.get("_time_major", False)
        self.use_prev_action = model_config["lstm_use_prev_action"]
        self.use_prev_reward = model_config["lstm_use_prev_reward"]

        if isinstance(action_space, Discrete):
            self.action_dim = action_space.n
        elif isinstance(action_space, MultiDiscrete):
            self.action_dim = np.sum(action_space.nvec)
        elif action_space.shape is not None:
            self.action_dim = int(np.product(action_space.shape))
        else:
            self.action_dim = int(len(action_space))

        # Add prev-action/reward nodes to input to LSTM.
        if self.use_prev_action:
            self.num_outputs += self.action_dim
        if self.use_prev_reward:
            self.num_outputs += 1

        # Define actual LSTM layer (with num_outputs being the nodes coming
        # from the wrapped (underlying) layer).
        self.lstm = nn.LSTM(
            self.num_outputs, self.cell_size, batch_first=not self.time_major)

        # Set self.num_outputs to the number of output nodes desired by the
        # caller of this constructor.
        self.num_outputs = num_outputs

        # Postprocess LSTM output with another hidden layer and compute values.
        self._logits_branch = SlimFC(
            in_size=self.cell_size,
            out_size=self.num_outputs,
            activation_fn=None,
            initializer=torch.nn.init.xavier_uniform_)
        self._value_branch = SlimFC(
            in_size=self.cell_size,
            out_size=1,
            activation_fn=None,
            initializer=torch.nn.init.xavier_uniform_)

        # __sphinx_doc_begin__
        # Add prev-a/r to this model's view, if required.
        if model_config["lstm_use_prev_action"]:
            self.view_requirements[SampleBatch.PREV_ACTIONS] = \
                ViewRequirement(SampleBatch.ACTIONS, space=self.action_space,
                                shift=-1)
        if model_config["lstm_use_prev_reward"]:
            self.view_requirements[SampleBatch.PREV_REWARDS] = \
                ViewRequirement(SampleBatch.REWARDS, shift=-1)
        # __sphinx_doc_end__

    @override(RecurrentNetwork)
    def forward(self, input_dict: Dict[str, TensorType],
                state: List[TensorType],
                seq_lens: TensorType) -> (TensorType, List[TensorType]):
        assert seq_lens is not None
        # Push obs through "unwrapped" net's `forward()` first.
        wrapped_out, _ = self._wrapped_forward(input_dict, [], None)

        # Concat. prev-action/reward if required.
        prev_a_r = []
        if self.model_config["lstm_use_prev_action"]:
            if isinstance(self.action_space, (Discrete, MultiDiscrete)):
                prev_a = one_hot(input_dict[SampleBatch.PREV_ACTIONS].float(),
                                 self.action_space)
            else:
                prev_a = input_dict[SampleBatch.PREV_ACTIONS].float()
            prev_a_r.append(torch.reshape(prev_a, [-1, self.action_dim]))
        if self.model_config["lstm_use_prev_reward"]:
            prev_a_r.append(
                torch.reshape(input_dict[SampleBatch.PREV_REWARDS].float(),
                              [-1, 1]))

        if prev_a_r:
            wrapped_out = torch.cat([wrapped_out] + prev_a_r, dim=1)

        # Then through our LSTM.
        input_dict["obs_flat"] = wrapped_out
        return super().forward(input_dict, state, seq_lens)

    @override(RecurrentNetwork)
    def forward_rnn(self, inputs: TensorType, state: List[TensorType],
                    seq_lens: TensorType) -> (TensorType, List[TensorType]):
        # Don't show paddings to RNN(?)
        # TODO: (sven) For now, only allow, iff time_major=True to not break
        #  anything retrospectively (time_major not supported previously).
        # max_seq_len = inputs.shape[0]
        # time_major = self.model_config["_time_major"]
        # if time_major and max_seq_len > 1:
        #     inputs = torch.nn.utils.rnn.pack_padded_sequence(
        #         inputs, seq_lens,
        #         batch_first=not time_major, enforce_sorted=False)
        self._features, [h, c] = self.lstm(
            inputs,
            [torch.unsqueeze(state[0], 0),
             torch.unsqueeze(state[1], 0)])
        # Re-apply paddings.
        # if time_major and max_seq_len > 1:
        #     self._features, _ = torch.nn.utils.rnn.pad_packed_sequence(
        #         self._features,
        #         batch_first=not time_major)
        model_out = self._logits_branch(self._features)
        return model_out, [torch.squeeze(h, 0), torch.squeeze(c, 0)]

    @override(ModelV2)
    def get_initial_state(self) -> Union[List[np.ndarray], List[TensorType]]:
        # Place hidden states on same device as model.
        linear = next(self._logits_branch._model.children())
        h = [
            linear.weight.new(1, self.cell_size).zero_().squeeze(0),
            linear.weight.new(1, self.cell_size).zero_().squeeze(0)
        ]
        return h

    @override(ModelV2)
    def value_function(self) -> TensorType:
        assert self._features is not None, "must call forward() first"
        return torch.reshape(self._value_branch(self._features), [-1])

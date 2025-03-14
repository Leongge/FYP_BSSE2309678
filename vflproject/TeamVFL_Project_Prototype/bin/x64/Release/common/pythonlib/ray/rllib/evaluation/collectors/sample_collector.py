from abc import abstractmethod, ABCMeta
import logging
from typing import Dict, List, Optional, TYPE_CHECKING, Union

from ray.rllib.evaluation.episode import Episode
from ray.rllib.policy.policy_map import PolicyMap
from ray.rllib.policy.sample_batch import MultiAgentBatch, SampleBatch
from ray.rllib.utils.typing import AgentID, EnvID, EpisodeID, PolicyID, \
    TensorType

if TYPE_CHECKING:
    from ray.rllib.agents.callbacks import DefaultCallbacks

logger = logging.getLogger(__name__)


# yapf: disable
# __sphinx_doc_begin__
class SampleCollector(metaclass=ABCMeta):
    """Collects samples for all policies and agents from a multi-agent env.

    This API is controlled by RolloutWorker objects to store all data
    generated by Environments and Policies/Models during rollout and
    postprocessing. It's purposes are to a) make data collection and
    SampleBatch/input_dict generation from this data faster, b) to unify
    the way we collect samples from environments and model (outputs), thereby
    allowing for possible user customizations, c) to allow for more complex
    inputs fed into different policies (e.g. multi-agent case with inter-agent
    communication channel).
    """

    def __init__(self,
                 policy_map: PolicyMap,
                 clip_rewards: Union[bool, float],
                 callbacks: "DefaultCallbacks",
                 multiple_episodes_in_batch: bool = True,
                 rollout_fragment_length: int = 200,
                 count_steps_by: str = "env_steps"):
        """Initializes a SampleCollector instance.

        Args:
            policy_map (PolicyMap): Maps policy ids to policy instances.
            clip_rewards (Union[bool, float]): Whether to clip rewards before
                postprocessing (at +/-1.0) or the actual value to +/- clip.
            callbacks (DefaultCallbacks): RLlib callbacks.
            multiple_episodes_in_batch (bool): Whether it's allowed to pack
                multiple episodes into the same built batch.
            rollout_fragment_length (int): The

        """

        self.policy_map = policy_map
        self.clip_rewards = clip_rewards
        self.callbacks = callbacks
        self.multiple_episodes_in_batch = multiple_episodes_in_batch
        self.rollout_fragment_length = rollout_fragment_length
        self.count_steps_by = count_steps_by

    @abstractmethod
    def add_init_obs(self, episode: Episode, agent_id: AgentID,
                     policy_id: PolicyID, t: int,
                     init_obs: TensorType) -> None:
        """Adds an initial obs (after reset) to this collector.

        Since the very first observation in an environment is collected w/o
        additional data (w/o actions, w/o reward) after env.reset() is called,
        this method initializes a new trajectory for a given agent.
        `add_init_obs()` has to be called first for each agent/episode-ID
        combination. After this, only `add_action_reward_next_obs()` must be
        called for that same agent/episode-pair.

        Args:
            episode (Episode): The Episode, for which we
                are adding an Agent's initial observation.
            agent_id (AgentID): Unique id for the agent we are adding
                values for.
            env_id (EnvID): The environment index (in a vectorized setup).
            policy_id (PolicyID): Unique id for policy controlling the agent.
            t (int): The time step (episode length - 1). The initial obs has
                ts=-1(!), then an action/reward/next-obs at t=0, etc..
            init_obs (TensorType): Initial observation (after env.reset()).

        Examples:
            >>> obs = env.reset()
            >>> collector.add_init_obs(my_episode, 0, "pol0", -1, obs)
            >>> obs, r, done, info = env.step(action)
            >>> collector.add_action_reward_next_obs(12345, 0, "pol0", False, {
            ...     "action": action, "obs": obs, "reward": r, "done": done
            ... })
        """
        raise NotImplementedError

    @abstractmethod
    def add_action_reward_next_obs(self, episode_id: EpisodeID,
                                   agent_id: AgentID, env_id: EnvID,
                                   policy_id: PolicyID, agent_done: bool,
                                   values: Dict[str, TensorType]) -> None:
        """Add the given dictionary (row) of values to this collector.

        The incoming data (`values`) must include action, reward, done, and
        next_obs information and may include any other information.
        For the initial observation (after Env.reset()) of the given agent/
        episode-ID combination, `add_initial_obs()` must be called instead.

        Args:
            episode_id (EpisodeID): Unique id for the episode we are adding
                values for.
            agent_id (AgentID): Unique id for the agent we are adding
                values for.
            env_id (EnvID): The environment index (in a vectorized setup).
            policy_id (PolicyID): Unique id for policy controlling the agent.
            agent_done (bool): Whether the given agent is done with its
                trajectory (the multi-agent episode may still be ongoing).
            values (Dict[str, TensorType]): Row of values to add for this
                agent. This row must contain the keys SampleBatch.ACTION,
                REWARD, NEW_OBS, and DONE.

        Examples:
            >>> obs = env.reset()
            >>> collector.add_init_obs(12345, 0, "pol0", obs)
            >>> obs, r, done, info = env.step(action)
            >>> collector.add_action_reward_next_obs(12345, 0, "pol0", False, {
            ...     "action": action, "obs": obs, "reward": r, "done": done
            ... })
        """
        raise NotImplementedError

    @abstractmethod
    def episode_step(self, episode: Episode) -> None:
        """Increases the episode step counter (across all agents) by one.

        Args:
            episode (Episode): Episode we are stepping through.
                Useful for handling counting b/c it is called once across
                all agents that are inside this episode.
        """
        raise NotImplementedError

    @abstractmethod
    def total_env_steps(self) -> int:
        """Returns total number of env-steps taken so far.

        Thereby, a step in an N-agent multi-agent environment counts as only 1
        for this metric. The returned count contains everything that has not
        been built yet (and returned as MultiAgentBatches by the
        `try_build_truncated_episode_multi_agent_batch` or
        `postprocess_episode(build=True)` methods). After such build, this
        counter is reset to 0.

        Returns:
            int: The number of env-steps taken in total in the environment(s)
                so far.
        """
        raise NotImplementedError

    @abstractmethod
    def total_agent_steps(self) -> int:
        """Returns total number of (individual) agent-steps taken so far.

        Thereby, a step in an N-agent multi-agent environment counts as N.
        If less than N agents have stepped (because some agents were not
        required to send actions), the count will be increased by less than N.
        The returned count contains everything that has not been built yet
        (and returned as MultiAgentBatches by the
        `try_build_truncated_episode_multi_agent_batch` or
        `postprocess_episode(build=True)` methods). After such build, this
        counter is reset to 0.

        Returns:
            int: The number of (individual) agent-steps taken in total in the
                environment(s) so far.
        """
        raise NotImplementedError

    @abstractmethod
    def get_inference_input_dict(self, policy_id: PolicyID) -> \
            Dict[str, TensorType]:
        """Returns an input_dict for an (inference) forward pass from our data.

        The input_dict can then be used for action computations inside a
        Policy via `Policy.compute_actions_from_input_dict()`.

        Args:
            policy_id (PolicyID): The Policy ID to get the input dict for.

        Returns:
            Dict[str, TensorType]: The input_dict to be passed into the ModelV2
                for inference/training.

        Examples:
            >>> obs, r, done, info = env.step(action)
            >>> collector.add_action_reward_next_obs(12345, 0, "pol0", {
            ...     "action": action, "obs": obs, "reward": r, "done": done
            ... })
            >>> input_dict = collector.get_inference_input_dict(policy.model)
            >>> action = policy.compute_actions_from_input_dict(input_dict)
            >>> # repeat
        """
        raise NotImplementedError

    @abstractmethod
    def postprocess_episode(self,
                            episode: Episode,
                            is_done: bool = False,
                            check_dones: bool = False,
                            build: bool = False) -> Optional[MultiAgentBatch]:
        """Postprocesses all agents' trajectories in a given episode.

        Generates (single-trajectory) SampleBatches for all Policies/Agents and
        calls Policy.postprocess_trajectory on each of these. Postprocessing
        may happens in-place, meaning any changes to the viewed data columns
        are directly reflected inside this collector's buffers.
        Also makes sure that additional (newly created) data columns are
        correctly added to the buffers.

        Args:
            episode (Episode): The Episode object for which
                to post-process data.
            is_done (bool): Whether the given episode is actually terminated
                (all agents are done OR we hit a hard horizon). If True, the
                episode will no longer be used/continued and we may need to
                recycle/erase it internally. If a soft-horizon is hit, the
                episode will continue to be used and `is_done` should be set
                to False here.
            check_dones (bool): Whether we need to check that all agents'
                trajectories have dones=True at the end.
            build (bool): Whether to build a MultiAgentBatch from the given
                episode (and only that episode!) and return that
                MultiAgentBatch. Used for batch_mode=`complete_episodes`.

        Returns:
            Optional[MultiAgentBatch]: If `build` is True, the
                SampleBatch or MultiAgentBatch built from `episode` (either
                just from that episde or from the `_PolicyCollectorGroup`
                in the `episode.batch_builder` property).
        """
        raise NotImplementedError

    @abstractmethod
    def try_build_truncated_episode_multi_agent_batch(self) -> \
            List[Union[MultiAgentBatch, SampleBatch]]:
        """Tries to build an MA-batch, if `rollout_fragment_length` is reached.

        Any unprocessed data will be first postprocessed with a policy
        postprocessor.
        This is usually called to collect samples for policy training.
        If not enough data has been collected yet (`rollout_fragment_length`),
        returns an empty list.

        Returns:
            List[Union[MultiAgentBatch, SampleBatch]]: Returns a (possibly
                empty) list of MultiAgentBatches (containing the accumulated
                SampleBatches for each policy or a simple SampleBatch if only
                one policy). The list will be empty if
                `self.rollout_fragment_length` has not been reached yet.
        """
        raise NotImplementedError
# __sphinx_doc_end__

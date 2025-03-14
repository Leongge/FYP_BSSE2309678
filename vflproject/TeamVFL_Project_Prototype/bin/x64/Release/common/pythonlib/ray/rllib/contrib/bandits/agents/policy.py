import logging
import time

from gym import spaces
from ray.rllib.agents.trainer import with_common_config
from ray.rllib.contrib.bandits.models.linear_regression import \
    DiscreteLinearModelThompsonSampling, \
    DiscreteLinearModelUCB, DiscreteLinearModel, \
    ParametricLinearModelThompsonSampling, ParametricLinearModelUCB
from ray.rllib.models.catalog import ModelCatalog
from ray.rllib.models.modelv2 import restore_original_dimensions
from ray.rllib.policy.policy_template import build_policy_class
from ray.rllib.policy.sample_batch import SampleBatch
from ray.rllib.policy.torch_policy import TorchPolicy
from ray.rllib.utils.annotations import override
from ray.rllib.utils.metrics.learner_info import LEARNER_STATS_KEY
from ray.util.debug import log_once

logger = logging.getLogger(__name__)

TS_PATH = "ray.rllib.contrib.bandits.exploration.ThompsonSampling"
UCB_PATH = "ray.rllib.contrib.bandits.exploration.UCB"

DEFAULT_CONFIG = with_common_config({
    # No remote workers by default.
    "num_workers": 0,
    "framework": "torch",  # Only PyTorch supported so far.

    # Do online learning one step at a time.
    "rollout_fragment_length": 1,
    "train_batch_size": 1,

    # Bandits cant afford to do one timestep per iteration as it is extremely
    # slow because of metrics collection overhead. This setting means that the
    # agent will be trained for 100 times in one iteration of Rllib
    "timesteps_per_iteration": 100
})


class BanditPolicyOverrides:
    @override(TorchPolicy)
    def learn_on_batch(self, postprocessed_batch):
        train_batch = self._lazy_tensor_dict(postprocessed_batch)
        unflattened_obs = restore_original_dimensions(
            train_batch[SampleBatch.CUR_OBS], self.observation_space,
            self.framework)

        info = {}

        start = time.time()
        self.model.partial_fit(unflattened_obs,
                               train_batch[SampleBatch.REWARDS],
                               train_batch[SampleBatch.ACTIONS])

        infos = postprocessed_batch["infos"]
        if "regret" in infos[0]:
            regret = sum(
                row["infos"]["regret"] for row in postprocessed_batch.rows())
            self.regrets.append(regret)
            info["cumulative_regret"] = sum(self.regrets)
        else:
            if log_once("no_regrets"):
                logger.warning("The env did not report `regret` values in "
                               "its `info` return, ignoring.")
        info["update_latency"] = time.time() - start
        return {LEARNER_STATS_KEY: info}


def make_model_and_action_dist(policy, obs_space, action_space, config):
    dist_class, logit_dim = ModelCatalog.get_action_dist(
        action_space, config["model"], framework="torch")
    model_cls = DiscreteLinearModel

    if hasattr(obs_space, "original_space"):
        original_space = obs_space.original_space
    else:
        original_space = obs_space

    exploration_config = config.get("exploration_config")
    # Model is dependent on exploration strategy because of its implicitness

    # TODO: Have a separate model catalogue for bandits
    if exploration_config:
        if exploration_config["type"] == TS_PATH:
            if isinstance(original_space, spaces.Dict):
                assert "item" in original_space.spaces, \
                    "Cannot find 'item' key in observation space"
                model_cls = ParametricLinearModelThompsonSampling
            else:
                model_cls = DiscreteLinearModelThompsonSampling
        elif exploration_config["type"] == UCB_PATH:
            if isinstance(original_space, spaces.Dict):
                assert "item" in original_space.spaces, \
                    "Cannot find 'item' key in observation space"
                model_cls = ParametricLinearModelUCB
            else:
                model_cls = DiscreteLinearModelUCB

    model = model_cls(
        obs_space,
        action_space,
        logit_dim,
        config["model"],
        name="LinearModel")
    return model, dist_class


def init_cum_regret(policy, *args):
    policy.regrets = []


BanditPolicy = build_policy_class(
    name="BanditPolicy",
    framework="torch",
    get_default_config=lambda: DEFAULT_CONFIG,
    loss_fn=None,
    after_init=init_cum_regret,
    make_model_and_action_dist=make_model_and_action_dist,
    optimizer_fn=lambda policy, config: None,  # Pass a dummy optimizer
    mixins=[BanditPolicyOverrides])

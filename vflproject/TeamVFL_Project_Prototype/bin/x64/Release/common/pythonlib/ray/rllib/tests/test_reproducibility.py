import gym
import numpy as np
import unittest

import ray
from ray.rllib.agents.dqn import DQNTrainer
from ray.rllib.utils.test_utils import framework_iterator
from ray.tune.registry import register_env


class TestReproducibility(unittest.TestCase):
    def test_reproducing_trajectory(self):
        class PickLargest(gym.Env):
            def __init__(self):
                self.observation_space = gym.spaces.Box(
                    low=float("-inf"), high=float("inf"), shape=(4, ))
                self.action_space = gym.spaces.Discrete(4)

            def reset(self, **kwargs):
                self.obs = np.random.randn(4)
                return self.obs

            def step(self, action):
                reward = self.obs[action]
                return self.obs, reward, True, {}

        def env_creator(env_config):
            return PickLargest()

        for fw in framework_iterator(frameworks=("tf", "torch")):
            trajs = list()
            for trial in range(3):
                ray.init()
                register_env("PickLargest", env_creator)
                config = {
                    "seed": 666 if trial in [0, 1] else 999,
                    "min_iter_time_s": 0,
                    "timesteps_per_iteration": 100,
                    "framework": fw,
                }
                agent = DQNTrainer(config=config, env="PickLargest")

                trajectory = list()
                for _ in range(8):
                    r = agent.train()
                    trajectory.append(r["episode_reward_max"])
                    trajectory.append(r["episode_reward_min"])
                trajs.append(trajectory)

                ray.shutdown()

            # trial0 and trial1 use same seed and thus
            # expect identical trajectories.
            all_same = True
            for v0, v1 in zip(trajs[0], trajs[1]):
                if v0 != v1:
                    all_same = False
            self.assertTrue(all_same)

            # trial1 and trial2 use different seeds and thus
            # most rewards tend to be different.
            diff_cnt = 0
            for v1, v2 in zip(trajs[1], trajs[2]):
                if v1 != v2:
                    diff_cnt += 1
            self.assertTrue(diff_cnt > 8)


if __name__ == "__main__":
    import pytest
    import sys
    sys.exit(pytest.main(["-v", __file__]))

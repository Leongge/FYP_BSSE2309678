import gymnasium
import numpy as np


class SingleVecEnv:
    def __init__(self, gym_env_fns, *args):
        assert len(gym_env_fns) == 1
        self.gym_env = gym_env_fns[0]()
        self.render_mode = self.gym_env.render_mode
        self.observation_space = self.gym_env.observation_space
        self.action_space = self.gym_env.action_space
        self.num_envs = 1
        self.metadata = self.gym_env.metadata

    def reset(self, seed=None, options=None):
        # TODO: should this include info
        return np.expand_dims(self.gym_env.reset(seed=seed, options=options), 0)

    def step_async(self, actions):
        self._saved_actions = actions

    def step_wait(self):
        return self.step(self._saved_actions)

    def render(self):
        return self.gym_env.render()

    def close(self):
        self.gym_env.close()

    def step(self, actions):
        observations, reward, term, trunc, info = self.gym_env.step(actions[0])
        if term or trunc:
            observations = self.gym_env.reset()
        observations = np.expand_dims(observations, 0)
        rewards = np.array([reward], dtype=np.float32)
        terms = np.array([term], dtype=np.uint8)
        truncs = np.array([trunc], dtype=np.uint8)
        infos = [info]
        return observations, rewards, terms, truncs, infos

    def env_is_wrapped(self, wrapper_class):
        env_tmp = self.gym_env
        while isinstance(env_tmp, gymnasium.Wrapper):
            if isinstance(env_tmp, wrapper_class):
                return [True]
            env_tmp = env_tmp.env
        return [False]

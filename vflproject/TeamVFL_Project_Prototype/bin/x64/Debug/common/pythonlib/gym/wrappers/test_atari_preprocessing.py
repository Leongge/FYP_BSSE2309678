import numpy as np
import gym
from gym.wrappers import AtariPreprocessing
import pytest

pytest.importorskip('atari_py')


@pytest.fixture(scope='module')
def env_fn():
    return lambda: gym.make('PongNoFrameskip-v4')


def test_atari_preprocessing_grayscale(env_fn):
    import cv2
    env1 = env_fn()
    env2 = AtariPreprocessing(env_fn(), screen_size=84, grayscale_obs=True, frame_skip=1, noop_max=0)
    env3 = AtariPreprocessing(env_fn(), screen_size=84, grayscale_obs=False, frame_skip=1, noop_max=0)
    env1.reset()
    # take these steps to imitate actions of FireReset logic
    env1.step(1)
    obs1 = env1.step(2)[0]
    obs2 = env2.reset()
    obs3 = env3.reset()
    assert obs1.shape == (210, 160, 3)
    assert obs2.shape == (84, 84)
    assert obs3.shape == (84, 84, 3)
    np.testing.assert_allclose(obs3, cv2.resize(obs1, (84, 84), interpolation=cv2.INTER_AREA))
    obs3_gray = cv2.cvtColor(obs3, cv2.COLOR_RGB2GRAY)
    # the edges of the numbers do not render quite the same in the grayscale, so we ignore them
    np.testing.assert_allclose(obs2[10:], obs3_gray[10:])

    env1.close()
    env2.close()
    env3.close()


def test_atari_preprocessing_scale(env_fn):
    # arbitrarily chosen number for stepping into env. and ensuring all observations are in the required range
    max_test_steps = 10

    for grayscale in [True, False]:
        for scaled in [True, False]:
            env = AtariPreprocessing(env_fn(), screen_size=84, grayscale_obs=grayscale, scale_obs=scaled,
                                     frame_skip=1, noop_max=0)
            obs = env.reset().flatten()
            done, step_i = False, 0
            max_obs = 1 if scaled else 255
            assert (0 <= obs).all() and (obs <= max_obs).all(), 'Obs. must be in range [0,{}]'.format(max_obs)
            while not done or step_i <= max_test_steps:
                obs, _, done, _ = env.step(env.action_space.sample())
                obs = obs.flatten()
                assert (0 <= obs).all() and (obs <= max_obs).all(), 'Obs. must be in range [0,{}]'.format(max_obs)
                step_i += 1

            env.close()
"""
Example of running an RLlib Trainer against a locally running Unity3D editor
instance (available as Unity3DEnv inside RLlib).
For a distributed cloud setup example with Unity,
see `examples/serving/unity3d_[server|client].py`

To run this script against a local Unity3D engine:
1) Install Unity3D and `pip install mlagents`.

2) Open the Unity3D Editor and load an example scene from the following
   ml-agents pip package location:
   `.../ml-agents/Project/Assets/ML-Agents/Examples/`
   This script supports the `3DBall`, `3DBallHard`, `SoccerStrikersVsGoalie`,
    `Tennis`, and `Walker` examples.
   Specify the game you chose on your command line via e.g. `--env 3DBall`.
   Feel free to add more supported examples here.

3) Then run this script (you will have to press Play in your Unity editor
   at some point to start the game and the learning process):
$ python unity3d_env_local.py --env 3DBall --stop-reward [..]
  [--framework=torch]?
"""

import argparse
import os

import ray
from ray import tune
from ray.rllib.env.wrappers.unity3d_env import Unity3DEnv
from ray.rllib.utils.test_utils import check_learning_achieved

parser = argparse.ArgumentParser()
parser.add_argument(
    "--env",
    type=str,
    default="3DBall",
    choices=[
        "3DBall",
        "3DBallHard",
        "GridFoodCollector",
        "Pyramids",
        "SoccerStrikersVsGoalie",
        "Sorter",
        "Tennis",
        "VisualHallway",
        "Walker",
    ],
    help="The name of the Env to run in the Unity3D editor: `3DBall(Hard)?|"
    "Pyramids|GridFoodCollector|SoccerStrikersVsGoalie|Sorter|Tennis|"
    "VisualHallway|Walker` (feel free to add more and PR!)")
parser.add_argument(
    "--file-name",
    type=str,
    default=None,
    help="The Unity3d binary (compiled) game, e.g. "
    "'/home/ubuntu/soccer_strikers_vs_goalie_linux.x86_64'. Use `None` for "
    "a currently running Unity3D editor.")
parser.add_argument(
    "--from-checkpoint",
    type=str,
    default=None,
    help="Full path to a checkpoint file for restoring a previously saved "
    "Trainer state.")
parser.add_argument("--num-workers", type=int, default=0)
parser.add_argument(
    "--as-test",
    action="store_true",
    help="Whether this script should be run as a test: --stop-reward must "
    "be achieved within --stop-timesteps AND --stop-iters.")
parser.add_argument(
    "--stop-iters",
    type=int,
    default=9999,
    help="Number of iterations to train.")
parser.add_argument(
    "--stop-timesteps",
    type=int,
    default=10000000,
    help="Number of timesteps to train.")
parser.add_argument(
    "--stop-reward",
    type=float,
    default=9999.0,
    help="Reward at which we stop training.")
parser.add_argument(
    "--horizon",
    type=int,
    default=3000,
    help="The max. number of `step()`s for any episode (per agent) before "
    "it'll be reset again automatically.")
parser.add_argument(
    "--framework",
    choices=["tf", "tf2", "tfe", "torch"],
    default="tf",
    help="The DL framework specifier.")

if __name__ == "__main__":
    ray.init()

    args = parser.parse_args()

    tune.register_env(
        "unity3d",
        lambda c: Unity3DEnv(
            file_name=c["file_name"],
            no_graphics=(args.env != "VisualHallway" and
                         c["file_name"] is not None),
            episode_horizon=c["episode_horizon"],
        ))

    # Get policies (different agent types; "behaviors" in MLAgents) and
    # the mappings from individual agents to Policies.
    policies, policy_mapping_fn = \
        Unity3DEnv.get_policy_configs_for_game(args.env)

    config = {
        "env": "unity3d",
        "env_config": {
            "file_name": args.file_name,
            "episode_horizon": args.horizon,
        },
        # For running in editor, force to use just one Worker (we only have
        # one Unity running)!
        "num_workers": args.num_workers if args.file_name else 0,
        # Other settings.
        "lr": 0.0003,
        "lambda": 0.95,
        "gamma": 0.99,
        "sgd_minibatch_size": 256,
        "train_batch_size": 4000,
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        "num_sgd_iter": 20,
        "rollout_fragment_length": 200,
        "clip_param": 0.2,
        # Multi-agent setup for the particular env.
        "multiagent": {
            "policies": policies,
            "policy_mapping_fn": policy_mapping_fn,
        },
        "model": {
            "fcnet_hiddens": [512, 512],
        },
        "framework": "tf" if args.env != "Pyramids" else "torch",
        "no_done_at_end": True,
    }
    # Switch on Curiosity based exploration for Pyramids env
    # (not solvable otherwise).
    if args.env == "Pyramids":
        config["exploration_config"] = {
            "type": "Curiosity",
            "eta": 0.1,
            "lr": 0.001,
            # No actual feature net: map directly from observations to feature
            # vector (linearly).
            "feature_net_config": {
                "fcnet_hiddens": [],
                "fcnet_activation": "relu",
            },
            "sub_exploration": {
                "type": "StochasticSampling",
            },
            "forward_net_activation": "relu",
            "inverse_net_activation": "relu",
        }
    elif args.env == "GridFoodCollector":
        config["model"] = {
            "conv_filters": [[16, [4, 4], 2], [32, [4, 4], 2],
                             [256, [10, 10], 1]],
        }
    elif args.env == "Sorter":
        config["model"]["use_attention"] = True

    stop = {
        "training_iteration": args.stop_iters,
        "timesteps_total": args.stop_timesteps,
        "episode_reward_mean": args.stop_reward,
    }

    # Run the experiment.
    results = tune.run(
        "PPO",
        config=config,
        stop=stop,
        verbose=1,
        checkpoint_freq=5,
        checkpoint_at_end=True,
        restore=args.from_checkpoint)

    # And check the results.
    if args.as_test:
        check_learning_achieved(results, args.stop_reward)

    ray.shutdown()

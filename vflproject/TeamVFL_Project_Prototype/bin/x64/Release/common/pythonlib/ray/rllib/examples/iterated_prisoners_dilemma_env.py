##########
# Contribution by the Center on Long-Term Risk:
# https://github.com/longtermrisk/marltoolbox
##########
import argparse
import os

import ray
from ray import tune
from ray.rllib.agents.pg import PGTrainer
from ray.rllib.examples.env.matrix_sequential_social_dilemma import \
    IteratedPrisonersDilemma

parser = argparse.ArgumentParser()
parser.add_argument(
    "--framework",
    choices=["tf", "tf2", "tfe", "torch"],
    default="tf",
    help="The DL framework specifier.")
parser.add_argument("--stop-iters", type=int, default=200)


def main(debug, stop_iters=200, tf=False):
    train_n_replicates = 1 if debug else 1
    seeds = list(range(train_n_replicates))

    ray.init(num_cpus=os.cpu_count(), num_gpus=0, local_mode=debug)

    rllib_config, stop_config = get_rllib_config(seeds, debug, stop_iters, tf)
    tune_analysis = tune.run(
        PGTrainer,
        config=rllib_config,
        stop=stop_config,
        checkpoint_freq=0,
        checkpoint_at_end=True,
        name="PG_IPD")
    ray.shutdown()
    return tune_analysis


def get_rllib_config(seeds, debug=False, stop_iters=200, tf=False):
    stop_config = {
        "training_iteration": 2 if debug else stop_iters,
    }

    env_config = {
        "players_ids": ["player_row", "player_col"],
        "max_steps": 20,
        "get_additional_info": True,
    }

    rllib_config = {
        "env": IteratedPrisonersDilemma,
        "env_config": env_config,
        "multiagent": {
            "policies": {
                env_config["players_ids"][0]: (
                    None, IteratedPrisonersDilemma.OBSERVATION_SPACE,
                    IteratedPrisonersDilemma.ACTION_SPACE, {}),
                env_config["players_ids"][1]: (
                    None, IteratedPrisonersDilemma.OBSERVATION_SPACE,
                    IteratedPrisonersDilemma.ACTION_SPACE, {}),
            },
            "policy_mapping_fn": lambda agent_id, **kwargs: agent_id,
        },
        "seed": tune.grid_search(seeds),
        "num_gpus": int(os.environ.get("RLLIB_NUM_GPUS", "0")),
        "framework": args.framework,
    }

    return rllib_config, stop_config


if __name__ == "__main__":
    debug_mode = True
    args = parser.parse_args()
    main(debug_mode, args.stop_iters, args.tf)

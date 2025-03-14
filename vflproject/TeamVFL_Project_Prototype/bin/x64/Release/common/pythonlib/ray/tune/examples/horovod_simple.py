import torch
import numpy as np

import ray
from ray import tune
from ray.tune.integration.horovod import DistributedTrainableCreator
import time


def sq(x):
    m2 = 1.
    m1 = -20.
    m0 = 50.
    return m2 * x * x + m1 * x + m0


def qu(x):
    m3 = 10.
    m2 = 5.
    m1 = -20.
    m0 = -5.
    return m3 * x * x * x + m2 * x * x + m1 * x + m0


class Net(torch.nn.Module):
    def __init__(self, mode="sq"):
        super(Net, self).__init__()

        if mode == "square":
            self.mode = 0
            self.param = torch.nn.Parameter(torch.FloatTensor([1., -1.]))
        else:
            self.mode = 1
            self.param = torch.nn.Parameter(torch.FloatTensor([1., -1., 1.]))

    def forward(self, x):
        if ~self.mode:
            return x * x + self.param[0] * x + self.param[1]
        else:
            return_val = 10 * x * x * x
            return_val += self.param[0] * x * x
            return_val += self.param[1] * x + self.param[2]
            return return_val


def train(config):
    import torch
    import horovod.torch as hvd
    hvd.init()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    mode = config["mode"]
    net = Net(mode).to(device)
    optimizer = torch.optim.SGD(
        net.parameters(),
        lr=config["lr"],
    )
    optimizer = hvd.DistributedOptimizer(optimizer)

    num_steps = 5
    print(hvd.size())
    np.random.seed(1 + hvd.rank())
    torch.manual_seed(1234)
    # To ensure consistent initialization across slots,
    hvd.broadcast_parameters(net.state_dict(), root_rank=0)
    hvd.broadcast_optimizer_state(optimizer, root_rank=0)

    start = time.time()
    x_max = config["x_max"]
    for step in range(1, num_steps + 1):
        features = torch.Tensor(np.random.rand(1) * 2 * x_max -
                                x_max).to(device)
        if mode == "square":
            labels = sq(features)
        else:
            labels = qu(features)
        optimizer.zero_grad()
        outputs = net(features)
        loss = torch.nn.MSELoss()(outputs, labels)
        loss.backward()

        optimizer.step()
        time.sleep(0.1)
        tune.report(loss=loss.item())
    total = time.time() - start
    print(f"Took {total:0.3f} s. Avg: {total / num_steps:0.3f} s.")


def tune_horovod(hosts_per_trial,
                 slots_per_host,
                 num_samples,
                 use_gpu,
                 mode="square",
                 x_max=1.):
    horovod_trainable = DistributedTrainableCreator(
        train,
        use_gpu=use_gpu,
        num_hosts=hosts_per_trial,
        num_slots=slots_per_host,
        replicate_pem=False)
    analysis = tune.run(
        horovod_trainable,
        metric="loss",
        mode="min",
        config={
            "lr": tune.uniform(0.1, 1),
            "mode": mode,
            "x_max": x_max
        },
        num_samples=num_samples,
        fail_fast=True)
    print("Best hyperparameters found were: ", analysis.best_config)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", type=str, default="square", choices=["square", "cubic"])
    parser.add_argument(
        "--learning_rate", type=float, default=0.1, dest="learning_rate")
    parser.add_argument("--x_max", type=float, default=1., dest="x_max")
    parser.add_argument("--gpu", action="store_true")
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help=("Finish quickly for testing."))
    parser.add_argument("--hosts-per-trial", type=int, default=1)
    parser.add_argument("--slots-per-host", type=int, default=2)
    parser.add_argument(
        "--server-address",
        type=str,
        default=None,
        required=False,
        help="The address of server to connect to if using "
        "Ray Client.")
    args, _ = parser.parse_known_args()

    if args.smoke_test:
        ray.init(num_cpus=2)
    elif args.server_address:
        ray.init(f"ray://{args.server_address}")

    # import ray
    # ray.init(address="auto")  # assumes ray is started with ray up

    tune_horovod(
        hosts_per_trial=args.hosts_per_trial,
        slots_per_host=args.slots_per_host,
        num_samples=2 if args.smoke_test else 10,
        use_gpu=args.gpu,
        mode=args.mode,
        x_max=args.x_max)

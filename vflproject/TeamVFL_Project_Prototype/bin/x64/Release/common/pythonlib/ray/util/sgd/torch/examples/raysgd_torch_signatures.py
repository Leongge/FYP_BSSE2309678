# flake8: noqa
"""This file holds code for the TorchTrainer creator signatures.

It ignores yapf because yapf doesn't allow comments right after code blocks,
but we put comments right after code blocks to prevent large white spaces
in the documentation.
"""
# yapf: disable

# __torch_operator_start__
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from ray.util.sgd.torch import TrainingOperator
from ray.util.sgd.torch.examples.train_example import LinearDataset

class MyTrainingOperator(TrainingOperator):
    def setup(self, config):
        # Setup all components needed for training here. This could include
        # data, models, optimizers, loss & schedulers.

        # Setup data loaders.
        train_dataset, val_dataset = LinearDataset(2, 5), LinearDataset(2,
                                                                        5)
        train_loader = DataLoader(train_dataset,
                                  batch_size=config["batch_size"])
        val_loader = DataLoader(val_dataset,
                                batch_size=config["batch_size"])

        # Setup model.
        model = nn.Linear(1, 1)

        # Setup optimizer.
        optimizer = torch.optim.SGD(model.parameters(), lr=config.get("lr", 1e-4))

        # Setup loss.
        criterion = torch.nn.BCELoss()

        # Setup scheduler.
        scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.9)

        # Register all of these components with Ray SGD.
        # This allows Ray SGD to do framework level setup like Cuda, DDP,
        # Distributed Sampling, FP16.
        # We also assign the return values of self.register to instance
        # attributes so we can access it in our custom training/validation
        # methods.
        self.model, self.optimizer, self.criterion, self.scheduler = \
            self.register(models=model, optimizers=optimizer,
                          criterion=criterion,
                          schedulers=scheduler)
        self.register_data(train_loader=train_loader, validation_loader=val_loader)
# __torch_operator_end__

# __torch_ray_start__
import ray

ray.init()
# or ray.init(address="auto") to connect to a running cluster.
# __torch_ray_end__

# __torch_trainer_start__
from ray.util.sgd import TorchTrainer

trainer = TorchTrainer(
    training_operator_cls=MyTrainingOperator,
    scheduler_step_freq="epoch",  # if scheduler is used
    config={"lr": 0.001, "batch_size": 64})

# __torch_trainer_end__

trainer.shutdown()

# __torch_model_start__
import torch.nn as nn

def model_creator(config):
    """Constructor function for the model(s) to be optimized.

    You will also need to provide a custom training
    function to specify the optimization procedure for multiple models.

    Args:
        config (dict): Configuration dictionary passed into ``TorchTrainer``.

    Returns:
        One or more torch.nn.Module objects.
    """
    return nn.Linear(1, 1)
# __torch_model_end__


# __torch_optimizer_start__
import torch

def optimizer_creator(model, config):
    """Constructor of one or more Torch optimizers.

    Args:
        models: The return values from ``model_creator``. This can be one
            or more torch nn modules.
        config (dict): Configuration dictionary passed into ``TorchTrainer``.

    Returns:
        One or more Torch optimizer objects.
    """
    return torch.optim.SGD(model.parameters(), lr=config.get("lr", 1e-4))
# __torch_optimizer_end__


# __torch_data_start__
from torch.utils.data import DataLoader
from ray.util.sgd.torch.examples.train_example import LinearDataset

def data_creator(config):
    """Constructs Iterables for training and validation.

    Note that even though two Iterable objects can be returned,
    only one Iterable will be used for training.

    Args:
        config: Configuration dictionary passed into ``TorchTrainer``

    Returns:
        One or Two Iterable objects. If only one Iterable object is provided,
        ``trainer.validate()`` will throw a ValueError.
    """
    train_dataset, val_dataset = LinearDataset(2, 5), LinearDataset(2, 5)
    train_loader = DataLoader(train_dataset, batch_size=config["batch_size"])
    val_loader = DataLoader(val_dataset, batch_size=config["batch_size"])
    return train_loader, val_loader
# __torch_data_end__

# __torch_loss_start__
import torch

def loss_creator(config):
    """Constructs the Torch Loss object.

    Note that optionally, you can pass in a Torch Loss constructor directly
    into the TorchTrainer (i.e., ``TorchTrainer(loss_creator=nn.BCELoss, ...)``).

    Args:
        config: Configuration dictionary passed into ``TorchTrainer``

    Returns:
        Torch Loss object.
    """
    return torch.nn.BCELoss()
# __torch_loss_end__

# __torch_scheduler_start__
import torch

def scheduler_creator(optimizer, config):
    """Constructor of one or more Torch optimizer schedulers.

    Args:
        optimizers: The return values from ``optimizer_creator``.
            This can be one or more torch optimizer objects.
        config: Configuration dictionary passed into ``TorchTrainer``

    Returns:
        One or more Torch scheduler objects.
    """
    return torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.9)

# __torch_scheduler_end__

# __backwards_compat_start__
from ray.util.sgd import TorchTrainer

MyTrainingOperator = TrainingOperator.from_creators(
    model_creator=model_creator, optimizer_creator=optimizer_creator,
    loss_creator=loss_creator, scheduler_creator=scheduler_creator,
    data_creator=data_creator)

trainer = TorchTrainer(
    training_operator_cls=MyTrainingOperator,
    scheduler_step_freq="epoch",  # if scheduler_creator is passed in
    config={"lr": 0.001, "batch_size": 64})

# __backwards_compat_end__

trainer.shutdown()

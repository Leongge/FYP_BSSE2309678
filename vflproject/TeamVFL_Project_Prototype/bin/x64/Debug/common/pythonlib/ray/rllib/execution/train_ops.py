import logging
import numpy as np
import math
from typing import Dict, List, Tuple, Any

import ray
from ray.rllib.evaluation.worker_set import WorkerSet
from ray.rllib.execution.common import \
    AGENT_STEPS_TRAINED_COUNTER, APPLY_GRADS_TIMER, COMPUTE_GRADS_TIMER, \
    LAST_TARGET_UPDATE_TS, LEARN_ON_BATCH_TIMER, \
    LOAD_BATCH_TIMER, NUM_TARGET_UPDATES, STEPS_SAMPLED_COUNTER, \
    STEPS_TRAINED_COUNTER, STEPS_TRAINED_THIS_ITER_COUNTER, \
    WORKER_UPDATE_TIMER, _check_sample_batch_type, \
    _get_global_vars, _get_shared_metrics
from ray.rllib.policy.sample_batch import DEFAULT_POLICY_ID, MultiAgentBatch
from ray.rllib.utils.annotations import ExperimentalAPI
from ray.rllib.utils.deprecation import DEPRECATED_VALUE, deprecation_warning
from ray.rllib.utils.framework import try_import_tf
from ray.rllib.utils.metrics import NUM_ENV_STEPS_TRAINED, \
    NUM_AGENT_STEPS_TRAINED
from ray.rllib.utils.metrics.learner_info import LearnerInfoBuilder, \
    LEARNER_INFO
from ray.rllib.utils.sgd import do_minibatch_sgd
from ray.rllib.utils.typing import PolicyID, SampleBatchType, ModelGradients

tf1, tf, tfv = try_import_tf()

logger = logging.getLogger(__name__)


@ExperimentalAPI
def train_one_step(trainer, train_batch) -> Dict:
    config = trainer.config
    workers = trainer.workers
    local_worker = workers.local_worker()
    policies = local_worker.policies_to_train
    num_sgd_iter = config.get("sgd_num_iter", 1)
    sgd_minibatch_size = config.get("sgd_minibatch_size", 0)

    learn_timer = trainer._timers[LEARN_ON_BATCH_TIMER]
    with learn_timer:
        # Subsample minibatches (size=`sgd_minibatch_size`) from the
        # train batch and loop through train batch `num_sgd_iter` times.
        if num_sgd_iter > 1 or sgd_minibatch_size > 0:
            info = do_minibatch_sgd(
                train_batch,
                {pid: local_worker.get_policy(pid)
                 for pid in policies}, local_worker, num_sgd_iter,
                sgd_minibatch_size, [])
        # Single update step using train batch.
        else:
            info = local_worker.learn_on_batch(train_batch)

    learn_timer.push_units_processed(train_batch.count)
    trainer._counters[NUM_ENV_STEPS_TRAINED] += train_batch.count
    trainer._counters[NUM_AGENT_STEPS_TRAINED] += train_batch.agent_steps()

    # Update weights - after learning on the local worker - on all remote
    # workers.
    if workers.remote_workers():
        with trainer._timers[WORKER_UPDATE_TIMER]:
            weights = ray.put(workers.local_worker().get_weights(policies))
            for e in workers.remote_workers():
                e.set_weights.remote(weights)
    return info


@ExperimentalAPI
def multi_gpu_train_one_step(trainer, train_batch) -> Dict:
    config = trainer.config
    workers = trainer.workers
    local_worker = workers.local_worker()
    policies = local_worker.policies_to_train
    num_sgd_iter = config.get("sgd_num_iter", 1)
    sgd_minibatch_size = config.get("sgd_minibatch_size",
                                    config["train_batch_size"])

    # Determine the number of devices (GPUs or 1 CPU) we use.
    num_devices = int(math.ceil(config["num_gpus"] or 1))

    # Make sure total batch size is dividable by the number of devices.
    # Batch size per tower.
    per_device_batch_size = sgd_minibatch_size // num_devices
    # Total batch size.
    batch_size = per_device_batch_size * num_devices
    assert batch_size % num_devices == 0
    assert batch_size >= num_devices, "Batch size too small!"

    # Handle everything as if multi-agent.
    train_batch = train_batch.as_multi_agent()

    # Load data into GPUs.
    load_timer = trainer._timers[LOAD_BATCH_TIMER]
    with load_timer:
        num_loaded_samples = {}
        for policy_id, batch in train_batch.policy_batches.items():
            # Not a policy-to-train.
            if policy_id not in policies:
                continue

            # Decompress SampleBatch, in case some columns are compressed.
            batch.decompress_if_needed()

            # Load the entire train batch into the Policy's only buffer
            # (idx=0). Policies only have >1 buffers, if we are training
            # asynchronously.
            num_loaded_samples[policy_id] = local_worker.policy_map[
                policy_id].load_batch_into_buffer(
                    batch, buffer_index=0)

    # Execute minibatch SGD on loaded data.
    learn_timer = trainer._timers[LEARN_ON_BATCH_TIMER]
    with learn_timer:
        # Use LearnerInfoBuilder as a unified way to build the final
        # results dict from `learn_on_loaded_batch` call(s).
        # This makes sure results dicts always have the same structure
        # no matter the setup (multi-GPU, multi-agent, minibatch SGD,
        # tf vs torch).
        learner_info_builder = LearnerInfoBuilder(num_devices=num_devices)

        for policy_id, samples_per_device in num_loaded_samples.items():
            policy = local_worker.policy_map[policy_id]
            num_batches = max(
                1,
                int(samples_per_device) // int(per_device_batch_size))
            logger.debug("== sgd epochs for {} ==".format(policy_id))
            for _ in range(num_sgd_iter):
                permutation = np.random.permutation(num_batches)
                for batch_index in range(num_batches):
                    # Learn on the pre-loaded data in the buffer.
                    # Note: For minibatch SGD, the data is an offset into
                    # the pre-loaded entire train batch.
                    results = policy.learn_on_loaded_batch(
                        permutation[batch_index] * per_device_batch_size,
                        buffer_index=0)

                    learner_info_builder.add_learn_on_batch_results(
                        results, policy_id)

        # Tower reduce and finalize results.
        learner_info = learner_info_builder.finalize()

    load_timer.push_units_processed(train_batch.count)
    learn_timer.push_units_processed(train_batch.count)

    trainer._counters[NUM_ENV_STEPS_TRAINED] += train_batch.count
    trainer._counters[NUM_AGENT_STEPS_TRAINED] += train_batch.agent_steps()

    # Update weights - after learning on the local worker - on all remote
    # workers.
    if workers.remote_workers():
        with trainer._timers[WORKER_UPDATE_TIMER]:
            weights = ray.put(workers.local_worker().get_weights(policies))
            for e in workers.remote_workers():
                e.set_weights.remote(weights)

    return learner_info


class TrainOneStep:
    """Callable that improves the policy and updates workers.

    This should be used with the .for_each() operator. A tuple of the input
    and learner stats will be returned.

    Examples:
        >>> rollouts = ParallelRollouts(...)
        >>> train_op = rollouts.for_each(TrainOneStep(workers))
        >>> print(next(train_op))  # This trains the policy on one batch.
        SampleBatch(...), {"learner_stats": ...}

    Updates the STEPS_TRAINED_COUNTER counter and LEARNER_INFO field in the
    local iterator context.
    """

    def __init__(self,
                 workers: WorkerSet,
                 policies: List[PolicyID] = frozenset([]),
                 num_sgd_iter: int = 1,
                 sgd_minibatch_size: int = 0):
        self.workers = workers
        self.local_worker = workers.local_worker()
        self.policies = policies
        self.num_sgd_iter = num_sgd_iter
        self.sgd_minibatch_size = sgd_minibatch_size

    def __call__(self,
                 batch: SampleBatchType) -> (SampleBatchType, List[dict]):
        _check_sample_batch_type(batch)
        metrics = _get_shared_metrics()
        learn_timer = metrics.timers[LEARN_ON_BATCH_TIMER]
        with learn_timer:
            # Subsample minibatches (size=`sgd_minibatch_size`) from the
            # train batch and loop through train batch `num_sgd_iter` times.
            if self.num_sgd_iter > 1 or self.sgd_minibatch_size > 0:
                lw = self.workers.local_worker()
                learner_info = do_minibatch_sgd(
                    batch, {
                        pid: lw.get_policy(pid)
                        for pid in self.policies
                        or self.local_worker.policies_to_train
                    }, lw, self.num_sgd_iter, self.sgd_minibatch_size, [])
            # Single update step using train batch.
            else:
                learner_info = \
                    self.workers.local_worker().learn_on_batch(batch)

            metrics.info[LEARNER_INFO] = learner_info
            learn_timer.push_units_processed(batch.count)
        metrics.counters[STEPS_TRAINED_COUNTER] += batch.count
        metrics.counters[STEPS_TRAINED_THIS_ITER_COUNTER] = batch.count
        if isinstance(batch, MultiAgentBatch):
            metrics.counters[
                AGENT_STEPS_TRAINED_COUNTER] += batch.agent_steps()
        # Update weights - after learning on the local worker - on all remote
        # workers.
        if self.workers.remote_workers():
            with metrics.timers[WORKER_UPDATE_TIMER]:
                weights = ray.put(self.workers.local_worker().get_weights(
                    self.policies or self.local_worker.policies_to_train))
                for e in self.workers.remote_workers():
                    e.set_weights.remote(weights, _get_global_vars())
        # Also update global vars of the local worker.
        self.workers.local_worker().set_global_vars(_get_global_vars())
        return batch, learner_info


class MultiGPUTrainOneStep:
    """Multi-GPU version of TrainOneStep.

    This should be used with the .for_each() operator. A tuple of the input
    and learner stats will be returned.

    Examples:
        >>> rollouts = ParallelRollouts(...)
        >>> train_op = rollouts.for_each(MultiGPUTrainOneStep(workers, ...))
        >>> print(next(train_op))  # This trains the policy on one batch.
        SampleBatch(...), {"learner_stats": ...}

    Updates the STEPS_TRAINED_COUNTER counter and LEARNER_INFO field in the
    local iterator context.
    """

    def __init__(
            self,
            *,
            workers: WorkerSet,
            sgd_minibatch_size: int,
            num_sgd_iter: int,
            num_gpus: int,
            _fake_gpus: bool = False,
            # Deprecated args.
            shuffle_sequences=DEPRECATED_VALUE,
            framework=DEPRECATED_VALUE):
        if framework != DEPRECATED_VALUE or \
                shuffle_sequences != DEPRECATED_VALUE:
            deprecation_warning(
                old="MultiGPUTrainOneStep(framework=..., "
                "shuffle_sequences=...)",
                error=False)

        self.workers = workers
        self.local_worker = workers.local_worker()
        self.num_sgd_iter = num_sgd_iter
        self.sgd_minibatch_size = sgd_minibatch_size
        self.shuffle_sequences = shuffle_sequences

        # Collect actual GPU devices to use.
        if not num_gpus:
            _fake_gpus = True
            num_gpus = 1
        type_ = "cpu" if _fake_gpus else "gpu"
        self.devices = [
            "/{}:{}".format(type_, 0 if _fake_gpus else i)
            for i in range(int(math.ceil(num_gpus)))
        ]

        # Make sure total batch size is dividable by the number of devices.
        # Batch size per tower.
        self.per_device_batch_size = sgd_minibatch_size // len(self.devices)
        # Total batch size.
        self.batch_size = self.per_device_batch_size * len(self.devices)
        assert self.batch_size % len(self.devices) == 0
        assert self.batch_size >= len(self.devices), "Batch size too small!"

    def __call__(self,
                 samples: SampleBatchType) -> (SampleBatchType, List[dict]):
        _check_sample_batch_type(samples)

        # Handle everything as if multi agent.
        samples = samples.as_multi_agent()

        metrics = _get_shared_metrics()
        load_timer = metrics.timers[LOAD_BATCH_TIMER]
        learn_timer = metrics.timers[LEARN_ON_BATCH_TIMER]
        # Load data into GPUs.
        with load_timer:
            num_loaded_samples = {}
            for policy_id, batch in samples.policy_batches.items():
                # Not a policy-to-train.
                if policy_id not in self.local_worker.policies_to_train:
                    continue

                # Decompress SampleBatch, in case some columns are compressed.
                batch.decompress_if_needed()

                # Load the entire train batch into the Policy's only buffer
                # (idx=0). Policies only have >1 buffers, if we are training
                # asynchronously.
                num_loaded_samples[policy_id] = self.local_worker.policy_map[
                    policy_id].load_batch_into_buffer(
                        batch, buffer_index=0)

        # Execute minibatch SGD on loaded data.
        with learn_timer:
            # Use LearnerInfoBuilder as a unified way to build the final
            # results dict from `learn_on_loaded_batch` call(s).
            # This makes sure results dicts always have the same structure
            # no matter the setup (multi-GPU, multi-agent, minibatch SGD,
            # tf vs torch).
            learner_info_builder = LearnerInfoBuilder(
                num_devices=len(self.devices))

            for policy_id, samples_per_device in num_loaded_samples.items():
                policy = self.local_worker.policy_map[policy_id]
                num_batches = max(
                    1,
                    int(samples_per_device) // int(self.per_device_batch_size))
                logger.debug("== sgd epochs for {} ==".format(policy_id))
                for _ in range(self.num_sgd_iter):
                    permutation = np.random.permutation(num_batches)
                    for batch_index in range(num_batches):
                        # Learn on the pre-loaded data in the buffer.
                        # Note: For minibatch SGD, the data is an offset into
                        # the pre-loaded entire train batch.
                        results = policy.learn_on_loaded_batch(
                            permutation[batch_index] *
                            self.per_device_batch_size,
                            buffer_index=0)

                        learner_info_builder.add_learn_on_batch_results(
                            results, policy_id)

            # Tower reduce and finalize results.
            learner_info = learner_info_builder.finalize()

        load_timer.push_units_processed(samples.count)
        learn_timer.push_units_processed(samples.count)

        metrics.counters[STEPS_TRAINED_COUNTER] += samples.count
        metrics.counters[STEPS_TRAINED_THIS_ITER_COUNTER] = samples.count
        metrics.counters[AGENT_STEPS_TRAINED_COUNTER] += samples.agent_steps()
        metrics.info[LEARNER_INFO] = learner_info

        if self.workers.remote_workers():
            with metrics.timers[WORKER_UPDATE_TIMER]:
                weights = ray.put(self.workers.local_worker().get_weights(
                    self.local_worker.policies_to_train))
                for e in self.workers.remote_workers():
                    e.set_weights.remote(weights, _get_global_vars())

        # Also update global vars of the local worker.
        self.workers.local_worker().set_global_vars(_get_global_vars())
        return samples, learner_info


# Backward compatibility.
TrainTFMultiGPU = MultiGPUTrainOneStep


class ComputeGradients:
    """Callable that computes gradients with respect to the policy loss.

    This should be used with the .for_each() operator.

    Examples:
        >>> grads_op = rollouts.for_each(ComputeGradients(workers))
        >>> print(next(grads_op))
        {"var_0": ..., ...}, 50  # grads, batch count

    Updates the LEARNER_INFO info field in the local iterator context.
    """

    def __init__(self, workers: WorkerSet):
        self.workers = workers

    def __call__(self, samples: SampleBatchType) -> Tuple[ModelGradients, int]:
        _check_sample_batch_type(samples)
        metrics = _get_shared_metrics()
        with metrics.timers[COMPUTE_GRADS_TIMER]:
            grad, info = self.workers.local_worker().compute_gradients(samples)
        # RolloutWorker.compute_gradients returns pure single agent stats
        # in a non-multi agent setup.
        if isinstance(samples, MultiAgentBatch):
            metrics.info[LEARNER_INFO] = info
        else:
            metrics.info[LEARNER_INFO] = {DEFAULT_POLICY_ID: info}
        return grad, samples.count


class ApplyGradients:
    """Callable that applies gradients and updates workers.

    This should be used with the .for_each() operator.

    Examples:
        >>> apply_op = grads_op.for_each(ApplyGradients(workers))
        >>> print(next(apply_op))
        None

    Updates the STEPS_TRAINED_COUNTER counter in the local iterator context.
    """

    def __init__(self,
                 workers,
                 policies: List[PolicyID] = frozenset([]),
                 update_all=True):
        """Creates an ApplyGradients instance.

        Args:
            workers (WorkerSet): workers to apply gradients to.
            update_all (bool): If true, updates all workers. Otherwise, only
                update the worker that produced the sample batch we are
                currently processing (i.e., A3C style).
        """
        self.workers = workers
        self.local_worker = workers.local_worker()
        self.policies = policies
        self.update_all = update_all

    def __call__(self, item: Tuple[ModelGradients, int]) -> None:
        if not isinstance(item, tuple) or len(item) != 2:
            raise ValueError(
                "Input must be a tuple of (grad_dict, count), got {}".format(
                    item))
        gradients, count = item
        metrics = _get_shared_metrics()
        metrics.counters[STEPS_TRAINED_COUNTER] += count
        metrics.counters[STEPS_TRAINED_THIS_ITER_COUNTER] = count

        apply_timer = metrics.timers[APPLY_GRADS_TIMER]
        with apply_timer:
            self.workers.local_worker().apply_gradients(gradients)
            apply_timer.push_units_processed(count)

        # Also update global vars of the local worker.
        self.workers.local_worker().set_global_vars(_get_global_vars())

        if self.update_all:
            if self.workers.remote_workers():
                with metrics.timers[WORKER_UPDATE_TIMER]:
                    weights = ray.put(self.workers.local_worker().get_weights(
                        self.policies or self.local_worker.policies_to_train))
                    for e in self.workers.remote_workers():
                        e.set_weights.remote(weights, _get_global_vars())
        else:
            if metrics.current_actor is None:
                raise ValueError(
                    "Could not find actor to update. When "
                    "update_all=False, `current_actor` must be set "
                    "in the iterator context.")
            with metrics.timers[WORKER_UPDATE_TIMER]:
                weights = self.workers.local_worker().get_weights(
                    self.policies or self.local_worker.policies_to_train)
                metrics.current_actor.set_weights.remote(
                    weights, _get_global_vars())


class AverageGradients:
    """Callable that averages the gradients in a batch.

    This should be used with the .for_each() operator after a set of gradients
    have been batched with .batch().

    Examples:
        >>> batched_grads = grads_op.batch(32)
        >>> avg_grads = batched_grads.for_each(AverageGradients())
        >>> print(next(avg_grads))
        {"var_0": ..., ...}, 1600  # averaged grads, summed batch count
    """

    def __call__(self, gradients: List[Tuple[ModelGradients, int]]
                 ) -> Tuple[ModelGradients, int]:
        acc = None
        sum_count = 0
        for grad, count in gradients:
            if acc is None:
                acc = grad
            else:
                acc = [a + b for a, b in zip(acc, grad)]
            sum_count += count
        logger.info("Computing average of {} microbatch gradients "
                    "({} samples total)".format(len(gradients), sum_count))
        return acc, sum_count


class UpdateTargetNetwork:
    """Periodically call policy.update_target() on all trainable policies.

    This should be used with the .for_each() operator after training step
    has been taken.

    Examples:
        >>> train_op = ParallelRollouts(...).for_each(TrainOneStep(...))
        >>> update_op = train_op.for_each(
        ...     UpdateTargetIfNeeded(workers, target_update_freq=500))
        >>> print(next(update_op))
        None

    Updates the LAST_TARGET_UPDATE_TS and NUM_TARGET_UPDATES counters in the
    local iterator context. The value of the last update counter is used to
    track when we should update the target next.
    """

    def __init__(self,
                 workers: WorkerSet,
                 target_update_freq: int,
                 by_steps_trained: bool = False,
                 policies: List[PolicyID] = frozenset([])):
        self.workers = workers
        self.local_worker = workers.local_worker()
        self.target_update_freq = target_update_freq
        self.policies = policies
        if by_steps_trained:
            self.metric = STEPS_TRAINED_COUNTER
        else:
            self.metric = STEPS_SAMPLED_COUNTER

    def __call__(self, _: Any) -> None:
        metrics = _get_shared_metrics()
        cur_ts = metrics.counters[self.metric]
        last_update = metrics.counters[LAST_TARGET_UPDATE_TS]
        if cur_ts - last_update > self.target_update_freq:
            to_update = self.policies or self.local_worker.policies_to_train
            self.workers.local_worker().foreach_trainable_policy(
                lambda p, p_id: p_id in to_update and p.update_target())
            metrics.counters[NUM_TARGET_UPDATES] += 1
            metrics.counters[LAST_TARGET_UPDATE_TS] = cur_ts

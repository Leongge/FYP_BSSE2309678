from typing import (Any, Callable, Dict, List, TYPE_CHECKING, Type, Union,
                    Optional)

import distutils
import logging
import os
import time
from dataclasses import dataclass
import warnings

from inspect import isclass
from shlex import quote

import ray
import yaml
from ray.tune import TuneError
from ray.tune.callback import Callback
from ray.tune.checkpoint_manager import Checkpoint
from ray.tune.result import NODE_IP
from ray.util import get_node_ip_address
from ray.util.debug import log_once
from ray.tune.cluster_info import get_ssh_key, get_ssh_user
from ray.tune.sync_client import (CommandBasedClient, get_sync_client,
                                  get_cloud_sync_client, NOOP)
from ray.util.annotations import PublicAPI

if TYPE_CHECKING:
    from ray.tune.trial import Trial

logger = logging.getLogger(__name__)

# Syncing period for syncing checkpoints between nodes or to cloud.
SYNC_PERIOD = 300

CLOUD_CHECKPOINTING_URL = (
    "https://docs.ray.io/en/master/tune/user-guide.html#using-cloud-storage")
_log_sync_warned = False
_syncers = {}


def wait_for_sync():
    for syncer in _syncers.values():
        syncer.wait()


def set_sync_periods(sync_config: "SyncConfig"):
    """Sets sync period from config."""
    global SYNC_PERIOD
    SYNC_PERIOD = int(sync_config.sync_period)


def validate_sync_config(sync_config: "SyncConfig"):
    if sync_config.node_sync_period >= 0 or sync_config.cloud_sync_period >= 0:
        # Until fully deprecated, try to consolidate
        if (sync_config.node_sync_period >= 0
                and sync_config.cloud_sync_period >= 0):
            sync_period = min(sync_config.node_sync_period,
                              sync_config.cloud_sync_period)
        else:
            sync_period = max(sync_config.node_sync_period,
                              sync_config.cloud_sync_period)

        sync_config.sync_period = sync_period
        sync_config.node_sync_period = -1
        sync_config.cloud_sync_period = -1

        warnings.warn(
            "The `node_sync_period` and "
            "`cloud_sync_period` properties of `tune.SyncConfig` are "
            "deprecated. Pass the `sync_period` property instead. "
            "\nFor now, the lower of the two values (if provided) will "
            f"be used as the sync_period. This value is: {sync_period}",
            DeprecationWarning)

    if sync_config.sync_to_cloud or sync_config.sync_to_driver:
        if bool(sync_config.upload_dir):
            syncer = sync_config.sync_to_cloud
            help = "set"
        else:
            syncer = sync_config.sync_to_driver
            help = "not set"

        sync_config.syncer = syncer
        sync_config.sync_to_cloud = None
        sync_config.sync_to_driver = None

        warnings.warn(
            "The `sync_to_cloud` and `sync_to_driver` properties of "
            "`tune.SyncConfig` are deprecated. Pass the `syncer` property "
            "instead. Presence of an `upload_dir` decides if checkpoints "
            "are synced to cloud or not. Syncing to driver is "
            "automatically disabled if an `upload_dir` is given."
            f"\nFor now, as the upload dir is {help}, the respective "
            f"syncer is used. This value is: {syncer}", DeprecationWarning)


def log_sync_template(options=""):
    """Template enabling syncs between driver and worker when possible.
    Requires ray cluster to be started with the autoscaler. Also requires
    rsync to be installed.

    Args:
        options (str): Additional rsync options.

    Returns:
        Sync template with source and target parameters. None if rsync
        unavailable.
    """
    if not distutils.spawn.find_executable("rsync"):
        if log_once("tune:rsync"):
            logger.error("Log sync requires rsync to be installed.")
        return None
    global _log_sync_warned
    ssh_key = get_ssh_key()
    if ssh_key is None:
        if not _log_sync_warned:
            logger.debug("Log sync requires cluster to be setup with "
                         "`ray up`.")
            _log_sync_warned = True
        return None

    rsh = "ssh -i {ssh_key} -o ConnectTimeout=120s -o StrictHostKeyChecking=no"
    rsh = rsh.format(ssh_key=quote(ssh_key))
    template = "rsync {options} -savz -e {rsh} {{source}} {{target}}"
    return template.format(options=options, rsh=quote(rsh))


@PublicAPI
@dataclass
class SyncConfig:
    """Configuration object for syncing.

    If an ``upload_dir`` is specified, both experiment and trial checkpoints
    will be stored on remote (cloud) storage. Synchronization then only
    happens via this remote storage.

    Args:
        upload_dir (str): Optional URI to sync training results and checkpoints
            to (e.g. ``s3://bucket``, ``gs://bucket`` or ``hdfs://path``).
            Specifying this will enable cloud-based checkpointing.
        syncer (None|func|str): Function for syncing the local_dir to and
            from remote storage. If string, then it must be a string template
            that includes ``{source}`` and ``{target}`` for the syncer to run.
            If not provided, it defaults to rsync for non cloud-based storage,
            and to standard S3, gsutil or HDFS sync commands for cloud-based
            storage.
            If set to ``None``, no syncing will take place.
            Defaults to ``"auto"`` (auto detect).
        sync_on_checkpoint (bool): Force sync-down of trial checkpoint to
            driver (only non cloud-storage).
            If set to False, checkpoint syncing from worker to driver
            is asynchronous and best-effort. This does not affect persistent
            storage syncing. Defaults to True.
        sync_period (int): Syncing period for syncing between nodes.

    """
    upload_dir: Optional[str] = None
    syncer: Union[None, str] = "auto"

    sync_on_checkpoint: bool = True
    sync_period: int = 300

    # Deprecated arguments
    sync_to_cloud: Any = None
    sync_to_driver: Any = None
    node_sync_period: int = -1
    cloud_sync_period: int = -1

    def __post_init__(self):
        validate_sync_config(self)


class Syncer:
    def __init__(self, local_dir, remote_dir, sync_client=NOOP):
        """Syncs between two directories with the sync_function.

        Arguments:
            local_dir (str): Directory to sync. Uniquely identifies the syncer.
            remote_dir (str): Remote directory to sync with.
            sync_client (SyncClient): Client for syncing between local_dir and
                remote_dir. Defaults to a Noop.
        """
        self._local_dir = (os.path.join(local_dir, "")
                           if local_dir else local_dir)
        self._remote_dir = remote_dir
        self.last_sync_up_time = float("-inf")
        self.last_sync_down_time = float("-inf")
        self.sync_client = sync_client

    def sync_up_if_needed(self,
                          sync_period: int,
                          exclude: Optional[List] = None):
        """Syncs up if time since last sync up is greather than sync_period.

        Args:
            sync_period (int): Time period between subsequent syncs.
            exclude (List[str]): Pattern of files to exclude, e.g.
                ``["*/checkpoint_*]`` to exclude trial checkpoints.
        """

        if time.time() - self.last_sync_up_time > sync_period:
            self.sync_up(exclude)

    def sync_down_if_needed(self,
                            sync_period: int,
                            exclude: Optional[List] = None):
        """Syncs down if time since last sync down is greather than sync_period.

        Args:
            sync_period (int): Time period between subsequent syncs.
            exclude (List[str]): Pattern of files to exclude, e.g.
                ``["*/checkpoint_*]`` to exclude trial checkpoints.
        """
        if time.time() - self.last_sync_down_time > sync_period:
            self.sync_down(exclude)

    def sync_up(self, exclude: Optional[List] = None):
        """Attempts to start the sync-up to the remote path.

        Args:
            exclude (List[str]): Pattern of files to exclude, e.g.
                ``["*/checkpoint_*]`` to exclude trial checkpoints.

        Returns:
            Whether the sync (if feasible) was successfully started.
        """
        result = False
        if self.validate_hosts(self._local_dir, self._remote_path):
            try:
                result = self.sync_client.sync_up(
                    self._local_dir, self._remote_path, exclude=exclude)
                self.last_sync_up_time = time.time()
            except Exception:
                logger.exception("Sync execution failed.")
        return result

    def sync_down(self, exclude: Optional[List] = None):
        """Attempts to start the sync-down from the remote path.

        Args:
            exclude (List[str]): Pattern of files to exclude, e.g.
                ``["*/checkpoint_*]`` to exclude trial checkpoints.

        Returns:
             Whether the sync (if feasible) was successfully started.
        """
        result = False
        if self.validate_hosts(self._local_dir, self._remote_path):
            try:
                result = self.sync_client.sync_down(
                    self._remote_path, self._local_dir, exclude=exclude)
                self.last_sync_down_time = time.time()
            except Exception:
                logger.exception("Sync execution failed.")
        return result

    def validate_hosts(self, source, target):
        if not (source and target):
            logger.debug("Source or target is empty, skipping log sync for "
                         "{}".format(self._local_dir))
            return False
        return True

    def wait(self):
        """Waits for the sync client to complete the current sync."""
        self.sync_client.wait()

    def reset(self):
        self.last_sync_up_time = float("-inf")
        self.last_sync_down_time = float("-inf")
        self.sync_client.reset()

    def close(self):
        self.sync_client.close()

    @property
    def _remote_path(self):
        return self._remote_dir


class CloudSyncer(Syncer):
    """Syncer for syncing files to/from the cloud."""

    def __init__(self, local_dir, remote_dir, sync_client):
        super(CloudSyncer, self).__init__(local_dir, remote_dir, sync_client)

    def sync_up_if_needed(self, exclude: Optional[List] = None):
        return super(CloudSyncer, self).sync_up_if_needed(
            SYNC_PERIOD, exclude=exclude)

    def sync_down_if_needed(self, exclude: Optional[List] = None):
        return super(CloudSyncer, self).sync_down_if_needed(
            SYNC_PERIOD, exclude=exclude)


class NodeSyncer(Syncer):
    """Syncer for syncing files to/from a remote dir to a local dir."""

    def __init__(self, local_dir, remote_dir, sync_client):
        self.local_ip = get_node_ip_address()
        self.worker_ip = None
        super(NodeSyncer, self).__init__(local_dir, remote_dir, sync_client)

    def set_worker_ip(self, worker_ip):
        """Sets the worker IP to sync logs from."""
        self.worker_ip = worker_ip

    def has_remote_target(self):
        """Returns whether the Syncer has a remote target."""
        if not self.worker_ip:
            logger.debug("Worker IP unknown, skipping sync for %s",
                         self._local_dir)
            return False
        if self.worker_ip == self.local_ip:
            logger.debug("Worker IP is local IP, skipping sync for %s",
                         self._local_dir)
            return False
        return True

    def sync_up_if_needed(self, exclude: Optional[List] = None):
        if not self.has_remote_target():
            return True
        return super(NodeSyncer, self).sync_up_if_needed(
            SYNC_PERIOD, exclude=exclude)

    def sync_down_if_needed(self, exclude: Optional[List] = None):
        if not self.has_remote_target():
            return True
        return super(NodeSyncer, self).sync_down_if_needed(
            SYNC_PERIOD, exclude=exclude)

    def sync_up_to_new_location(self, worker_ip):
        if worker_ip != self.worker_ip:
            logger.debug("Setting new worker IP to %s", worker_ip)
            self.set_worker_ip(worker_ip)
            self.reset()
            if not self.sync_up():
                logger.warning(
                    "Sync up to new location skipped. This should not occur.")
        else:
            logger.warning("Sync attempted to same IP %s.", worker_ip)

    def sync_up(self, exclude: Optional[List] = None):
        if not self.has_remote_target():
            return True
        return super(NodeSyncer, self).sync_up(exclude=exclude)

    def sync_down(self, exclude: Optional[List] = None):
        if not self.has_remote_target():
            return True
        logger.debug("Syncing from %s to %s", self._remote_path,
                     self._local_dir)
        return super(NodeSyncer, self).sync_down(exclude=exclude)

    @property
    def _remote_path(self):
        ssh_user = get_ssh_user()
        global _log_sync_warned
        if not self.has_remote_target():
            return None
        if ssh_user is None:
            if not _log_sync_warned:
                logger.error("Syncer requires cluster to be setup with "
                             "`ray up`.")
                _log_sync_warned = True
            return None
        return "{}@{}:{}/".format(ssh_user, self.worker_ip, self._remote_dir)


def get_cloud_syncer(local_dir, remote_dir=None,
                     sync_function=None) -> CloudSyncer:
    """Returns a Syncer.

    This syncer is in charge of syncing the local_dir with upload_dir.

    If no ``remote_dir`` is provided, it will return a no-op syncer.

    If a ``sync_function`` is provided, it will return a CloudSyncer using
    a custom SyncClient initialized by the sync function. Otherwise it will
    return a CloudSyncer with default templates for s3/gs/hdfs.

    Args:
        local_dir (str): Source directory for syncing.
        remote_dir (str): Target directory for syncing. If not provided, a
            no-op Syncer is returned.
        sync_function (func | str): Function for syncing the local_dir to
            remote_dir. If string, then it must be a string template for
            syncer to run. If not provided, it defaults
            to standard S3, gsutil or HDFS sync commands.

    Raises:
        ValueError if malformed remote_dir.
    """
    key = (local_dir, remote_dir)

    if key in _syncers:
        return _syncers[key]

    if not remote_dir:
        _syncers[key] = CloudSyncer(local_dir, remote_dir, NOOP)
        return _syncers[key]

    if sync_function == "auto":
        sync_function = None  # Auto-detect

    # Maybe get user-provided sync client here
    client = get_sync_client(sync_function)

    if client:
        # If the user provided a sync template or function
        _syncers[key] = CloudSyncer(local_dir, remote_dir, client)
    else:
        # Else, get default cloud sync client (e.g. S3 syncer)
        sync_client = get_cloud_sync_client(remote_dir)
        _syncers[key] = CloudSyncer(local_dir, remote_dir, sync_client)

    return _syncers[key]


def get_node_syncer(local_dir, remote_dir=None, sync_function=None):
    """Returns a NodeSyncer.

    Args:
        local_dir (str): Source directory for syncing.
        remote_dir (str): Target directory for syncing. If not provided, a
            noop Syncer is returned.
        sync_function (func|str|bool): Function for syncing the local_dir to
            remote_dir. If string, then it must be a string template for
            syncer to run. If True or not provided, it defaults rsync. If
            False, a noop Syncer is returned.
    """
    if sync_function == "auto":
        sync_function = None  # Auto-detect

    key = (local_dir, remote_dir)
    if key in _syncers:
        return _syncers[key]
    elif isclass(sync_function) and issubclass(sync_function, Syncer):
        _syncers[key] = sync_function(local_dir, remote_dir, None)
        return _syncers[key]
    elif not remote_dir or sync_function is False:
        sync_client = NOOP
    elif sync_function and sync_function is not True:
        sync_client = get_sync_client(sync_function)
    else:
        sync = log_sync_template()
        if sync:
            sync_client = CommandBasedClient(sync, sync)
            sync_client.set_logdir(local_dir)
        else:
            sync_client = NOOP

    _syncers[key] = NodeSyncer(local_dir, remote_dir, sync_client)
    return _syncers[key]


class SyncerCallback(Callback):
    def __init__(self, sync_function: Union[None, bool, Callable]):
        self._sync_function = sync_function
        self._syncers: Dict["Trial", NodeSyncer] = {}

    def _get_trial_syncer(self, trial: "Trial"):
        if trial not in self._syncers:
            self._syncers[trial] = self._create_trial_syncer(trial)
        return self._syncers[trial]

    def _create_trial_syncer(self, trial: "Trial"):
        return get_node_syncer(
            trial.logdir,
            remote_dir=trial.logdir,
            sync_function=self._sync_function)

    def _sync_trial_checkpoint(self, trial: "Trial", checkpoint: Checkpoint):
        if checkpoint.storage == Checkpoint.MEMORY:
            return

        trial_syncer = self._get_trial_syncer(trial)
        # If the sync_function is False, syncing to driver is disabled.
        # In every other case (valid values include None, True Callable,
        # NodeSyncer) syncing to driver is enabled.
        if trial.sync_on_checkpoint and self._sync_function is not False:
            try:
                # Wait for any other syncs to finish. We need to sync again
                # after this to handle checkpoints taken mid-sync.
                trial_syncer.wait()
            except TuneError as e:
                # Errors occurring during this wait are not fatal for this
                # checkpoint, so it should just be logged.
                logger.error(
                    "Trial %s: An error occurred during the "
                    "checkpoint pre-sync wait - %s", trial, str(e))
            # Force sync down and wait before tracking the new checkpoint.
            try:
                if trial_syncer.sync_down():
                    trial_syncer.wait()
                else:
                    logger.error(
                        "Trial %s: Checkpoint sync skipped. "
                        "This should not happen.", trial)
            except TuneError as e:
                if trial.uses_cloud_checkpointing:
                    # Even though rsync failed the trainable can restore
                    # from remote durable storage.
                    logger.error("Trial %s: Sync error - %s", trial, str(e))
                else:
                    # If the trainable didn't have remote storage to upload
                    # to then this checkpoint may have been lost, so we
                    # shouldn't track it with the checkpoint_manager.
                    raise e
            if not trial.uses_cloud_checkpointing:
                if not os.path.exists(checkpoint.value):
                    raise TuneError("Trial {}: Checkpoint path {} not "
                                    "found after successful sync down. "
                                    "Are you running on a Kubernetes or "
                                    "managed cluster? rsync will not function "
                                    "due to a lack of SSH functionality. "
                                    "You'll need to use cloud-checkpointing "
                                    "if that's the case, see instructions "
                                    "here: {} .".format(
                                        trial, checkpoint.value,
                                        CLOUD_CHECKPOINTING_URL))

    def on_trial_start(self, iteration: int, trials: List["Trial"],
                       trial: "Trial", **info):
        self._get_trial_syncer(trial)

    def on_trial_result(self, iteration: int, trials: List["Trial"],
                        trial: "Trial", result: Dict, **info):
        trial_syncer = self._get_trial_syncer(trial)
        trial_syncer.set_worker_ip(result.get(NODE_IP))
        trial_syncer.sync_down_if_needed()

    def on_trial_complete(self, iteration: int, trials: List["Trial"],
                          trial: "Trial", **info):
        trial_syncer = self._get_trial_syncer(trial)
        if NODE_IP in trial.last_result:
            trainable_ip = trial.last_result[NODE_IP]
        else:
            trainable_ip = ray.get(trial.runner.get_current_ip.remote())
        trial_syncer.set_worker_ip(trainable_ip)
        trial_syncer.sync_down_if_needed()
        trial_syncer.close()

    def on_checkpoint(self, iteration: int, trials: List["Trial"],
                      trial: "Trial", checkpoint: Checkpoint, **info):
        self._sync_trial_checkpoint(trial, checkpoint)


def detect_cluster_syncer(
        sync_config: Optional[SyncConfig],
        cluster_config_file: str = "~/ray_bootstrap_config.yaml"
) -> Union[bool, Type, NodeSyncer]:
    """Detect cluster Syncer given SyncConfig.

    Returns False if cloud checkpointing is enabled (when upload dir is
    set).

    Else, returns sync config syncer if manually specified.

    Else, detects cluster environment (e.g. Docker, Kubernetes) and returns
    syncer accordingly.

    """
    from ray.tune.integration.docker import DockerSyncer

    sync_config = sync_config or SyncConfig()

    if bool(sync_config.upload_dir) or sync_config.syncer is None:
        # No sync to driver for cloud checkpointing or if manually disabled
        return False

    _syncer = sync_config.syncer

    if _syncer == "auto":
        _syncer = None

    if isinstance(_syncer, Type):
        return _syncer

    # Else: True or None. Auto-detect.
    cluster_config_file = os.path.expanduser(cluster_config_file)
    if not os.path.exists(cluster_config_file):
        return _syncer

    with open(cluster_config_file, "rt") as fp:
        config = yaml.safe_load(fp.read())

    if config.get("docker"):
        logger.debug(
            "Detected docker autoscaling environment. Using `DockerSyncer` "
            "as sync client. If this is not correct or leads to errors, "
            "please pass a `syncer` parameter in the `SyncConfig` to "
            "`tune.run().` to manually configure syncing behavior.")
        return DockerSyncer

    if config.get("provider", {}).get("type", "") == "kubernetes":
        from ray.tune.integration.kubernetes import (
            NamespacedKubernetesSyncer, try_import_kubernetes)
        if not try_import_kubernetes():
            logger.warning(
                "Detected Ray autoscaling environment on Kubernetes, "
                "but Kubernetes Python CLI is not installed. "
                "Checkpoint syncing may not work properly across "
                "multiple pods. Be sure to install 'kubernetes' on "
                "each container.")

        namespace = config["provider"].get("namespace", "ray")
        logger.debug(
            f"Detected Ray autoscaling environment on Kubernetes. Using "
            f"`NamespacedKubernetesSyncer` with namespace `{namespace}` "
            f"as sync client. If this is not correct or leads to errors, "
            f"please pass a `syncer` parameter in the `SyncConfig` "
            f"to `tune.run()` to manually configure syncing behavior..")
        return NamespacedKubernetesSyncer(namespace)

    return _syncer

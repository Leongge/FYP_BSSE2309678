import os
import sys
import json
import logging
import yaml
import hashlib
import subprocess
import runpy
import shutil

from filelock import FileLock
from typing import Optional, List, Dict, Any, Set
from pathlib import Path

import ray

from ray._private.runtime_env.utils import RuntimeEnv
from ray._private.runtime_env.conda_utils import (
    get_conda_activate_commands, create_conda_env, delete_conda_env)
from ray._private.runtime_env.context import RuntimeEnvContext
from ray._private.utils import (get_wheel_filename, get_master_wheel_url,
                                get_release_wheel_url, try_to_create_directory)
from ray._private.runtime_env.packaging import Protocol, parse_uri

default_logger = logging.getLogger(__name__)


def _resolve_current_ray_path() -> str:
    # When ray is built from source with pip install -e,
    # ray.__file__ returns .../python/ray/__init__.py and this function returns
    # ".../python".
    # When ray is installed from a prebuilt binary, ray.__file__ returns
    # .../site-packages/ray/__init__.py and this function returns
    # ".../site-packages".
    return os.path.split(os.path.split(ray.__file__)[0])[0]


def _get_ray_setup_spec():
    """Find the Ray setup_spec from the currently running Ray.

    This function works even when Ray is built from source with pip install -e.
    """
    ray_source_python_path = _resolve_current_ray_path()
    setup_py_path = os.path.join(ray_source_python_path, "setup.py")
    return runpy.run_path(setup_py_path)["setup_spec"]


def _resolve_install_from_source_ray_dependencies():
    """Find the Ray dependencies when Ray is installed from source."""
    return _get_ray_setup_spec().install_requires


def _resolve_install_from_source_ray_extras() -> Dict[str, List[str]]:
    return _get_ray_setup_spec().extras


def _inject_ray_to_conda_site(
        conda_path, logger: Optional[logging.Logger] = default_logger):
    """Write the current Ray site package directory to a new site"""
    python_binary = os.path.join(conda_path, "bin/python")
    site_packages_path = subprocess.check_output(
        [python_binary, "-c",
         "import site; print(site.getsitepackages()[0])"]).decode().strip()

    ray_path = _resolve_current_ray_path()
    logger.warning(f"Injecting {ray_path} to environment {conda_path} "
                   "because _inject_current_ray flag is on.")

    maybe_ray_dir = os.path.join(site_packages_path, "ray")
    if os.path.isdir(maybe_ray_dir):
        logger.warning(f"Replacing existing ray installation with {ray_path}")
        shutil.rmtree(maybe_ray_dir)

    # See usage of *.pth file at
    # https://docs.python.org/3/library/site.html
    with open(os.path.join(site_packages_path, "ray.pth"), "w") as f:
        f.write(ray_path)


def _current_py_version():
    return ".".join(map(str, sys.version_info[:3]))  # like 3.6.10


def current_ray_pip_specifier(
        logger: Optional[logging.Logger] = default_logger) -> Optional[str]:
    """The pip requirement specifier for the running version of Ray.

    Returns:
        A string which can be passed to `pip install` to install the
        currently running Ray version, or None if running on a version
        built from source locally (likely if you are developing Ray).

    Examples:
        Returns "https://s3-us-west-2.amazonaws.com/ray-wheels/[..].whl"
            if running a stable release, a nightly or a specific commit
    """
    if os.environ.get("RAY_CI_POST_WHEEL_TESTS"):
        # Running in Buildkite CI after the wheel has been built.
        # Wheels are at in the ray/.whl directory, but use relative path to
        # allow for testing locally if needed.
        return os.path.join(
            Path(ray.__file__).resolve().parents[2], ".whl",
            get_wheel_filename())
    elif ray.__commit__ == "{{RAY_COMMIT_SHA}}":
        # Running on a version built from source locally.
        if os.environ.get("RAY_RUNTIME_ENV_LOCAL_DEV_MODE") != "1":
            logger.warning(
                "Current Ray version could not be detected, most likely "
                "because you have manually built Ray from source.  To use "
                "runtime_env in this case, set the environment variable "
                "RAY_RUNTIME_ENV_LOCAL_DEV_MODE=1.")
        return None
    elif "dev" in ray.__version__:
        # Running on a nightly wheel.
        return get_master_wheel_url()
    else:
        return get_release_wheel_url()


def inject_dependencies(
        conda_dict: Dict[Any, Any],
        py_version: str,
        pip_dependencies: Optional[List[str]] = None) -> Dict[Any, Any]:
    """Add Ray, Python and (optionally) extra pip dependencies to a conda dict.

    Args:
        conda_dict (dict): A dict representing the JSON-serialized conda
            environment YAML file.  This dict will be modified and returned.
        py_version (str): A string representing a Python version to inject
            into the conda dependencies, e.g. "3.7.7"
        pip_dependencies (List[str]): A list of pip dependencies that
            will be prepended to the list of pip dependencies in
            the conda dict.  If the conda dict does not already have a "pip"
            field, one will be created.
    Returns:
        The modified dict.  (Note: the input argument conda_dict is modified
        and returned.)
    """
    if pip_dependencies is None:
        pip_dependencies = []
    if conda_dict.get("dependencies") is None:
        conda_dict["dependencies"] = []

    # Inject Python dependency.
    deps = conda_dict["dependencies"]

    # Add current python dependency.  If the user has already included a
    # python version dependency, conda will raise a readable error if the two
    # are incompatible, e.g:
    #   ResolvePackageNotFound: - python[version='3.5.*,>=3.6']
    deps.append(f"python={py_version}")

    if "pip" not in deps:
        deps.append("pip")

    # Insert pip dependencies.
    found_pip_dict = False
    for dep in deps:
        if isinstance(dep, dict) and dep.get("pip") and isinstance(
                dep["pip"], list):
            dep["pip"] = pip_dependencies + dep["pip"]
            found_pip_dict = True
            break
    if not found_pip_dict:
        deps.append({"pip": pip_dependencies})

    return conda_dict


def _get_conda_env_hash(conda_dict: Dict) -> str:
    # Set `sort_keys=True` so that different orderings yield the same hash.
    serialized_conda_spec = json.dumps(conda_dict, sort_keys=True)
    hash = hashlib.sha1(serialized_conda_spec.encode("utf-8")).hexdigest()
    return hash


def get_uri(runtime_env: Dict) -> Optional[str]:
    """Return `"conda://<hashed_dependencies>"`, or None if no GC required."""
    conda = runtime_env.get("conda")
    if conda is not None:
        if isinstance(conda, str):
            # User-preinstalled conda env.  We don't garbage collect these, so
            # we don't track them with URIs.
            uri = None
        elif isinstance(conda, dict):
            uri = "conda://" + _get_conda_env_hash(conda_dict=conda)
        else:
            raise TypeError("conda field received by RuntimeEnvAgent must be "
                            f"str or dict, not {type(conda).__name__}.")
    else:
        uri = None
    return uri


class CondaManager:
    def __init__(self, resources_dir: str):
        self._resources_dir = os.path.join(resources_dir, "conda")
        try_to_create_directory(self._resources_dir)
        self._created_envs: Set[str] = set()

    def _get_path_from_hash(self, hash: str) -> str:
        """Generate a path from the hash of a conda or pip spec.

        The output path also functions as the name of the conda environment
        when using the `--prefix` option to `conda create` and `conda remove`.

        Example output:
            /tmp/ray/session_2021-11-03_16-33-59_356303_41018/runtime_resources
                /conda/ray-9a7972c3a75f55e976e620484f58410c920db091
        """
        return os.path.join(self._resources_dir, hash)

    def delete_uri(self,
                   uri: str,
                   logger: Optional[logging.Logger] = default_logger) -> bool:
        logger.info(f"Got request to delete URI {uri}")
        protocol, hash = parse_uri(uri)
        if protocol != Protocol.CONDA:
            raise ValueError(
                "CondaManager can only delete URIs with protocol "
                f"conda.  Received protocol {protocol}, URI {uri}")

        conda_env_path = self._get_path_from_hash(hash)
        self._created_envs.remove(conda_env_path)
        successful = delete_conda_env(prefix=conda_env_path, logger=logger)
        if not successful:
            logger.warning(f"Error when deleting conda env {conda_env_path}. ")
        return successful

    def setup(self,
              runtime_env: RuntimeEnv,
              context: RuntimeEnvContext,
              logger: Optional[logging.Logger] = default_logger):
        if not runtime_env.has_conda():
            return

        logger.debug("Setting up conda or pip for runtime_env: "
                     f"{runtime_env.serialize()}")

        if runtime_env.conda_env_name():
            conda_env_name = runtime_env.conda_env_name()
        else:
            conda_dict = json.loads(runtime_env.conda_config())
            protocol, hash = parse_uri(runtime_env.conda_uri())
            conda_env_name = self._get_path_from_hash(hash)
            assert conda_dict is not None

            ray_pip = current_ray_pip_specifier(logger=logger)
            if ray_pip:
                extra_pip_dependencies = [ray_pip, "ray[default]"]
            elif runtime_env.get_extension("_inject_current_ray") == "True":
                extra_pip_dependencies = (
                    _resolve_install_from_source_ray_dependencies())
            else:
                extra_pip_dependencies = []
            conda_dict = inject_dependencies(conda_dict, _current_py_version(),
                                             extra_pip_dependencies)

            # It is not safe for multiple processes to install conda envs
            # concurrently, even if the envs are different, so use a global
            # lock for all conda installs.
            # See https://github.com/ray-project/ray/issues/17086
            file_lock_name = "ray-conda-install.lock"
            with FileLock(os.path.join(self._resources_dir, file_lock_name)):
                try:
                    conda_yaml_file = os.path.join(self._resources_dir,
                                                   "environment.yml")
                    with open(conda_yaml_file, "w") as file:
                        yaml.dump(conda_dict, file)

                    if conda_env_name in self._created_envs:
                        logger.debug(f"Conda env {conda_env_name} already "
                                     "created, skipping creation.")
                    else:
                        create_conda_env(
                            conda_yaml_file,
                            prefix=conda_env_name,
                            logger=logger)
                        self._created_envs.add(conda_env_name)
                finally:
                    os.remove(conda_yaml_file)

                if runtime_env.get_extension("_inject_current_ray"):
                    _inject_ray_to_conda_site(
                        conda_path=conda_env_name, logger=logger)

        context.py_executable = "python"
        context.command_prefix += get_conda_activate_commands(conda_env_name)
        logger.info(
            f"Finished setting up runtime environment at {conda_env_name}")

# Copyright (c) 2020, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of the Optimyzer Client, which is released under the BSD 3-Clause License.

"""The filesystem module handles reading and writing parameter data in the experiment folders."""
import json
import os
import subprocess
from operator import itemgetter
from typing import Any, Dict, List, NamedTuple, Union

from .external import symlink  # type: ignore


def _write_instance_config(directory: str, configuration: Dict[str, Any]) -> None:
    """
    Writes a given configuration into a directory.

    Parameters
    ----------
    directory : str
        the directory
    configuration : Dict[str, Any]
        the configuration dictionary
    """

    with open(os.path.join(directory, "config.json"), "w") as fp:
        json.dump(configuration, fp, sort_keys=True, indent=2)


def _read_instance_config(directory: str) -> Dict[str, Any]:
    """
    Reads a configuration file from a directory.

    Parameters
    ----------
    directory : str
        the directory

    Returns
    -------
    Dict[str, Any]
        the configuration dictionary
    """

    # Note: no try/except, FileNotFoundError should be handeled by the caller
    with open(os.path.join(directory, "config.json"), "r") as fp:
        configuration = dict(json.load(fp))

    return configuration


# pylint: disable=unsubscriptable-object
def _write_instance_value(directory: str, value: Union[float, int]) -> None:
    """
    Writes a given optimization value to a directory.

    Parameters
    ----------
    directory : str
        the directory
    value : Union[float, int]
        the value for this instance
    """

    value_dict = dict()
    value_dict["value"] = value
    with open(os.path.join(directory, "value.json"), "w") as fp:
        json.dump(value_dict, fp, sort_keys=True, indent=2)


def _read_instance_value(directory: str) -> float:
    """
    Reads optimization value from directory.

    Parameters
    ----------
    directory : str
        the directory

    Returns
    -------
    float
        the value
    """

    # Note: no try/except, FileNotFoundError should be handeled by the caller
    with open(os.path.join(directory, "value.json"), "r") as fp:
        value = float(json.load(fp)["value"])

    return value


# pylint: disable=inherit-non-class,too-few-public-methods
class Instance(NamedTuple):
    """Provides type hinting for the instance dict."""

    id: str
    value: float
    config: Dict[str, Any]


class EmptyWorkdirError(Exception):
    """Raised when there are no instances in the Optimyzer working directory."""


def _get_all_instances(directory: str) -> List[Instance]:
    """
    Collects all instances from a base directory.

    Parameters
    ----------
    directory : str
        an Optimyzer basedir

    Returns
    -------
    List[Tuple[str, float, Dict[str, Any]]]
        a list of instances, which are represented by (id, value, config) named  tuples
    """

    instances = list()
    dirs = next(os.walk(directory))[1]
    for instance_id in dirs:
        # exclude symlinks (Linux) and junctions (Windows)
        instancepath = os.path.join(directory, instance_id)
        if os.path.realpath(instancepath) != os.path.abspath(instancepath):
            continue

        metadatapath = os.path.join(instancepath, ".optimyzer")

        try:
            config = _read_instance_config(metadatapath)
        except FileNotFoundError:
            # no config means the instance wasn't really created, yet
            continue

        try:
            value = _read_instance_value(metadatapath)
        except FileNotFoundError:
            # no value means that the experiment isn't finished and we don't know how good it is
            continue

        instances.append(Instance(instance_id, value, config))

    return instances


def _get_best_instance(directory: str, minimize: bool) -> Instance:
    """
    Gets the best instance from a base directory.

    Parameters
    ----------
    directory : str
        an Optimyzer basedir
    minimze : bool
        whether smaller is better

    Returns
    -------
    Tuple[str, float, Dict[str, Any]]
        one instance, represented by (id, value, config) named  tuple
    """

    instances = _get_all_instances(directory)
    if instances:
        instances.sort(key=itemgetter(1), reverse=(not minimize))
        best_instance = instances[0]
        return best_instance
    else:
        raise EmptyWorkdirError("The base directory appears to be empty. Cannot get best instance.")


def _symlink(link: str, target: str) -> None:  # pragma: no cover
    """
    Create a operating-system depending symlink.
    """

    if os.name == "posix":
        symlink(target, link, overwrite=True)

    # on Windows, symlinks need admin rights, therefore we create a junction point instead
    elif os.name == "nt":
        # first, delete the old junction after checking it really is a link
        # check for junction: a linked path resolves to a different realpath
        if os.path.exists(target) and os.path.realpath(target) != target:
            os.unlink(target)

        # Python doesn't have an API for junction points, use shell command execution instead
        subprocess.check_call(
            'mklink /J "%s" "%s"' % (link, target),
            shell=True,
            stdout=subprocess.DEVNULL,
        )

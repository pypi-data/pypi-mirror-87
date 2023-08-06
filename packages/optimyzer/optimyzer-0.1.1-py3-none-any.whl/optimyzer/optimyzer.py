# Copyright (c) 2020, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of the Optimyzer Client, which is released under the BSD 3-Clause License.

"""The optimyzer module holds the core functionality of the Optimyzer framework."""

import hashlib
import json
import math
import os
from types import SimpleNamespace
from typing import Any, Dict, Union

from .filesystem import (
    EmptyWorkdirError,
    _get_best_instance,
    _symlink,
    _write_instance_config,
    _write_instance_value,
)
from .parameterspace import Parameter, ParameterSpace


class Configuration(SimpleNamespace):
    """
    Helper class to provide an object for each configuration, such that the individual
    parameters of the configuration are object attributes.
    """

    # pylint: disable=unsubscriptable-object
    def __init__(
        self,
        config_dict: Dict[str, Any],
        basepath: str,
        instance_id: str,
        value: Union[float, int] = math.nan,
    ) -> None:
        """
        Initialize a configuration, either empty or from a dict.

        Parameters
        ----------
        config_dict : Dict[str, Any], optional
            dict of the configuration, by default None
        basepath : str
            the basepath of this Optimyzer
        instance_id : str
            the id hash for this instance
        value : Union[float, int], optional
            the value of this instance, if it is finished, by default math.nan
        """

        self.id = instance_id
        self.workdir = os.path.join(basepath, instance_id)
        self.value = value

        if config_dict:
            super().__init__(**config_dict)
        else:
            super().__init__()

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the Configuration as dict

        Returns
        -------
        Dict[str, Any]
            the dict of this Configuration
        """
        return self.__dict__


class Optimyzer:
    """
    The Optimyzer class provides the functionality to define a parameter space and sample from it.
    It also handles different experiment folders, so that each experiment can run in its own
    directory.
    """

    def __init__(self, basedir: str, minimize: bool = False) -> None:
        """
        Parameters
        ----------
        basedir : str
            the directory where instances are written to
        minimize : bool, optional
            whether to minimize or not (in that case we maximize), by default False
        """

        self._basedir = os.path.abspath(basedir)
        self._parameterspace = ParameterSpace()
        self._optimal = False
        self._frozen = False
        self._minimize = minimize

        self._instance_config: Dict[str, Any] = dict()
        self._instance_id = ""
        self._instancedir = ""
        self._metadatadir = ""

    def add_parameter(self, parameter: Parameter) -> None:
        """
        Add parameter to the configuration of this Optimyzer instance.

        Parameters
        ----------
        parameter : Parameter
            parameter to add to Optimyzer
        """
        if not self._frozen:
            self._parameterspace.add(parameter)
        else:
            raise RuntimeError("You can only add parameters before creating a config.")

    def create_config(self, optimal: bool = False, chdir: bool = False) -> Configuration:
        """
        Create the configuration for this instance.

        Parameters
        ----------
        optimal: bool, optional
            whether to use the so-far best instance, by default False
        chdir: bool, optional
            whether to change directory into the instance directory, by default False

        Returns
        -------
        Configuration
            parameter configuration for this instance, includes the `id` and the `workdir`
        """

        # freeze this instance to avoid changes in the parameterspace
        self._frozen = True

        # we either return the optimal configuration or we sample from the parameterspace
        if optimal:
            best_instance = _get_best_instance(self._basedir, self._minimize)
            self._instance_config = best_instance.config
            self._instance_id = best_instance.id
            self._optimal = True
        else:
            self._instance_config = self._parameterspace.sample()
            print(f"Sampled the instance config {self._instance_config}.")
            self._instance_id = hashlib.sha256(
                json.dumps(self._instance_config, sort_keys=True).encode("utf-8")
            ).hexdigest()[0:20]

        self._instancedir = os.path.join(self._basedir, self._instance_id)
        self._metadatadir = os.path.join(self._instancedir, ".optimyzer")

        if not optimal:
            print(f"Creating directories for instance {self._instance_id}.")
            os.makedirs(self._metadatadir)

        if chdir:
            os.chdir(self._instancedir)

        # write configuration to JSON file
        if not optimal:
            _write_instance_config(self._metadatadir, self._instance_config)

        return Configuration(self._instance_config, self._basedir, self._instance_id)

    def get_config(self) -> Configuration:
        """
        Get the configuration for this instance.

        Returns
        -------
        Dict[str, Any]
            parameter configuration for this instance, includes the `id` and the `workdir`
        """
        if not self._instancedir:
            raise RuntimeError("Sorry, but you first have to call create_config()!")
        return Configuration(self._instance_config, self._basedir, self._instance_id)

    def get_workdir(self) -> str:
        """
        Get the absolute path of the working directory for this instance

        Returns
        -------
        str
            absolute path for this instance
        """
        if not self._instancedir:
            raise RuntimeError("Sorry, but you first have to call create_config()!")
        return self._instancedir

    # pylint: disable=unsubscriptable-object
    def report_result(self, result: Union[float, int]) -> None:
        """
        Report the result of this run to Optimyzer. By default, the result is a performance (higher
        is better). If you want to report a loss (lower is better), you have to initialize the
        Optimyzer instance with `minimize=True`.

        Parameters
        ----------
        result : Union[float, int]
            the result for this experiment, usually a performance or a loss
        """

        if not self._instancedir:
            raise RuntimeError("Sorry, but you first have to call get_config()!")

        if self._optimal:
            print(f"The result for this optimal run was was: {result}")
            raise RuntimeWarning("You're trying to report a result for the optimal configuration.")

        try:
            best_instance = _get_best_instance(self._basedir, self._minimize)
            best_value = best_instance.value
        except EmptyWorkdirError:
            best_value = math.nan

        print(f"Current result is {result}, best result so far was {best_value}")
        print(f"Reporting {result} for instance {self._instance_id}.")

        _write_instance_value(self._metadatadir, result)

        # update the symlink if this run is better than all other runs (or all others are nan)
        if (
            (self._minimize and result < best_value)
            or (not self._minimize and result > best_value)
            or math.isnan(best_value)
        ):
            _symlink(os.path.join(self._basedir, "best_instance"), self._instance_id)


# This method is top-level so that also users can use it to retrieve the best result.
def get_optimal_config(basedir: str = ".", minimize: bool = False) -> Configuration:
    """
    Get the best configuration.

    Parameters
    ----------
    basedir : str, optional
        base directory to get the optimal configuration from, by default "."
    minimize : bool, optional
        whether to minimize or not (in that case we maximize), by default False

    Returns
    -------
    Configuration
        parameter configuration for this instance, includes the `id`, the `workdir` and the
        `value` for this instance
    """

    instance = _get_best_instance(os.path.abspath(basedir), minimize)

    return Configuration(instance.config, os.path.abspath(basedir), instance.id, instance.value)

# Copyright (c) 2020, Gauss Machine Learning GmbH. All rights reserved.
# This file is part of the Optimyzer Client, which is released under the BSD 3-Clause License.

"""The parameterspace module contains different variants of parameters to optimize."""

import random
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple, Union


class ParameterSpace:
    """
    The `ParameterSpace` defines the space over which parameters are optimized. It holds individual
    parameters and exposes the ability to sample individual configurations.
    """

    def __init__(self) -> None:
        """
        Parameters
        ----------
        None
        """

        self.parameters = list()  # type: List[Parameter]

    def add(self, parameter: "Parameter") -> None:
        """
        Adds a parameter to the parameterspace.
        """
        if parameter.name == "workdir":
            raise RuntimeError("Parameters must not be called 'workdir'.")
        if parameter.name == "id":
            raise RuntimeError("Parameters must not be called 'id'.")
        if parameter.name == "value":
            raise RuntimeError("Parameters must not be called 'value'.")

        self.parameters.append(parameter)

    def sample(self) -> Dict[str, Any]:
        """
        Get an independent sample for each parameter of the parameterspace.

        Parameters
        ----------
        None

        Returns
        -------
        Configuration
            namespace with the individual parameters as the attributes. The values of each attribute
            is the sampled value for the parameter.
        """

        values = dict()
        for p in self.parameters:
            values[p.name] = p.sample()

        return values


class Parameter(ABC):  # pragma: no cover
    """
    Abstract base class for parameters.
    """

    @abstractmethod
    def __init__(self, name: str) -> None:
        """
        Parameters
        ----------
        name
            Name of the parameter.
        """

        self.name = name

    @abstractmethod
    def sample(self) -> Union[int, float, str]:
        """
        Get a sample from the parameter.

        Returns
        -------
        Union[int, float, str]
            The sample for the parameter, depending on the type.
        """


class FloatParameter(Parameter):
    """
    Continuous parameter with a range.
    """

    def __init__(self, name: str, parameter_range: Tuple[float, float]) -> None:
        """
        Parameters
        ----------
        name: str

        parameter_range: Tuple[float, float]
        """

        # check if the type is Tuple[float, float]
        if not (
            isinstance(parameter_range, tuple)
            and all(isinstance(x, (int, float)) for x in parameter_range)
        ):
            raise RuntimeError("FloatParameter needs a Tuple[float, float] to work.")

        if parameter_range[0] > parameter_range[1]:
            raise RuntimeError("The minimum must be smaller than the maximum.")

        self.parameter_range = parameter_range

        super().__init__(name)

    def sample(self) -> float:
        """
        Get a uniform sample within the range of the parameter.
        """

        minimum = self.parameter_range[0]
        maximum = self.parameter_range[1]

        return random.uniform(minimum, maximum)


class IntParameter(Parameter):
    """
    Integer parameter with a range.
    """

    def __init__(self, name: str, parameter_range: Tuple[int, int]) -> None:
        """
        Parameters
        ----------
        name: str

        parameter_range: Tuple[int, int]
        """

        # check if the type is Tuple[int, int]
        if not (
            isinstance(parameter_range, tuple) and all(isinstance(x, int) for x in parameter_range)
        ):
            raise RuntimeError("IntParameter needs a Tuple[int, int] to work.")

        if parameter_range[0] > parameter_range[1]:
            raise RuntimeError("The minimum must be smaller than the maximum.")

        self.parameter_range = parameter_range

        super().__init__(name)

    def sample(self) -> int:
        """
        Get a uniform sample within the range of the parameter.
        """

        minimum = self.parameter_range[0]
        maximum = self.parameter_range[1]

        return random.randint(minimum, maximum)

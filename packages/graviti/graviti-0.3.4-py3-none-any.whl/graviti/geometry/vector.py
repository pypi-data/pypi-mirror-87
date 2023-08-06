#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Basic, Vector, Vector2D and Vector3D.
"""

from typing import Dict, Optional, Sequence, Tuple, Type, TypeVar, Union

from ..utility import UserSequence

T = TypeVar("T", bound="Vector")  # pylint: disable=invalid-name


class Vector(UserSequence[float]):
    """A class used as base class of Vector2D and Vector3D, extending the :class `Sequence`.

    :param args: Coordinates of the vector
    :param loads: A dicitionary containing coordinates of a vector
    :param kwargs: float
        vector2d = Vector(x=1, y=2)
        vector3d = Vector(x=1, y=2, z=3)
    :raises ValueError: When the dimension of the input parameters is not correct
    :return: The created Vector2D or Vector3D class
    """

    _DIMENSION: Optional[int] = None

    _data: Tuple[float, ...]

    def __new__(
        cls: Type[T],
        *args: Union[None, float, Sequence[float]],
        loads: Optional[Dict[str, float]] = None,
        **kwargs: float,
    ) -> T:
        data = cls._process_args(*args, loads=loads, **kwargs)

        ReturnType: Type["Vector"] = cls
        if len(data) == Vector2D._DIMENSION:
            ReturnType = Vector2D
        elif len(data) == Vector3D._DIMENSION:
            ReturnType = Vector3D
        else:
            raise ValueError("Require 2 or 3 dimensional data to construct a Vector.")

        obj: T = object.__new__(ReturnType)
        obj._data = data
        return obj

    def __repr__(self) -> str:
        """Returns the representation of the vector.

        :returns: Vector representation in str
        """
        return f"{self.__class__.__name__}{self._data}"

    def __add__(self, other: Sequence[float]) -> T:
        """Calculate the sum of vector and other sequence.

        :raises ValueError: When the vectors to be added have different dimensions
        :returns: The sum vector of adding two vectors
        """
        if not isinstance(other, Sequence):  # pylint: disable=W1116
            return NotImplemented

        if len(self._data) != len(other):
            raise ValueError("Vectors to be added must have the same dimension")
        result: T = object.__new__(self.__class__)
        result._data = tuple(i + j for i, j in zip(self._data, other))
        return result

    def __radd__(self, other: Sequence[float]) -> T:
        """Calculate the sum of other sequence and the vector.

        :returns: The sum vector of adding two vectors
        """
        return self.__add__(other)

    def __neg__(self) -> T:
        result: T = object.__new__(self.__class__)
        result._data = tuple(-coordinate for coordinate in self._data)
        return result

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._data.__eq__(other._data)

        return False

    @staticmethod
    def _process_args(
        *args: Union[None, float, Sequence[float]],
        loads: Optional[Dict[str, float]] = None,
        **kwargs: float,
    ) -> Tuple[float, ...]:
        if loads:
            kwargs = loads

        if kwargs:
            if "z" in kwargs:
                return (kwargs["x"], kwargs["y"], kwargs["z"])
            return (kwargs["x"], kwargs["y"])

        data: Optional[Sequence[float]]
        data = args[0] if len(args) == 1 else args  # type: ignore[assignment]
        if not data:
            return ()

        try:
            return tuple(data)
        except TypeError as error:
            raise TypeError("Require 2 or 3 dimensional data to construct a vector.") from error


class Vector2D(Vector):
    """A class used to represent 2D vector extending the :class `Vector`."""

    _DIMENSION = 2

    def __new__(
        cls,
        *args: Union[None, float, Sequence[float]],
        loads: Optional[Dict[str, float]] = None,
        **kwargs: float,
    ) -> "Vector2D":
        obj: "Vector2D" = object.__new__(cls)
        if loads:
            kwargs = loads
        if kwargs:
            obj._data = (kwargs["x"], kwargs["y"])
            return obj

        data: Optional[Sequence[float]]
        data = args[0] if len(args) == 1 else args  # type: ignore[assignment]
        if not data:
            obj._data = (0.0, 0.0)
            return obj

        try:
            x, y = data  # pylint: disable=invalid-name
            obj._data = (x, y)
            return obj
        except (ValueError, TypeError) as error:
            raise TypeError(
                f"Require {cls._DIMENSION} dimensional data to construct {cls.__name__}."
            ) from error

    @property
    def x(self) -> float:  # pylint: disable=invalid-name
        """Returns the x coordinate of the vector.

        :return: x coordinate in float type
        """
        return self._data[0]

    @property
    def y(self) -> float:  # pylint: disable=invalid-name

        """Returns the y coordinate of the vector.

        :return: y coordinate in float type
        """
        return self._data[1]

    def dumps(self) -> Dict[str, float]:
        """Dumps the vector as a dictionary.

        :return: A dictionary containing the vector coordinate.
        """
        return {"x": self._data[0], "y": self._data[1]}


class Vector3D(Vector):
    """A class used to represent 3D vector extending the :class `Vector`."""

    _DIMENSION = 3

    def __new__(
        cls,
        *args: Union[None, float, Sequence[float]],
        loads: Optional[Dict[str, float]] = None,
        **kwargs: float,
    ) -> "Vector3D":
        obj: "Vector3D" = object.__new__(cls)
        if loads:
            kwargs = loads
        if kwargs:
            obj._data = (kwargs["x"], kwargs["y"], kwargs["z"])
            return obj

        data: Optional[Sequence[float]]
        data = args[0] if len(args) == 1 else args  # type: ignore[assignment]
        if not data:
            obj._data = (0.0, 0.0, 0.0)
            return obj

        try:
            x, y, z = data  # pylint: disable=invalid-name
            obj._data = (x, y, z)
            return obj
        except (ValueError, TypeError) as error:
            raise TypeError(
                f"Require {cls._DIMENSION} dimensional data to construct {cls.__name__}."
            ) from error

    @property
    def x(self) -> float:  # pylint: disable=invalid-name

        """Returns the x coordinate of the vector.

        :return: x coordinate in float type
        """
        return self._data[0]

    @property
    def y(self) -> float:  # pylint: disable=invalid-name

        """Returns the y coordinate of the vector.

        :return: y coordinate in float type
        """
        return self._data[1]

    @property
    def z(self) -> float:  # pylint: disable=invalid-name

        """Returns the z coordinate of the vector.

        :return: z coordinate in float type
        """
        return self._data[2]

    def dumps(self) -> Dict[str, float]:
        """Dumps the vector as a dictionary.

        :return: A dictionary containing the vector coordinate.
        """
        return {"x": self._data[0], "y": self._data[1], "z": self._data[2]}

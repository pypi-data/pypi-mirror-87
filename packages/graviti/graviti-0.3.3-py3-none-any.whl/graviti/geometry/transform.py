#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Transform3D.
"""

from typing import Dict, Optional, Sequence, Type, TypeVar, Union, overload

import numpy as np

from .quaternion import Quaternion
from .vector import Vector3D

T = TypeVar("T", bound="Transform3D")  # pylint: disable=invalid-name


class Transform3D:
    """A class used to represent a transformation in 3D.

    :param transform: A Transform3D object or a 4x4 or 3x4 transfrom matrix
    :param translation: Translation in a sequence of [x, y, z]
    :param rotation: Rotation in a sequence of [w, x, y, z] or 3x3 rotation matrix or Quaternion
    :param loads: A dictionary containing the translation and the rotation
    :param kwargs: Other parameters to initialize rotation of the transform
    :raises ValueError: When the shape of the input matrix is wrong
    """

    MatrixType = Union[None, Sequence[Sequence[float]], np.ndarray]
    TransformType = Union[None, "Transform3D", Sequence[Sequence[float]], np.ndarray]

    def __init__(
        self,
        transform: TransformType = None,
        *,
        translation: Optional[Sequence[float]] = None,
        rotation: Quaternion.ArgsType = None,
        loads: Optional[Dict[str, Dict[str, float]]] = None,
        **kwargs: Quaternion.KwargsType,
    ) -> None:
        if loads:
            self._translation = Vector3D(loads=loads["translation"])
            self._rotation = Quaternion(loads=loads["rotation"])
            return

        if transform is not None:
            if isinstance(transform, Transform3D):
                self._translation = transform.translation
                self._rotation = transform.rotation
                return

            if isinstance(transform, Sequence):  # pylint: disable=W1116
                transform = np.array(transform)
            if transform.shape != (3, 4) and transform.shape != (4, 4):
                raise ValueError("The shape of input transform matrix must be 3x4 or 4x4.")

            self._translation = Vector3D(transform[0, 3], transform[1, 3], transform[2, 3])
            self._rotation = Quaternion(transform)
            return

        self._translation = Vector3D(translation)
        self._rotation = Quaternion(rotation, loads=None, **kwargs)

    def dumps(self) -> Dict[str, Dict[str, float]]:
        """Dumps the 3D transform as a dictionary.

        :return: A dictionary containing rotation and translation information of the transform3D
        """
        return {
            "translation": self._translation.dumps(),
            "rotation": self._rotation.dumps(),
        }

    @overload
    def __mul__(self: T, other: T) -> T:
        ...

    @overload
    def __mul__(self: T, other: Quaternion) -> T:
        ...

    @overload
    def __mul__(self: T, other: Sequence[float]) -> Vector3D:
        ...

    def __mul__(self: T, other: Union[T, Quaternion, Sequence[float]]) -> Union[T, Vector3D]:

        if isinstance(other, Sequence):  # pylint: disable=W1116
            return self._translation + self._rotation.rotate(other)

        if isinstance(other, Quaternion):
            return self._create(self._translation, self._rotation * other)

        if isinstance(other, Transform3D):
            return self._create(self * other.translation, self._rotation * other.rotation)

        return NotImplemented  # type: ignore[unreachable]

    def __rmul__(self: T, other: Quaternion) -> T:
        if isinstance(other, Quaternion):
            return self._create(other * self._translation, other * self._rotation)

        return NotImplemented  # type: ignore[unreachable]

    def __repr__(self) -> str:
        translation = self._translation
        rotation = self._rotation
        return (
            f"{self.__class__.__name__}("
            f"\n  Translation({translation.x}, {translation.y}, {translation.z}),"
            f"\n  Rotation({rotation.w}, {rotation.x}, {rotation.y}, {rotation.z}),"
            "\n)"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            return self._translation.__eq__(other.translation) and self._rotation == other.rotation

        return False

    @property
    def translation(self) -> Vector3D:
        """Returns translation of the 3D transform.

        :return: Translation in Vector3D
        """
        return self._translation

    def set_translation(self, *args: Union[float, Sequence[float]], **kwargs: float) -> None:
        """Set the translation of the transform.

        :param args: Coordinates of the translation vector
        :param kwargs: keyword-only argument to set different dimension for translation vector
            transform.set_translation(x=1, y=2, z=3)
        """
        self._translation = Vector3D(*args, loads=None, **kwargs)

    @property
    def rotation(self) -> Quaternion:
        """Returns rotation of the 3D transform.

        :return: rotation in Quaternion
        """
        return self._rotation

    def set_rotation(
        self,
        *args: Union[Quaternion.ArgsType, float],
        **kwargs: Quaternion.KwargsType,
    ) -> None:
        """Set the rotation of the transform.

        :param args: Coordinates of the Quaternion
        :param kwargs: keyword-only argument to the Quaternion
        """
        self._rotation = Quaternion(*args, loads=None, **kwargs)

    def as_matrix(self) -> np.ndarray:
        """Return the transform as a 4x4 transform matrix.

        :return: A 4x4 numpy array representing the transform matrix
        """
        matrix = np.eye(4)
        matrix[:3, 3] = self._translation
        matrix[:3, :3] = self._rotation.as_matrix()
        return matrix

    def inverse(self: T) -> T:
        """Return the inverse of the transform.

        :return: A Transform3D object representing the inverse of this Transform3D
        """
        rotation = self._rotation.inverse()
        translation = rotation.rotate(-self._translation)
        return self._create(translation, rotation)

    @classmethod
    def _create(cls: Type[T], translation: Vector3D, rotation: Quaternion) -> T:
        transform: T = object.__new__(cls)
        transform._translation = translation  # pylint: disable=protected-access
        transform._rotation = rotation  # pylint: disable=protected-access
        return transform

#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Box2D, Box3D"""

from typing import Dict, List, Optional, Sequence, TypeVar, Union

from ..utility import UserSequence
from .quaternion import Quaternion
from .transform import Transform3D
from .vector import Vector2D, Vector3D

T = TypeVar("T", bound="Box3D")  # pylint: disable=invalid-name


class Box2D(UserSequence[float]):
    """Contain the definition of 2D bounding box and some related operations.

    :param args: Union[None, float, Sequence[float]],
        box = Box2D()
        box = Box2D(10, 20, 30, 40)
        box = Box2D([10, 20, 30, 40])
    :param loads: [
        {
            "x": ...
            "y": ...
        },
        {
            "x": ...
            "y": ...
        }
    ]
    :param x: X coordinate of the top left vertex of the box
    :param y: Y coordinate of the top left vertex of the box
    :param width: Length along the x axis
    :param height: Length along the y axis
    :raise TypeError: When input params do not meet the requirement
    """

    _LENGTH = 4

    def __init__(
        self,
        *args: Union[None, float, Sequence[float]],
        loads: Optional[List[Dict[str, float]]] = None,
        x: Optional[float] = None,
        y: Optional[float] = None,
        width: Optional[float] = None,
        height: Optional[float] = None,
    ) -> None:
        # pylint: disable=invalid-name

        if loads:
            xmin, ymin = loads[0]["x"], loads[0]["y"]
            xmax, ymax = loads[1]["x"], loads[1]["y"]

        elif x is not None or y is not None or width is not None or height is not None:
            try:
                xmin, ymin = x, y  # type: ignore[assignment]
                xmax, ymax = x + width, y + height  # type: ignore[operator]
            except TypeError as error:
                raise TypeError(
                    "Require x, y, width, height keyword arguments to construct a 2D box."
                ) from error

        else:
            arg: Optional[Sequence[float]]
            arg = args[0] if len(args) == 1 else args  # type: ignore[assignment]
            if arg is None:
                self._data = (0.0,) * Box2D._LENGTH
                return

            try:
                xmin, ymin, xmax, ymax = arg
            except (ValueError, TypeError) as error:
                raise TypeError(
                    f"Require 4 dimensional data to construct {self.__class__.__name__}."
                ) from error

        if xmin >= xmax or ymin >= ymax:
            self._data = (0.0,) * Box2D._LENGTH
        else:
            self._data = (xmin, ymin, xmax, ymax)

    def dumps(self) -> List[Dict[str, float]]:
        """Dump a 2D box as a list.

        :return: a list containing vertex coordinates of the box
        """
        return [{"x": self._data[0], "y": self._data[1]}, {"x": self._data[2], "y": self._data[3]}]

    def __repr__(self) -> str:
        """Print as Box2D(x1, y1, x2, y2)

        :return: a string like "Box2D(x1, y1, x2, y2)"
        """
        return f"{self.__class__.__name__}{self._data}"

    def __and__(self, other: "Box2D") -> "Box2D":
        """Calculate the intersect box of two boxes.

        :param other: the other box
        :return: the intersect box of the two boxes
        """
        # pylint: disable=invalid-name
        x1 = max(self._data[0], other._data[0])
        y1 = max(self._data[1], other._data[1])
        x2 = min(self._data[2], other._data[2])
        y2 = min(self._data[3], other._data[3])
        return Box2D(x1, y1, x2, y2)

    def __len__(self) -> int:
        return Box2D._LENGTH

    @property
    def xmin(self) -> float:
        """Get the minimum x coordinate.

        :return: minimum x coordinate
        """
        return self._data[0]

    @property
    def ymin(self) -> float:
        """Get the minimum y coordinate.

        :return: minimum y coordinate
        """
        return self._data[1]

    @property
    def xmax(self) -> float:
        """Get the maximum x coordinate.

        :return: maximum x coordinate
        """
        return self._data[2]

    @property
    def ymax(self) -> float:
        """Get the maximum y coordinate.

        :return: maximum y coordinate
        """
        return self._data[3]

    @property
    def tl(self) -> Vector2D:  # pylint: disable=invalid-name
        """Get the top left point.

        :return: the top left point
        """
        return Vector2D(self._data[:2])

    @property
    def br(self) -> Vector2D:  # pylint: disable=invalid-name
        """Get the bottom right point.

        :return: the bottom right point
        """
        return Vector2D(self._data[2:])

    @property
    def width(self) -> float:
        """Get the width of the 2d box"""
        return self._data[2] - self._data[0]

    @property
    def height(self) -> float:
        """Get the height of the 2d box"""
        return self._data[3] - self._data[1]

    def area(self) -> float:
        """Get the area of the 2d box"""
        return self.width * self.height

    @staticmethod
    def iou(box1: "Box2D", box2: "Box2D") -> float:
        """Calculate the intersection over union of two 2d boxes.

        :param box1: a 2d box
        :param box2: a 2d box
        :return: intersection over union between the two input boxes
        """
        area1 = box1.area()
        area2 = box2.area()
        intersect_box = box1 & box2
        intersect = intersect_box.area()
        union = area1 + area2 - intersect
        return intersect / union


class Box3D:
    """Contain the definition of 3D bounding box and some related operations.

    :param transform: A Transform3D object or a 4x4 or 3x4 transfrom matrix
    :param translation: Translation in a sequence of [x, y, z]
    :param rotation: Rotation in a sequence of [w, x, y, z] or 3x3 rotation matrix or `Quaternion`
    :param size: Size in a sequence of [x, y, z]
    :param loads: {
        "translation": {
            "x": ...
            "y": ...
            "z": ...
        },
        "rotation": {
            "w": ...
            "x": ...
            "y": ...
            "z": ...
        },
        "size": {
            "x": ...
            "y": ...
            "z": ...
        }
    }
    :param kwargs: Other parameters to initialize rotation of the transform
    """

    def __init__(
        self,
        transform: Transform3D.TransformType = None,
        *,
        translation: Optional[Sequence[float]] = None,
        rotation: Quaternion.ArgsType = None,
        size: Optional[Sequence[float]] = None,
        loads: Optional[Dict[str, Dict[str, float]]] = None,
        **kwargs: Quaternion.KwargsType,
    ) -> None:
        if loads:
            self._size = Vector3D(loads=loads["size"])
            self._transform = Transform3D(loads=loads)
            return

        self._transform = Transform3D(
            transform, translation=translation, rotation=rotation, loads=None, **kwargs
        )
        self._size = Vector3D(size)

    def dumps(self) -> Dict[str, Dict[str, float]]:
        """Dump the 3d box as a dictionary.

        :return: a dictionary containing translation, rotation and size info
        """
        box3d_dict = self._transform.dumps()
        box3d_dict["size"] = self.size.dumps()
        return box3d_dict

    def __repr__(self) -> str:
        translation = self.translation
        rotation = self.rotation
        size = self.size

        return (
            f"{self.__class__.__name__}("
            f"\n  Translation({translation.x}, {translation.y}, {translation.z}),"
            f"\n  Rotation({rotation.w}, {rotation.x}, {rotation.y}, {rotation.z}),"
            f"\n  Size({size.x}, {size.y}, {size.z}),"
            "\n)"
        )

    def __rmul__(self: T, other: Transform3D) -> T:
        if isinstance(other, Transform3D):
            box: T = object.__new__(self.__class__)
            box._transform = other * self._transform
            box._size = self._size
            return box

        return NotImplemented  # type: ignore[unreachable]

    @property
    def translation(self) -> Vector3D:
        """Get the translation of the 3d box by property."""
        return self._transform.translation

    @property
    def rotation(self) -> Quaternion:
        """Get the rotation of the 3d box by property."""
        return self._transform.rotation

    @property
    def transform(self) -> Transform3D:
        """Get the transform of the 3d box by property."""
        return self._transform

    @property
    def size(self) -> Vector3D:
        """Get the size of the 3d box by property."""
        return self._size

    def volume(self) -> float:
        """Get the volume of the 3d box."""
        return self.size.x * self.size.y * self.size.z

    @classmethod
    def iou(cls, box1: "Box3D", box2: "Box3D", angle_threshold: float = 5) -> float:
        """Calculate the iou between two 3d boxes.

        :param box1: a 3d box
        :param box2: a 3d box
        :param angle_threshold: the threshold of the relative angles between two input 3d boxes,
        in degree
        :return: the iou of the two 3d boxes
        """
        box2 = box1.transform.inverse() * box2
        if abs(box2.rotation.degrees) > angle_threshold:
            return 0

        intersect_size = [
            cls._line_intersect(*args) for args in zip(box1.size, box2.size, box2.translation)
        ]
        intersect = intersect_size[0] * intersect_size[1] * intersect_size[2]
        union = box1.volume() + box2.volume() - intersect
        return intersect / union

    @staticmethod
    def _line_intersect(length1: float, length2: float, midpoint_distance: float) -> float:
        """Calculate the intersect length between two parallel lines.

        :param length1: the length of line1
        :param length2: the length of line2
        :param midpoint_distance: the distance between midpoints of the two lines
        :return: the intersect length between line1 and line2
        """
        line1_min = -length1 / 2
        line1_max = length1 / 2
        line2_min = -length2 / 2 + midpoint_distance
        line2_max = length2 / 2 + midpoint_distance
        intersect_length = min(line1_max, line2_max) - max(line1_min, line2_min)
        return intersect_length if intersect_length > 0 else 0

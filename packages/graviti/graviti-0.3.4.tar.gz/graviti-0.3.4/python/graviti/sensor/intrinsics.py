#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class CameraMatrix, DistortionCoefficients, CameraIntrinsics.
"""

import math
from typing import Dict, Generator, Iterator, Mapping, Optional, Sequence, Tuple

import numpy as np

from ..geometry import Vector2D


class CameraMatrix:
    """A class representing camera matrix.

    :param matrix: A 3x3 Sequence of camera matrix
    :param loads: A dict containing parameters of camera matrix
    :param kwargs: Float values which keys must be "fx", "fy", "cx", "cy" and "skew"(optional)
    :raises KeyError: When essential keys are missing in param loads
    :raises TypeError: When kwargs do not have correct keys and only param kwargs is provided
    """

    def __init__(
        self,
        matrix: Optional[Sequence[Sequence[float]]] = None,
        *,
        loads: Optional[Dict[str, float]] = None,
        **kwargs: float,
    ) -> None:
        if loads:
            kwargs = loads

        if kwargs:
            try:
                self._fx = kwargs["fx"]
                self._fy = kwargs["fy"]
                self._cx = kwargs["cx"]
                self._cy = kwargs["cy"]
                self._skew = kwargs.get("skew", 0)
                return
            except KeyError as error:
                if loads:
                    raise
                if matrix is None:
                    raise TypeError(
                        f"Missing key {error} in kwargs to initialize {self.__class__.__name__}"
                    )

        if matrix is not None:
            self._fx = matrix[0][0]
            self._fy = matrix[1][1]
            self._cx = matrix[0][2]
            self._cy = matrix[1][2]
            self._skew = matrix[0][1]
            return

        raise TypeError(f"Require 'fx', 'fy', 'cx', 'cy' to initialize {self.__class__.__name__}")

    def dumps(self) -> Dict[str, float]:
        """Dumps the camera matrix into a dict."""
        return {
            "fx": self._fx,
            "fy": self._fy,
            "cx": self._cx,
            "cy": self._cy,
            "skew": self._skew,
        }

    def __repr__(self) -> str:
        str_list = [
            f"{self.__class__.__name__}(",
            f"  fx={self._fx},",
            f"  fy={self._fy},",
            f"  cx={self._cx},",
            f"  cy={self._cy},",
        ]
        if self._skew:
            str_list.append(f"  skew={self._skew},")
        str_list.append(")")
        return "\n".join(str_list)

    @property
    def fx(self) -> float:  # pylint: disable=invalid-name
        """Get the fx of the camera matrix."""
        return self._fx

    @property
    def fy(self) -> float:  # pylint: disable=invalid-name
        """Get the fy of the camera matrix."""
        return self._fy

    @property
    def cx(self) -> float:  # pylint: disable=invalid-name
        """Get the cx of the camera matrix."""
        return self._cx

    @property
    def cy(self) -> float:  # pylint: disable=invalid-name
        """Get the cy of the camera matrix."""
        return self._cy

    @property
    def skew(self) -> float:
        """Get the skew of the camera matrix."""
        return self._skew

    def as_matrix(self) -> np.ndarray:
        """Returns camera matrix as a 3x3 matrix.

        :return: A 3x3 numpy array representing the camera matrix
        """
        return np.array(
            [
                [self._fx, self._skew, self._cx],
                [0.0, self._cy, self._cy],
                [0.0, 0.0, 1.0],
            ]
        )

    def project(self, point: Sequence[float]) -> Vector2D:
        """Project a point to the pixel coordinate.

        :param point: A Sequence containing coordinates of the point to be projected
        :raises TypeError: When the dimension of input point is not two or three
        """
        # pylint: disable=invalid-name
        if len(point) == 3:
            x = point[0] / point[2]
            y = point[1] / point[2]
        elif len(point) == 2:
            x = point[0]
            y = point[1]
        else:
            raise TypeError("The point to be projected must have 2 or 3 dimension")

        x = self._fx * x + self._skew * y + self._cx
        y = self._fy * y + self._cy
        return Vector2D(x, y)


class DistortionCoefficients(Mapping[str, float]):
    """A class representing camera distortion coefficients.

    :param loads: A dict containig distortion coefficients of a camera
    :param kwargs: Float values which keys must be k1, k2, ... and p1, p2, ...
    """

    _FISHEYE_MINIMUM_R = 1e-8

    def __init__(self, *, loads: Optional[Dict[str, float]] = None, **kwargs: float) -> None:
        self._data: Dict[str, float] = {}
        if loads:
            kwargs = loads

        self._data.update(dict(self._distortion_generator("p", kwargs)))
        self._data.update(dict(self._distortion_generator("k", kwargs)))

        if not self._data:
            raise TypeError(
                f"Require tangential or radial distortion to initialize {self.__class__.__name__}"
            )

    def __repr__(self) -> str:
        str_list = [f"{self.__class__.__name__}{{"]
        for key, value in self._data.items():
            str_list.append(f'  "{key}": {value},')
        str_list.append("}")
        return "\n".join(str_list)

    def __getitem__(self, key: str) -> float:
        return self._data.__getitem__(key)

    def __len__(self) -> int:
        return self._data.__len__()

    def __iter__(self) -> Iterator[str]:
        return self._data.__iter__()

    def dumps(self) -> Dict[str, float]:
        """Dumps the distortion coefficients into a dict.

        :return: A dict containing all the camera distortion coefficients
        """
        return self._data.copy()

    def distort(self, point: Sequence[float], is_fisheye: bool = False) -> Vector2D:
        """Add distortion a point.

        :param point: A Sequence containing coordinates of the point to be distorted
        :raises TypeError: When the dimension of input point is not two or three
        :return: Distorted 2D point
        """
        # pylint: disable=invalid-name
        if len(point) == 3:
            x = point[0] / point[2]
            y = point[1] / point[2]
        elif len(point) == 2:
            x = point[0]
            y = point[1]
        else:
            raise TypeError("The point to be projected must have 2 or 3 dimension")

        x2 = x ** 2
        y2 = y ** 2
        xy2 = 2 * x * y
        r2 = x2 + y2

        radial_distortion = self._calculate_radial_distortion(r2, is_fisheye)
        tangential_distortion = self._calculate_tangential_distortion(r2, x2, y2, xy2, is_fisheye)
        x = x * radial_distortion + tangential_distortion[0]
        y = y * radial_distortion + tangential_distortion[1]
        return Vector2D(x, y)

    def _calculate_radial_distortion(self, r2: float, is_fisheye: bool = False) -> float:
        # pylint: disable=invalid-name
        if is_fisheye:
            r = math.sqrt(r2)
            factor = math.atan(r)
            factor2 = factor ** 2
        else:
            factor2 = r2

        radial_distortion = 1.0
        for i, (_, value) in enumerate(self._distortion_generator("k", self._data), 1):
            radial_distortion += value * factor2 ** i

        if is_fisheye:
            radial_distortion = radial_distortion * factor / r if r > self._FISHEYE_MINIMUM_R else 1
        return radial_distortion

    def _calculate_tangential_distortion(  # pylint: disable=too-many-arguments
        self, r2: float, x2: float, y2: float, xy2: float, is_fisheye: bool
    ) -> Tuple[float, float]:
        # pylint: disable=invalid-name
        if is_fisheye:
            return (0, 0)

        p1 = self._data["p1"]
        p2 = self._data["p2"]
        return (p1 * xy2 + p2 * (r2 + 2 * x2), p1 * (r2 + 2 * y2) + p2 * xy2)

    @staticmethod
    def _distortion_generator(
        distortion_keyword: str, data: Dict[str, float]
    ) -> Generator[Tuple[str, float], None, None]:
        for index in range(1, len(data) + 1):
            key = f"{distortion_keyword}{index}"
            if key not in data:
                break
            yield (key, data[key])


class CameraIntrinsics:
    """A class representing camera intrinsics including camera matrix and distortion coeffecients.

    :param camera_matrix: A 3x3 Sequence of camera matrix
    :param loads: A dictionary containig 'cameraMatrix' and 'distortionCoefficients'
    :param kwargs: Float values to initialize CameraMatrix and DistortionCoefficients
    """

    def __init__(
        self,
        camera_matrix: Optional[Sequence[Sequence[float]]] = None,
        *,
        loads: Optional[Dict[str, Dict[str, float]]] = None,
        _init_distortion: bool = True,
        **kwargs: float,
    ) -> None:
        if loads:
            self._camera_matrix = CameraMatrix(loads=loads["cameraMatrix"])
            if "distortionCoefficients" not in loads:
                self._distortion_coefficients = None
            else:
                self._distortion_coefficients = DistortionCoefficients(
                    loads=loads["distortionCoefficients"]
                )
            return

        self._camera_matrix = CameraMatrix(camera_matrix, loads=None, **kwargs)
        if kwargs and _init_distortion:
            try:
                self._distortion_coefficients = DistortionCoefficients(loads=None, **kwargs)
                return
            except TypeError:
                pass
        self._distortion_coefficients = None

    def dumps(self) -> Dict[str, Dict[str, float]]:
        """Dumps the camera intrinsics into a dictionary."""
        data = {"cameraMatrix": self._camera_matrix.dumps()}
        if self._distortion_coefficients:
            data["distortionCoefficients"] = self._distortion_coefficients.dumps()

        return data

    def __repr__(self) -> str:
        str_list = [
            f"{self.__class__.__name__}(",
            "  CameraMatrix(",
            f"    fx={self._camera_matrix.fx},",
            f"    fy={self._camera_matrix.fy},",
            f"    cx={self._camera_matrix.cx},",
            f"    cy={self._camera_matrix.cy},",
        ]
        if self._camera_matrix.skew:
            str_list.append(f"    skew={self._camera_matrix.skew},")
        str_list.append("  )")

        if self._distortion_coefficients:
            str_list.append("  DistortionCoefficients{")
            for key, value in self._distortion_coefficients.items():  # pylint: disable=no-member
                str_list.append(f'    "{key}": {value},')
            str_list.append("  }")

        str_list.append(")")
        return "\n".join(str_list)

    @property
    def camera_matrix(self) -> CameraMatrix:
        """Get the camera matrix of camera intrinsics.

        :return: CameraMatrix class object containing fx, fy, cx, cy, skew(optional)
        """
        return self._camera_matrix

    @property
    def distortion_coefficients(self) -> Optional[DistortionCoefficients]:
        """Get the distortion coefficients of camera intrinsics, could be None.

        :return: DistortionCoefficients class object
                containing tangential and radial distortion coefficients
        """
        return self._distortion_coefficients

    def set_camera_matrix(
        self,
        matrix: Optional[Sequence[Sequence[float]]] = None,
        **kwargs: float,
    ) -> None:
        """Set camera matrix of camera intrinsics.

        :param matrix: Camera matrix in 3x3 sequence
        :param kwargs: Keyword arguments containing fx, fy, cx, cy, skew(optional)
        """
        self._camera_matrix = CameraMatrix(matrix=matrix, loads=None, **kwargs)

    def set_distortion_coefficients(self, **kwargs: float) -> None:
        """Set distortion coefficients of camera intrinsics.

        :param kwargs: Keyword arguments containing p1, p2, ..., k1, k2, ...
        """
        self._distortion_coefficients = DistortionCoefficients(loads=None, **kwargs)

    def project(self, point: Sequence[float], is_fisheye: bool = False) -> Vector2D:
        """Project a point to the pixel coordinate,
           before that distort the point if ditortion coefficients are provided.

        :param point: A Sequence containing coordinates of the point to be projected
        :return: The coordinate on the pixel plane where the point is projected to
        """
        if self._distortion_coefficients:
            point = self._distortion_coefficients.distort(point, is_fisheye)
        return self._camera_matrix.project(point)

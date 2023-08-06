#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains location of each sections in the dataset."""

from ..label.label import LabelType


class SegmentLocation:
    """This class defines the location of segment in dataset(either Dataset or FusionDataset).

    :param segment_index: Segment index
    """

    def __init__(
        self,
        segment_index: int,
    ) -> None:
        self._segment_index = segment_index

    @property
    def segment_index(self) -> int:
        """Return index of segment in the dataset(either Dataset or FusionDataset).

        :return: index of segment in the dataset(either Dataset or FusionDataset)
        """
        return self._segment_index

    def __str__(self) -> str:
        return f"Segment_index: '{self._segment_index}', "


class DataLocationForDataset(SegmentLocation):
    """This class defines the location of data in dataset(Dataset).

    :param segment_index: index of segment in dataset(Dataset)
    :param data_index: index of data in segment(Dataset)
    """

    def __init__(
        self,
        segment_index: int,
        data_index: int,
    ) -> None:
        super().__init__(segment_index)
        self._data_index = data_index

    @property
    def data_index(self) -> int:
        """Return index of data in segment.

        :return: index of data in segment
        """
        return self._data_index

    def __str__(self) -> str:
        return f"Segment_index: '{self._segment_index}', " f"Data_index: '{self._data_index}', "


class DataLocationForFusionDataset(SegmentLocation):
    """This class defines the location of data in dataset(FusionDataset).

    :param segment_index: index of segment in dataset(FusionDataset)
    :param frame_index: index of frame in segment
    :param sensor_name: name of sensor in segment
    """

    def __init__(
        self,
        segment_index: int,
        frame_index: int,
        sensor_name: str,
    ) -> None:
        super().__init__(segment_index)
        self._frame_index = frame_index
        self._sensor_name = sensor_name

    @property
    def frame_index(self) -> int:
        """Return index of frame in segment.

        :return: index of frame in segment
        """
        return self._frame_index

    @property
    def sensor_name(self) -> str:
        """Return name of sensor in segment.

        :return: name of sensor in segment
        """
        return self._sensor_name

    def __str__(self) -> str:
        return (
            f"Segment_index: '{self._segment_index}', "
            f"Frame_index: '{self._frame_index}', "
            f"Sensor_name: '{self._sensor_name}', "
        )


class LabelLocation:
    """This class defines the location of label in data(either Dataset or FusionDataset).

    :param label_type: label type of data
    :param label_index: index of label in for each type of label
    """

    def __init__(
        self,
        label_type: LabelType,
        label_index: int,
    ) -> None:
        self._label_type = label_type
        self._label_index = label_index

    @property
    def label_type(self) -> LabelType:
        """Return label type of data.

        :return: label type of data
        """
        return self._label_type

    @property
    def label_index(self) -> int:
        """Return index of label in for each type of label.

        :return: index of label in for each type of label
        """
        return self._label_index

    def __str__(self) -> str:
        return f"Segment_index: '{self._label_type}', Frame_index: '{self._label_index}', "

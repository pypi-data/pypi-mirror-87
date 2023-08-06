# !/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""SegmentNameWrapper class for manage the path of the segment object."""


from pathlib import PurePosixPath


class SegmentNameWrapper:
    """SegmentPath class to handle segment path from tensorbay,
    provides functions to convert remote_path and object_path.

    :param segment_name: The name of the segment
    """

    _DEFAULT_SEGMENT_NAME = "_default"
    _PATH_PREFIX: str = ".segment/"
    _PATH_SUFFIX: str = "/.segment_end"

    def __init__(self, segment_name: str) -> None:
        if not segment_name:
            self._segment_prefix = ""
            self._post_segment_name = SegmentNameWrapper._DEFAULT_SEGMENT_NAME
        else:
            self._segment_prefix = (
                SegmentNameWrapper._PATH_PREFIX + segment_name + SegmentNameWrapper._PATH_SUFFIX
            )
            self._post_segment_name = segment_name

    def get_object_path(self, remote_path: str, sensor_name: str = "") -> str:
        """Convert remote_path to object_path

        :param remote_path: The remote_path of the data
        :param sensor_name: The name of the of the data sensor
        :return: The object_path convert from input remote_path
        """
        if not self._segment_prefix and not sensor_name:
            return remote_path

        return str(PurePosixPath(self._segment_prefix, sensor_name, remote_path))

    def get_remote_path(self, object_path: str, sensor_name: str = "") -> str:
        """Convert object_path to remote_path

        :param object_path: The object_path of the data
        :param sensor_name: The name of the of the data sensor
        :return: The remote_path convert from input object_path
        """
        if not self._segment_prefix and not sensor_name:
            return object_path

        header = PurePosixPath(self._segment_prefix, sensor_name)
        return object_path[len(str(header)) + 1 :]

    @property
    def post_segment_name(self) -> str:
        """Get to post segment name of current segment

        :return: The post segment name
        """
        return self._post_segment_name

    @staticmethod
    def get_local_segment_name(name: str) -> str:
        """Convert post segment name to local segment name

        :param name: The post segment name
        :return: The local segment name
        """
        return name if name != SegmentNameWrapper._DEFAULT_SEGMENT_NAME else ""

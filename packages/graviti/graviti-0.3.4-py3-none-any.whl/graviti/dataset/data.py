#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class Data"""

import os
from http.client import HTTPResponse
from typing import Any, Callable, Dict, List, Optional, Union, overload
from urllib.request import urlopen

from _io import BufferedReader
from typing_extensions import Literal

from ..label import (
    Classification,
    Label,
    LabeledBox2D,
    LabeledBox3D,
    LabeledPolygon2D,
    LabeledPolyline2D,
    LabeledSentence,
    LabelType,
)
from ..utility import TBRN, UserMapping

Labels = Union[
    Classification,
    List[LabeledBox2D],
    List[LabeledBox3D],
    List[LabeledPolygon2D],
    List[LabeledPolyline2D],
    List[LabeledSentence],
]


class Data(UserMapping[LabelType, Labels]):
    """this class defines the concept of labels to one file

    :param fileuri: the file path of the labeled object in this data
    :param timestamp: the timestamp when collecting the labeled object in this data
    :param loads: {
        "fileuri": <str>,
        "timestamp": <float>,
        "labels_classification": {...},
        "labels_box2D": {...},
        "labels_box3D": {...},
        "labels_polygon": {...},
        "labels_polyline": {...},
        "labels_sentence": {...},
    }
    :TypeError: when fileuri is not given
    """

    def __init__(
        self,
        fileuri: Union[str, TBRN, None] = None,
        *,
        remote_path: Optional[str] = None,
        timestamp: Optional[float] = None,
        url_getter: Optional[Callable[[TBRN], str]] = None,
        loads: Optional[Dict[str, Any]] = None,
    ) -> None:

        self._data: Dict[LabelType, Any] = {}
        self._remote_path = remote_path  # The remote storage location of the data
        self._url_getter = url_getter

        if loads:
            fileuri = loads["fileuri"]
            timestamp = loads.get("timestamp", None)
            self.load_labels(loads)

        if not fileuri:
            raise TypeError(
                f"{self.__class__.__name__}() missing 1 required positional argument: 'fileuri'"
            )

        if isinstance(fileuri, str) and fileuri.startswith("tb:"):
            fileuri = TBRN(tbrn=fileuri)

        self._fileuri = fileuri

        if timestamp is not None:
            self.timestamp = timestamp

        self._local_path = self._fileuri if isinstance(self._fileuri, str) else ""

    def dumps(self) -> Dict[str, Any]:
        """dump a data into a dict"""

        data_dict: Dict[str, Any] = {}
        data_dict["fileuri"] = str(self._fileuri)
        if hasattr(self, "timestamp"):
            data_dict["timestamp"] = self.timestamp

        data_dict.update(self.dump_labels())

        return data_dict

    def dump_labels(self) -> Dict[str, Any]:
        """dump all labels into a dict"""

        labels_dict: Dict[str, Any] = {}
        for key, labels in self._data.items():
            if key == LabelType.CLASSIFICATION:
                labels_dict[key.value] = labels.dumps()
            else:
                labels_dict[key.value] = [label.dumps() for label in labels]

        return labels_dict

    def load_labels(self, loads: Dict[str, Any]) -> None:
        """load all labels into the data object"""

        for label_type in LabelType:
            if label_type.value not in loads:
                continue

            labels = loads[label_type.value]

            if label_type == LabelType.CLASSIFICATION:
                self._data[label_type] = label_type.type(loads=labels)
            else:
                self._data[label_type] = [label_type.type(loads=label) for label in labels]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}("{self._fileuri}")'

    def get_url(self) -> str:
        """Return the url of the data host by tensorbay

        :return: the url of this data
        :raises ValueError: when the url_getter is missing
        """
        if not self._url_getter:
            raise ValueError(
                f"{self.__repr__()} has no url_getter, it is probably not a remote file"
            )

        return self._url_getter(self.tbrn)

    def open(self) -> Union[BufferedReader, HTTPResponse]:
        """Return binary fp of this file, the file pointer will be get by buildin `open()` for
        local file, by `urllib.request.urlopen()` for remote file

        :return: The file pointer for this data, the retuen class will be `_io.BufferedReader` for
        local file, `http.client.HTTPResponse` for remote file

        """
        if self._local_path:
            return open(self._local_path, "rb")

        return urlopen(self.get_url())

    @property
    def fileuri(self) -> Union[str, TBRN]:
        """Return fileuri of the data.

        :return: fileuri of the data
        """
        return self._fileuri

    @property
    def tbrn(self) -> TBRN:
        """Return timestamp of the data.

        :return: timestamp of the data
        :raises ValueError: when the tbrn is missing
        """
        if not isinstance(self._fileuri, TBRN):
            raise ValueError(f"{self.__repr__()} has no TBRN, it is probably not a remote file")

        return self._fileuri

    @property
    def local_path(self) -> str:
        """Return local path of the data.

        :return: local path of the data
        """
        return self._local_path

    @property
    def remote_path(self) -> str:
        """Get the remote path of the data

        :return: the remote path of the data
        """
        if self._remote_path:
            return self._remote_path

        if isinstance(self._fileuri, TBRN):
            return self._fileuri.remote_path

        return os.path.basename(self._fileuri)

    @remote_path.setter
    def remote_path(self, remote_path: str) -> None:
        """Set the remote path of the data """
        self._remote_path = remote_path

    def register_label(self, label_type: LabelType) -> None:
        """register a label type to data

        :param label_type: the LabelType to register
        """
        if label_type == LabelType.CLASSIFICATION:
            return

        self._data[label_type] = []

    def append_label(self, label: Label) -> None:
        """append a label to labels

        :param label: a Label to append
        :raises TypeError: when the label type of the append label is not registerd
        """

        if label.enum == LabelType.CLASSIFICATION:
            self._data[label.enum] = label
            return

        try:
            self._data[label.enum].append(label)
        except KeyError as error:
            raise TypeError(
                "LabelType needs to be registerd before appending label "
                f"(call register_label(LabelType.{label.enum.name}))"
            ) from error

    @overload
    def __getitem__(self, label_type: Literal[LabelType.CLASSIFICATION]) -> Classification:
        ...

    @overload
    def __getitem__(self, label_type: Literal[LabelType.BOX2D]) -> List[LabeledBox2D]:
        ...

    @overload
    def __getitem__(self, label_type: Literal[LabelType.BOX3D]) -> List[LabeledBox3D]:
        ...

    @overload
    def __getitem__(self, label_type: Literal[LabelType.POLYGON2D]) -> List[LabeledPolygon2D]:
        ...

    @overload
    def __getitem__(self, label_type: Literal[LabelType.POLYLINE2D]) -> List[LabeledPolyline2D]:
        ...

    @overload
    def __getitem__(self, label_type: LabelType) -> Labels:
        ...

    def __getitem__(self, label_type: LabelType) -> Labels:
        """return one type of labels in a data

        :param label_type: required LabelType
        """
        return self._data[label_type]  # type: ignore[no-any-return]

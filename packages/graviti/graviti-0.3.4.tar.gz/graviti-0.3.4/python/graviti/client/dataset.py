#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class DatasetClientBase, DatasetClient, FusionDatasetClient,
SegmentClientBase, SegmentClient, FusionSegmentClient
"""

from typing import List, Optional, Tuple, TypeVar, Union

from ..dataset import Data, Frame, FusionSegment, Segment
from ..label import LabelTables
from ..sensor import Sensor
from ..utility import NameSortedDict
from .contentset import (
    ContentSegmentClient,
    ContentsetClient,
    FusionContentSegmentClient,
    FusionContentsetClient,
)
from .labelset import (
    FusionLabelSegmentClient,
    FusionLabelsetClient,
    LabelSegmentClient,
    LabelsetClient,
    LabelsetClientBase,
)
from .requests import Client

T = TypeVar("T", bound=Sensor)  # pylint: disable=invalid-name


class SegmentClientBase:
    """This class defines the concept of a segment client and some opertions on it.

    :param name: Segment name, unique for a dataset
    :param contentset_name: Dataset name
    :param contentset_id: Dataset id
    :param client: The client used for sending request to TensorBay
    """

    _content_segment_client: Union[ContentSegmentClient, FusionContentSegmentClient]
    _label_segment_client: Union[None, LabelSegmentClient, FusionLabelSegmentClient]

    def __init__(
        self,
        name: str,
        dataset_name: str,
        dataset_id: str,
        client: Client,
    ) -> None:
        self._name = name
        self._dataset_name = dataset_name
        self._dataset_id = dataset_id
        self._client = client

    def set_description(self, description: str) -> None:
        """set description of the segment client.

        :param description: Description of the segment client to upload
        """
        self._content_segment_client.upload_description(description)

    @property
    def name(self) -> str:
        """Get the name of this segment client.

        :return: The name of the segment
        """
        return self._name

    @property
    def dataset_id(self) -> str:
        """Get the dataset ID.

        :return: The dataset ID
        """
        return self._dataset_id

    @property
    def contentset_id(self) -> str:
        """Get the contentset ID.

        :return: The contentset ID
        """
        return self._content_segment_client._contentset_id  # pylint: disable=protected-access

    @property
    def labelset_id(self) -> str:
        """Get the labelset ID.

        :return: The labelset ID
        """
        if not self._label_segment_client:
            return ""

        return self._label_segment_client._labelset_id  # pylint: disable=protected-access


class SegmentClient(SegmentClientBase):
    """ContentSegmentClient has only one sensor, supporting upload_data method."""

    _content_segment_client: ContentSegmentClient
    _label_segment_client: Optional[LabelSegmentClient]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        dataset_name: str,
        dataset_id: str,
        client: Client,
        content_segment_client: ContentSegmentClient,
        label_segment_client: Optional[LabelSegmentClient],
    ) -> None:
        super().__init__(name, dataset_name, dataset_id, client)
        self._content_segment_client = content_segment_client
        self._label_segment_client = label_segment_client

    def upload_data(self, local_path: str, remote_path: str = "") -> None:
        """Upload data with local path to the segment.

        :param local_path: The local path of the data to upload
        :param remote_path: The path to save the data in segment client
        :raises
            GASPathError: when remote_path does not follow linux style
            GASFrameError: when uploading frame has neither timestamp nor frame_index
        """

        self._content_segment_client.upload_data(local_path, remote_path)

    def upload_data_object(self, data: Data) -> None:
        """Upload data with local path in Data object to the segment.

        :param data: The data object which represents the local file to upload
        """
        self._content_segment_client.upload_data_object(data)
        if self._content_segment_client:
            self._content_segment_client.upload_data_object(data)

    def delete_data(self, remote_paths: Union[str, List[str]]) -> None:
        """Delete data with remote paths.

        :param remote_paths: A single path or a list of paths which need to deleted,
        eg: test/os1.png or [test/os1.png]
        """
        self._content_segment_client.delete_data(remote_paths)

    def list_data(self) -> List[str]:
        """List all data in a segment client.

        :return: A list of data path
        """
        if self._label_segment_client:
            return self._label_segment_client.list_data()

        return self._content_segment_client.list_data()

    def list_data_objects(self) -> List[Data]:
        """List all `Data` object in a dataset segment.

        :return: A list of `Data` object
        """
        if self._label_segment_client:
            return self._label_segment_client.list_data_objects()

        return self._content_segment_client.list_data_objects()


class FusionSegmentClient(SegmentClientBase):
    """FusionSegmentClient has multiple sensors,
    supporting upload_sensor and upload_frame method.
    """

    _content_segment_client: FusionContentSegmentClient
    _label_segment_client: Optional[FusionLabelSegmentClient]

    def __init__(  # pylint: disable=too-many-arguments
        self,
        name: str,
        dataset_name: str,
        dataset_id: str,
        client: Client,
        content_segment_client: FusionContentSegmentClient,
        label_segment_client: Optional[FusionLabelSegmentClient],
    ) -> None:
        super().__init__(name, dataset_name, dataset_id, client)
        self._content_segment_client = content_segment_client
        self._label_segment_client = label_segment_client

    def upload_sensor_object(self, sensor: T) -> None:
        """Upload sensor to the segment client.

        :param sensor: The sensor to upload
        """
        self._content_segment_client.upload_sensor_object(sensor)

    def delete_sensors(self, sensor_names: Union[str, List[str]]) -> None:
        """Delete sensors with a single name or a name list.

        :param sensor_names: A single sensor name or a list of sensor names
        """
        self._content_segment_client.delete_sensors(sensor_names)

    def list_sensors(self) -> List[str]:
        """List all sensor names in a segment client.

        :return: A list of sensor name
        """
        return self._content_segment_client.list_sensors()

    def list_sensor_objects(self) -> NameSortedDict[Sensor]:
        """List all sensors in a segment client.

        :return: A NameSortedDict of `Sensor` object
        """
        return self._content_segment_client.list_sensor_objects()

    def upload_frame_object(self, frame: Frame, frame_index: Optional[int] = None) -> None:
        """Upload frame to the segment client.

        :param frame: The frame to upload
        :param frame_index: The frame index, used for TensorBay to sort the frame
        :raises
            GASPathError: when remote_path does not follow linux style
        """

        self._content_segment_client.upload_frame_object(frame, frame_index)

        if self._label_segment_client:
            self._label_segment_client.upload_frame_object(frame)

    def list_frame_objects(self) -> List[Frame]:
        """List all frames in the segment client.

        :return: A list `Frame` object
        """
        if self._label_segment_client:
            return self._label_segment_client.list_frame_objects()

        return self._content_segment_client.list_frame_objects()


class DatasetClientBase:
    """This class defines the concept of a dataset and some operations on it.

    :param name: Dataset name
    :param dataset_id: Dataset id
    :param contentset_id: Contentset id
    :param labelset_id: Labelset id
    :param client: The client used for sending request to TensorBay
    """

    _contentset_client: Union[ContentsetClient, FusionContentsetClient]
    _labelset_client: Union[None, LabelsetClient, FusionLabelsetClient]

    def __init__(self, name: str, dataset_id: str, client: Client) -> None:
        self._name = name
        self._dataset_id = dataset_id
        self._client = client

    def set_description(self, description: str) -> None:
        """Set description of the dataset.

        :param description: description of the dataset
        """
        post_data = {
            "datasetId": self._dataset_id,
            "desc": description,
        }
        self._client.dataset_post("updateDataset", post_data)

    @property
    def dataset_id(self) -> str:
        """Get the dataset ID.

        :return: The dataset ID
        """
        return self._dataset_id

    @property
    def contentset_id(self) -> str:
        """Get the contentset ID.

        :return: The contentset ID
        """
        return self._contentset_client._contentset_id  # pylint: disable=protected-access

    @property
    def labelset_id(self) -> str:
        """Get the labelset ID.

        :return: The labelset ID
        """
        if not self._labelset_client:
            return ""
        return self._labelset_client._labelset_id  # pylint: disable=protected-access

    def _commit(self, message: str, tag: Optional[str] = None) -> Tuple[str, str, str]:
        post_data = {
            "datasetId": self._dataset_id,
            "versionDesc": message,
        }
        if tag:
            post_data["version"] = tag

        response = self._client.dataset_post("publishDataset", post_data)
        return (
            response["id"],
            response["contentSetId"],
            response["labelSetId"],
        )

    def list_segments(self) -> List[str]:
        """List all segment names in a dataset.

        :return: A list of segment names
        """
        return self._contentset_client.list_segments()

    def delete_segments(
        self,
        segment_names: Union[str, List[str]],
        force_delete: bool = False,
    ) -> None:
        """Delete segments according to the name list.

        :param name: A single segment Name or a list of the segment names, if empty, the default
        segment will be deleted, if you want to delete all segment, "_all" should be submitted.
        :param force_delete: By default, only segment with no sensor can be deleted.
        If force_delete is true, then sensor and its objects will also be deleted
        """
        self._contentset_client.delete_segments(segment_names, force_delete)

    def _create_labelset(self, label_tables: LabelTables) -> str:
        metadata = LabelsetClientBase.create_metadata(label_tables)
        if not metadata:
            raise TypeError("Empty label table")

        post_data = {
            "datasetId": self._dataset_id,
            "contentSetId": self.contentset_id,
            "type": LabelsetClientBase.TYPE_GROUND_TRUTH,
            "version": "v1.0.2",
            "meta": metadata,
        }

        data = self._client.labelset_post("createLabelSet", post_data)
        return data["labelSetId"]  # type: ignore[no-any-return]


class DatasetClient(DatasetClientBase):
    """dataset has only one sensor, supporting create segment."""

    _contentset_client: ContentsetClient
    _labelset_client: Optional[LabelsetClient]

    def __init__(  # pylint: disable=too-many-arguments
        self, name: str, dataset_id: str, client: Client, contentset_id: str, labelset_id: str
    ) -> None:
        super().__init__(name, dataset_id, client)
        self._contentset_client = ContentsetClient(name, contentset_id, client)
        if labelset_id:
            self._labelset_client = LabelsetClient(labelset_id, name, client)
        else:
            self._labelset_client = None

    def get_or_create_segment(self, name: str = "") -> SegmentClient:
        """Create a segment set according to its name.

        :param name: Segment name, can not be "_default"
        :return: Created segment with given name, if not given name, Created default segment
        """
        content_segment_client = self._contentset_client.get_or_create_segment(name)
        label_segment_client = (
            self._labelset_client.get_segment(name) if self._labelset_client else None
        )

        return SegmentClient(
            name,
            self._name,
            self._dataset_id,
            self._client,
            content_segment_client,
            label_segment_client,
        )

    def get_segment(self, name: str = "") -> SegmentClient:
        """Get a segment according to its name.

        :param name: The name of the desired segment
        :raises GASSegmentError: When the required segment does not exist
        :return: The desired segment
        """
        content_segment_client = self._contentset_client.get_segment(name)
        label_segment_client = (
            self._labelset_client.get_segment(name) if self._labelset_client else None
        )
        return SegmentClient(
            name,
            self._name,
            self._dataset_id,
            self._client,
            content_segment_client,
            label_segment_client,
        )

    def get_segment_object(self, name: str = "") -> Segment:
        """Get a segment object according to its name.

        :param name: The name of the desired segment object
        :raises GASSegmentError: When the required segment does not exist
        :return: The desired segment object
        """
        segment_client = self.get_segment(name)
        segment = Segment(name)
        for data in segment_client.list_data_objects():
            segment.append(data)

        return segment

    def upload_segment_object(
        self,
        segment: Segment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> SegmentClient:
        """Upload a `Segment` to the dataset,
        This function will upload all info contains in the input `Segment` object,
        which includes:
        - Create a segment using the name of input `Segment`
        - Upload all `Data` in the Segment to the dataset

        :param segment: The `Segment` object contains the information needs to be upload
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The client used for uploading the data in the `Segment`
        """
        content_segment_client = self._contentset_client.upload_segment_object(
            segment,
            jobs=jobs,
            skip_uploaded_files=skip_uploaded_files,
        )
        label_segment_client: Optional[LabelSegmentClient] = None
        if self._labelset_client:
            label_segment_client = self._labelset_client.upload_segment_object(
                segment,
                jobs=jobs,
                skip_uploaded_files=skip_uploaded_files,
            )

        return SegmentClient(
            segment.name,
            self._name,
            self._dataset_id,
            self._client,
            content_segment_client,
            label_segment_client,
        )

    def upload_label_tables(self, label_tables: LabelTables) -> None:
        """Upload a LabelTables to the dataset,

        :param label_tables: The `LabelTables` object to upload
        """
        if not self._labelset_client:
            labelset_id = self._create_labelset(label_tables)
            self._labelset_client = LabelsetClient(labelset_id, self._name, self._client)
            return

        self._labelset_client.upload_label_tables(label_tables)

    def commit(self, message: str, tag: Optional[str] = None) -> "DatasetClient":
        """
        Commit dataset

        :param message: The commit message of this commit
        :param tag: set a tag for current commit
        :return: The committed dataset client
        """
        dataset_id, contentset_id, labelset_id = self._commit(message, tag)
        return DatasetClient(self._name, dataset_id, self._client, contentset_id, labelset_id)


class FusionDatasetClient(DatasetClientBase):
    """Client for fusion dataset which has multiple sensors,
    supporting create fusion segment.
    """

    _contentset_client: FusionContentsetClient
    _labelset_client: Optional[FusionLabelsetClient]

    def __init__(  # pylint: disable=too-many-arguments
        self, name: str, dataset_id: str, client: Client, contentset_id: str, labelset_id: str
    ) -> None:
        super().__init__(name, dataset_id, client)
        self._contentset_client = FusionContentsetClient(name, contentset_id, client)
        if labelset_id:
            self._labelset_client = FusionLabelsetClient(labelset_id, name, client)
        else:
            self._labelset_client = None

    def get_or_create_segment(self, name: str = "") -> FusionSegmentClient:
        """Create a fusion segment set according to the given name.

        :param name: Segment name, can not be "_default"
        :return: Created fusion segment with given name, if not given name, Created default segment
        """
        content_segment_client = self._contentset_client.get_or_create_segment(name)
        label_segment_client = (
            self._labelset_client.get_segment(name) if self._labelset_client else None
        )

        return FusionSegmentClient(
            name,
            self._name,
            self._dataset_id,
            self._client,
            content_segment_client,
            label_segment_client,
        )

    def get_segment(self, name: str = "") -> FusionSegmentClient:
        """Get a fusion segment according to its name.

        :param name: The name of the desired fusion segment
        :raises GASSegmentError: When the required fusion segment does not exist
        :return: The desired fusion segment
        """
        content_segment_client = self._contentset_client.get_segment(name)
        label_segment_client = (
            self._labelset_client.get_segment(name) if self._labelset_client else None
        )
        return FusionSegmentClient(
            name,
            self._name,
            self._dataset_id,
            self._client,
            content_segment_client,
            label_segment_client,
        )

    def upload_segment_object(
        self,
        segment: FusionSegment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> FusionSegmentClient:
        """Upload a `FusionSegment` to the dataset,
        This function will upload all info contains in the input `FusionSegment` object,
        which includes:
        - Create a segment using the name of input `FusionSegment`
        - Upload all `Sensor` in the segment to the dataset
        - Upload all `Frame` in the segment to the dataset

        :param segment: The `Segment` object needs to be uploaded
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The client used for uploading the data in the `FusionSegment`
        """
        content_segment_client = self._contentset_client.upload_segment_object(
            segment,
            jobs=jobs,
            skip_uploaded_files=skip_uploaded_files,
        )
        label_segment_client: Optional[FusionLabelSegmentClient] = None
        if self._labelset_client:
            label_segment_client = self._labelset_client.upload_segment_object(
                segment,
                jobs=jobs,
                skip_uploaded_files=skip_uploaded_files,
            )

        return FusionSegmentClient(
            segment.name,
            self._name,
            self._dataset_id,
            self._client,
            content_segment_client,
            label_segment_client,
        )

    def upload_label_tables(self, label_tables: LabelTables) -> None:
        """Upload a LabelTables to the fusion dataset,

        :param label_tables: The `LabelTables` object to upload
        """
        if not self._labelset_client:
            labelset_id = self._create_labelset(label_tables)
            self._labelset_client = FusionLabelsetClient(labelset_id, self._name, self._client)
            return

        self._labelset_client.upload_label_tables(label_tables)

    def commit(self, message: str, tag: Optional[str] = None) -> "FusionDatasetClient":
        """
        Commit fusion dataset

        :param message: The commit message of this commit
        :param tag: set a tag for current commit
        :return: The committed fusion dataset client
        """
        dataset_id, contentset_id, labelset_id = self._commit(message, tag)
        return FusionDatasetClient(self._name, dataset_id, self._client, contentset_id, labelset_id)

#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines the class Labelset.
"""

from typing import Any, Dict, Generator, Iterable, List, Optional, Set, Tuple

from ..dataset import Data, Frame, FusionSegment, Segment
from ..label import AudioLabelTable, CategoryInfo, LabelTables, LabelType
from ..utility import TBRN, NameSortedDict, TBRNType
from .path import SegmentNameWrapper
from .requests import Client, multithread_upload

_FULL_DATA_LIST_TYPE = 2


class LabelSegmentClientBase:  # pylint: disable=too-few-public-methods
    """This class defines the concept of a labelset segment client and some opertions on it.

    :param name: Segment name, unique for a labelset
    :param labelset_id: Labelset ID
    :param dataset_name: Dataset name
    :param client: The client used for sending request to TensorBay
    """

    def __init__(self, name: str, labelset_id: str, dataset_name: str, client: Client) -> None:
        self._name = name
        self._labelset_id = labelset_id
        self._dataset_name = dataset_name
        self._client = client
        self._name_wrapper = SegmentNameWrapper(name)

    def get_segment_name(self) -> str:
        """Return the name of this labelset segment."""
        return self._name

    def _get_url(self, tbrn: TBRN) -> str:
        """Get url of specific remote_path from labelset

        :param remote_path: The remote_path of the data
        :param sensor_name: The name of the of the data sensor
        :return: The url of the input remote_path and sensor_name
        """
        remote_path = tbrn.remote_path
        sensor_name = tbrn.sensor_name if tbrn.type == TBRNType.FUSION_FILE else ""
        post_data = {
            "labelSetId": self._labelset_id,
            "listType": _FULL_DATA_LIST_TYPE,
            "needLabel": False,
            "objectPath": self._name_wrapper.get_object_path(remote_path, sensor_name),
            "outputVersion": "v1.0.2",
        }
        response = self._client.labelset_post("getUrlAndLabel", post_data)
        return response["url"]  # type: ignore[no-any-return]

    def _upload_label(
        self,
        data: Data,
        sensor_name: str = "",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Upload label to the labelset.

        :param data: The Data contains the labels to be uploaded
        :param sensor_name: Sensor name of the Data
        :param metadata: Some additional data of the label
        """
        remote_path = data.remote_path

        post_data: Dict[str, Any] = {}
        post_data["ObjectPath"] = self._name_wrapper.get_object_path(remote_path, sensor_name)
        post_data["labelValues"] = data.dump_labels()
        post_data["labelSetId"] = self._labelset_id
        if metadata:
            post_data["labelMeta"] = metadata
        self._client.labelset_post("putLabel", post_data)


class LabelSegmentClient(LabelSegmentClientBase):
    """A class used to represent a segment client of a labelset."""

    def upload_data_object(self, data: Data) -> None:
        """Upload the input data's label to the labelset segment.

        :param data: The `Data` object which contains the labels to be uploaded
        """
        self._upload_label(data)

    def list_data(self) -> List[str]:
        """List all data remote path in a labelset segment.

        :return: A list of data path
        """
        post_data = {
            "labelSetId": self._labelset_id,
            "listType": _FULL_DATA_LIST_TYPE,
            "segmentName": self._name_wrapper.post_segment_name,
        }
        objects = self._client.labelset_post("listObjectsBySegment", post_data)["objects"]
        return [self._name_wrapper.get_remote_path(info["objectName"]) for info in objects]

    def list_data_objects(self) -> List[Data]:
        """List all `Data` object in a labelset segment.

        :return: A list of `Data` object
        """
        labels = self._list_data_summaries()

        data_list = []
        for label in labels:
            remote_path = self._name_wrapper.get_remote_path(label["objectPath"])
            tbrn = TBRN(self._dataset_name, self._name, remote_path=remote_path)
            data = Data(tbrn, url_getter=self._get_url)
            data.load_labels(label["values"])
            data_list.append(data)

        return data_list

    def _list_data_summaries(self) -> List[Dict[str, Any]]:
        post_data = {
            "labelSetId": self._labelset_id,
            "listType": _FULL_DATA_LIST_TYPE,
            "segmentName": self._name_wrapper.post_segment_name,
            "outputVersion": "v1.0.2",
            "pageSize": -1,
            "projection": {
                "objectpath": 1,
                "values": 1,
            },
        }
        response = self._client.labelset_post("listLabelsBySegment", post_data)
        return response["labels"]  # type: ignore[no-any-return]

    def _list_uploaded_data(self) -> Set[str]:
        uploaded_set = set()
        labels = self._list_data_summaries()
        for label in labels:
            if not label["values"]:
                continue
            remote_path = self._name_wrapper.get_remote_path(label["objectPath"])
            uploaded_set.add(remote_path)

        return uploaded_set

    def _list_labels(self, remote_paths: List[str]) -> List[Dict[str, Any]]:
        post_data = {
            "labelSetId": self._labelset_id,
            "outputVersion": "v1.0.2",
            "objectPaths": [self._name_wrapper.get_object_path(path) for path in remote_paths],
            "ignoreObjectSize": True,
            "ignoreObjectUrl": True,
            "pageSize": -1,
            "projection": {
                "objectpath": 1,
                "values": 1,
            },
        }
        response = self._client.labelset_post("listLabels", post_data)
        return response["labels"]  # type: ignore[no-any-return]

    def _list_uploaded_data_tmp(self, segment: Segment) -> Set[str]:
        uploaded_set = set()
        page_size = 10000
        remote_paths = [data.remote_path for data in segment]
        for i in range(0, len(remote_paths), page_size):
            labels = self._list_labels(remote_paths[i : i + page_size])
            for label in labels:
                if not label["values"]:
                    continue
                remote_path = self._name_wrapper.get_remote_path(label["objectPath"])
                uploaded_set.add(remote_path)

        # labels = self._list_data_summaries()
        # for label in labels:
        #     if not label["values"]:
        #         continue
        #     remote_path = self._name_wrapper.get_remote_path(label["objectPath"])
        #     uploaded_set.add(remote_path)

        return uploaded_set


class FusionLabelSegmentClient(LabelSegmentClientBase):
    """A class used to represent a segment client of a fusion labelset."""

    def upload_frame_object(self, frame: Frame) -> None:
        """Upload the input frame's label to the fusion labelset segment.

        :param frame: The `Frame` object which contains the labels to be uploaded
        """
        for sensor_name, data in frame.items():
            self._upload_label(data, sensor_name)

    def list_frame_objects(self) -> List[Frame]:
        """List all frames in the labelset segment without the label info.

        :return: A list `Frame` object
        """
        summaries = self._list_frame_summaries()
        frames = []
        for frame_info in summaries:
            frame = Frame()
            for data_info in frame_info:
                sensor_name = data_info["sensorName"]
                object_path = data_info["objectPath"]
                remote_path = self._name_wrapper.get_remote_path(object_path, sensor_name)
                data = Data(remote_path, timestamp=data_info.get("timestamp", None))
                data.load_labels(data_info["label"]["values"])
                frame[sensor_name] = data

            frames.append(frame)

        return frames

    def _list_frame_summaries(self) -> List[List[Dict[str, Any]]]:
        post_data = {
            "labelSetId": self._labelset_id,
            "listType": _FULL_DATA_LIST_TYPE,
            "pageSize": -1,
            "needLabel": True,
            "outputVersion": "v1.0.2",
            "projection": {
                "objectpath": 1,
                "values": 1,
            },
            "segmentName": self._name_wrapper.post_segment_name,
        }
        response = self._client.labelset_post("listFrameObjects", post_data)
        return response["frameObjects"]  # type: ignore[no-any-return]

    def _list_uploaded_data(self) -> Set[Tuple[str, str]]:
        uploaded_set = set()
        summaries = self._list_frame_summaries()
        for frame_info in summaries:
            for data_info in frame_info:
                if not data_info["label"]["values"]:
                    continue
                sensor_name = data_info["sensorName"]
                object_path = data_info["objectPath"]
                remote_path = self._name_wrapper.get_remote_path(object_path, sensor_name)
                uploaded_set.add((sensor_name, remote_path))

        return uploaded_set


class LabelsetClientBase:
    """A base class which respresents a client of labelset.

    :param labelset_id: The ID of the labelset
    :param dataset_name: The name of the dataset
    :param client: The client used for sending request to TensorBay
    """

    TYPE_GROUND_TRUTH = 3
    _PUBLISH_STATUS = 2
    _STATISTICSED_STATUS = 4
    _TASK_TYPE = {
        LabelType.CLASSIFICATION: {"code": 7, "nameEn": "2D CLASSIFICATION"},
        LabelType.BOX2D: {"code": 10, "nameEn": "2D BOX"},
        LabelType.BOX3D: {"code": 4, "nameEn": "3D BOX"},
        LabelType.POLYGON2D: {"code": 22, "nameEn": "2D POLYGON"},
        LabelType.POLYLINE2D: {"code": 8, "nameEn": "2D POLYLINE"},
        LabelType.SENTENCE: {"code": 27, "nameEn": "SENTENCE"},
    }
    _DELIMITER = "."

    def __init__(self, labelset_id: str, dataset_name: str, client: Client) -> None:
        self._labelset_id = labelset_id
        self._dataset_name = dataset_name
        self._client = client

    def get_labelset_id(self) -> str:
        """Return the id of the labelset.

        :return: The id of the labelset
        """
        return self._labelset_id

    def upload_label_tables(self, label_tables: LabelTables) -> None:
        """Upload label tables to the labelset.

        :param label_tables: The label tables to be uploaded
        """
        metadata = LabelsetClientBase.create_metadata(label_tables)
        if not metadata:
            return

        post_data = {
            "labelSetId": self._labelset_id,
            "meta": metadata,
        }
        self._client.labelset_post("updateLabelSet", post_data)

    def list_segments(self) -> List[str]:
        """List all segment names in a labelset.

        :return: A list of segment names
        """
        post_data = {
            "labelSetId": self._labelset_id,
            "listType": _FULL_DATA_LIST_TYPE,
            "pageSize": -1,
        }
        segment_names = self._client.labelset_post("listSegments", post_data)["segments"]
        return [SegmentNameWrapper.get_local_segment_name(name) for name in segment_names]

    def publish(self) -> None:
        """Publish the labelset."""
        post_data = {"labelSetId": self._labelset_id, "status": LabelsetClientBase._PUBLISH_STATUS}
        self._client.labelset_post("updateLabelSetStatus", post_data)

    def is_published(self) -> bool:
        """Gheck whether the labelset is published.

        :return: Return `True` if the lableset is publish, otherwise return `False`
        """
        post_data = {"id": self._labelset_id, "projection": {"status": 1}}
        data = self._client.labelset_post("listLabelSets", post_data)
        status = data["labelSets"][0]["labelSet"]["status"]
        return status == LabelsetClientBase._STATISTICSED_STATUS  # type: ignore[no-any-return]

    @staticmethod
    def create_metadata(label_tables: LabelTables) -> Dict[str, Any]:
        """Return metadata created from the label tables.

        :return: A dict in metadata format
        """
        task_types = []
        for label_type, label_table in label_tables.items():
            task_type = LabelsetClientBase._TASK_TYPE[label_type].copy()
            if isinstance(label_table, AudioLabelTable):
                task_type.update(label_table.dumps())
            else:
                task_type["is_tracking"] = label_table.is_tracking
                if label_table.categories:
                    task_type["categories"] = LabelsetClientBase._create_categories_meta(
                        label_table.categories
                    )
                if label_table.attributes:
                    task_type["attributes"] = label_table.dump_attributes()

            task_types.append(task_type)

        return {"taskTypes": task_types} if task_types else {}

    @staticmethod
    def _create_categories_meta(categories: NameSortedDict[CategoryInfo]) -> List[Dict[str, Any]]:
        """Create the category metadata with parent-child relationship.

        :param categories: The input categories in a NameSortedDict
        :return: The created category metadata list
        """
        category_tree = []
        tree_index: Dict[str, Any] = {}
        for category in categories:
            category_info = {"nameEn": category}
            while True:
                i = category.rfind(LabelsetClientBase._DELIMITER)
                if i == -1:
                    category_tree.append(category_info)
                    break

                category = category[:i]
                if category in tree_index:
                    tree_index[category].append(category_info)
                    break

                tree_index[category] = [category_info]
                category_info = {"nameEn": category, "subcategories": tree_index[category]}
        return category_tree


class LabelsetClient(LabelsetClientBase):
    """A class which respresents a client of a labelset."""

    def get_segment(self, name: str) -> LabelSegmentClient:
        """Get a labelset segment according to the input name.

        :param name: The name of the requested labelset segment
        :return: The requested labelset segment client
        """

        return LabelSegmentClient(name, self._labelset_id, self._dataset_name, self._client)

    def upload_segment_object(
        self,
        segment: Segment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> LabelSegmentClient:
        """Upload a `Segment` to the labelset,
        This function will upload all labels contains in the input `Segment` object,

        :param segment: The `Segment` object contains the labels needs to be uploaded
        :param jobs: The number of the max workers in multithread upload
        :return: The client used for uploading the label in the `Segment`
        """
        segment_client = self.get_segment(segment.name)

        segment_filter: Iterable[Data]
        if skip_uploaded_files:
            # done_set = segment_client._list_uploaded_data()  # pylint: disable=protected-access
            done_set = segment_client._list_uploaded_data_tmp(
                segment
            )  # pylint: disable=protected-access
            segment_filter = filter(lambda data: data.remote_path not in done_set, segment)
        else:
            segment_filter = segment

        multithread_upload(segment_client.upload_data_object, segment_filter, jobs=jobs)
        return segment_client


class FusionLabelsetClient(LabelsetClientBase):
    """A class which respresents a client of a fusion labelset."""

    def get_segment(self, name: str) -> FusionLabelSegmentClient:
        """Get a client of fusion labelset segment according to the input name.

        :param name: The name of the requested fusion labelset segment
        :return: The requested client of fusion labelset segment
        """
        return FusionLabelSegmentClient(name, self._labelset_id, self._dataset_name, self._client)

    def upload_segment_object(
        self,
        segment: FusionSegment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> FusionLabelSegmentClient:
        """Upload a `FusionSegment` to the labelset,
        This function will upload all labels contains in the input `FusionSegment` object,

        :param segment: The `FusionSegment` object contains the labels needs to be uploaded
        :param jobs: The number of the max workers in multithread upload
        :return: The client used for uploading the label in the `FusionSegment`
        """
        segment_client = self.get_segment(segment.name)

        if skip_uploaded_files:
            done_set = segment_client._list_uploaded_data()  # pylint: disable=protected-access
        else:
            done_set = set()

        segment_filter = self._frame_data_generator(segment, done_set)

        multithread_upload(
            lambda args: segment_client._upload_label(  # pylint: disable=protected-access
                args[1], args[0]
            ),
            segment_filter,
            jobs=jobs,
        )

        return segment_client

    @staticmethod
    def _frame_data_generator(
        segment: FusionSegment,
        uploaded_set: Set[Tuple[str, str]],
    ) -> Generator[Tuple[str, Data], None, None]:
        for frame in segment:
            for sensor_name, data in frame.items():
                if (sensor_name, data.remote_path) in uploaded_set:
                    continue

                yield (sensor_name, data)

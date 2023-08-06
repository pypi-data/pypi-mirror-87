#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class ContentsetClientBase, ContentsetClient, FusionContentsetClient,
ContentSegmentClientBase, ContentSegmentClient, FusionContentSegmentClient
"""

import base64
import json
import os
import threading
import time
import uuid
from copy import deepcopy
from pathlib import PurePosixPath
from typing import Any, Dict, Generator, Iterable, List, Optional, Tuple, TypeVar, Union

import filetype
from requests_toolbelt import MultipartEncoder

from ..dataset import Data, Frame, FusionSegment, Segment
from ..sensor import Camera, FisheyeCamera, Sensor, SensorType
from ..utility import TBRN, NameSortedDict
from .exceptions import GASException, GASFrameError, GASPathError, GASSegmentError
from .path import SegmentNameWrapper
from .requests import Client, default_config, multithread_upload, post

T = TypeVar("T", bound=Sensor)  # pylint: disable=invalid-name


class ContentSegmentClientBase:
    """This class defines the concept of a segment client and some opertions on it.

    :param name: Segment name, unique for a contentset
    :param contentset_name: Dataset name
    :param contentset_id: Dataset id
    :param client: The client used for sending request to TensorBay
    """

    _PERMISSION_CATEGORY: str
    _EXPIRED_IN_SECOND = 240

    def __init__(self, name: str, contentset_name: str, contentset_id: str, client: Client) -> None:
        self._name = name
        self._contentset_name = contentset_name
        self._contentset_id = contentset_id
        self._client = client
        self._permission: Dict[str, Any] = {"expireAt": 0}
        self._permission_lock = threading.Lock()
        self._name_wrapper = SegmentNameWrapper(name)

    def upload_description(self, description: Optional[str] = None) -> None:
        """Upload description of the segment client.

        :param description: Description of the segment client to upload
        """
        if not description:
            return
        post_data = {"contentSetId": self._contentset_id, "name": self._name, "desc": description}
        self._client.contentset_post("createOrUpdateSegment", post_data)

    def get_segment_name(self) -> str:
        """Return the name of this segment client."""
        return self._name

    def _get_upload_permission(self) -> Dict[str, Any]:
        with self._permission_lock:
            if int(time.time()) >= self._permission["expireAt"]:
                post_data = {
                    "id": self._contentset_id,
                    "category": self._PERMISSION_CATEGORY,
                    "expiredInSec": self._EXPIRED_IN_SECOND,
                    "segmentName": self._name,
                }
                self._permission = self._client.contentset_post("getPutPermission", post_data)

                if default_config.is_intern:
                    urlsplit = self._permission["extra"]["host"].rsplit(".", 2)
                    urlsplit[0] += "-internal"
                    self._permission["extra"]["host"] = ".".join(urlsplit)

            return deepcopy(self._permission)

    def _clear_upload_permission(self) -> None:
        with self._permission_lock:
            self._permission = {"expireAt": 0}

    def _synchronize_upload_info(
        self, permission: Dict[str, Any], callback_info: Dict[str, Any]
    ) -> None:
        """Synchronize upload data info with tensorbay.

        :param permission: The data object which represents the permission info
        :param callback_info: The data object which represents the S3 info
        """
        if callback_info.pop("Server", None) != "AmazonS3":
            return
        post_data = callback_info
        post_data["x:id"] = permission["x:id"]
        post_data["x:category"] = permission["x:category"]
        post_data["object"] = permission["key"]
        post_data["x:incidental"] = permission.get("x:incidental", None)

        self._client.contentset_post("putCallback", post_data)

    @staticmethod
    def _post_multipart_formdata(
        url: str,
        local_path: str,
        remote_path: str,
        data: Dict[str, Any],
    ) -> Any:
        with open(local_path, "rb") as file:
            data["file"] = (remote_path, file, filetype.guess_mime(local_path))
            multipart = MultipartEncoder(data)
            return post(url, data=multipart, content_type=multipart.content_type)


class ContentSegmentClient(ContentSegmentClientBase):
    """ContentSegmentClient has only one sensor, supporting upload_data method."""

    _PERMISSION_CATEGORY = "contentSet"

    def upload_data(self, local_path: str, remote_path: str = "") -> None:
        """Upload data with local path to the segment.

        :param local_path: The local path of the data to upload
        :param remote_path: The path to save the data in segment client
        :raises
            GASPathError: when remote_path does not follow linux style
            GASFrameError: when uploading frame has neither timestamp nor frame_index
        """

        if not remote_path:
            remote_path = os.path.basename(local_path)

        if "\\" in remote_path:
            raise GASFrameError()

        permission = self._get_upload_permission()
        post_data = permission["result"]
        post_data["key"] = permission["extra"]["objectPrefix"] + remote_path

        try:
            response = self._post_multipart_formdata(
                permission["extra"]["host"],
                local_path,
                remote_path,
                post_data,
            )

            self._synchronize_upload_info(post_data, response)

        except GASException:
            self._clear_upload_permission()
            raise

    def upload_data_object(self, data: Data) -> None:
        """Upload data with local path in Data object to the segment.

        :param data: The data object which represents the local file to upload
        """
        self.upload_data(data.local_path, data.remote_path)

    def delete_data(self, remote_paths: Union[str, List[str]]) -> None:
        """Delete data with remote paths.

        :param remote_path_list: A single path or a list of paths which need to deleted,
        eg: test/os1.png or [test/os1.png]
        """
        if not isinstance(remote_paths, list):
            remote_paths = [remote_paths]

        object_paths = [self._name_wrapper.get_object_path(path) for path in remote_paths]
        post_data = {
            "contentSetId": self._contentset_id,
            "filePaths": object_paths,
        }
        self._client.contentset_post("deleteObjects", post_data)

    def list_data(self) -> List[str]:
        """List all data in a segment client.

        :return: A list of data path
        """
        post_data = {
            "contentSetId": self._contentset_id,
            "segmentName": self._name_wrapper.post_segment_name,
        }
        data = self._client.contentset_post("listObjects", post_data)
        return [self._name_wrapper.get_remote_path(object_path) for object_path in data["objects"]]

    def list_data_objects(self) -> List[Data]:
        """List all `Data` object in a contentset segment.

        :return: A list of `Data` object
        """
        data_list = []
        for remote_path in self.list_data():
            tbrn = TBRN(self._contentset_name, self._name, remote_path=remote_path)
            data_list.append(Data(tbrn))
        return data_list


class FusionContentSegmentClient(ContentSegmentClientBase):
    """FusionSegmentClient has multiple sensors,
    supporting upload_sensor and upload_frame method.
    """

    _PERMISSION_CATEGORY = "frame"

    def upload_sensor_object(self, sensor: T) -> None:
        """Upload sensor to the segment client.

        :param sensor: The sensor to upload
        """
        post_data = {
            "name": sensor.name,
            "type": sensor.enum.value,
            "extrinsicParams": sensor.extrinsics.dumps() if sensor.extrinsics else {},
        }

        if isinstance(sensor, (Camera, FisheyeCamera)):
            if sensor.intrinsics:
                intrinsics = sensor.intrinsics.dumps()
                intrinsics["distortionCoefficient"] = intrinsics.pop("distortionCoefficients", {})
                post_data["intrinsicParams"] = intrinsics
            else:
                post_data["intrinsicParams"] = {}

        if sensor.description:
            post_data["desc"] = sensor.description

        post_data["contentSetId"] = self._contentset_id
        post_data["segmentName"] = self._name
        self._client.contentset_post("createOrUpdateSensor", post_data)

    def delete_sensors(self, sensor_names: Union[str, List[str]]) -> None:
        """Delete sensors with a single name or a name list.

        :param sensor_names: A single sensor name or a list of sensor names
        """
        if not isinstance(sensor_names, list):
            sensor_names = [sensor_names]
        post_data = {
            "contentSetId": self._contentset_id,
            "sensorNames": {self._name: sensor_names},
        }
        self._client.contentset_post("deleteSensors", post_data)

    def _list_sensor_summaries(self) -> List[Dict[str, Any]]:
        post_data = {
            "contentSetId": self._contentset_id,
            "segmentName": self._name_wrapper.post_segment_name,
        }
        data = self._client.contentset_post("listSensors", post_data)
        return data["sensors"]  # type: ignore[no-any-return]

    def list_sensors(self) -> List[str]:
        """List all sensor names in a segment client.

        :return: A list of sensor name
        """
        sensor_summaries = self._list_sensor_summaries()
        sensor_names: List[str] = []
        for sensor_info in sensor_summaries:
            sensor_names.append(sensor_info["name"])
        return sensor_names

    def list_sensor_objects(self) -> NameSortedDict[Sensor]:
        """List all sensors in a segment client.

        :return: A NameSortedDict of `Sensor` object
        """
        sensor_summaries = self._list_sensor_summaries()
        sensors: NameSortedDict[Sensor] = NameSortedDict()
        for sensor_info in sensor_summaries:
            SensorClass = SensorType(sensor_info["type"]).type  # pylint: disable=invalid-name
            sensor = SensorClass(sensor_info["name"])
            sensor.description = sensor_info["desc"]
            extrinsics = json.loads(sensor_info["extrinsicParams"])
            if extrinsics:
                sensor.set_extrinsics(loads=extrinsics)
            if isinstance(sensor, Camera):
                intrinsics = json.loads(sensor_info["intrinsicParams"])
                if intrinsics:
                    sensor.set_camera_matrix(**intrinsics["cameraMatrix"])
                    if "distortionCoefficient" in intrinsics:
                        sensor.set_distortion_coefficients(**intrinsics["distortionCoefficient"])
            sensors.add(sensor)

        return sensors

    def upload_frame_object(self, frame: Frame, frame_index: Optional[int] = None) -> None:
        """Upload frame to the segment client.

        :param frame: The frame to upload
        :param frame_index: The frame index, used for TensorBay to sort the frame
        :raises
            GASPathError: when remote_path does not follow linux style
        """

        frame_id = str(uuid.uuid4())

        for sensor_name, data in frame.items():
            remote_path = data.remote_path

            if "\\" in remote_path:
                raise GASPathError(remote_path)

            if frame_index is None and not hasattr(data, "timestamp"):
                raise TypeError(
                    "Either 'frame_index' or 'timestamp' is necessary for sorting frames"
                )

            permission = self._get_upload_permission()
            post_data = permission["result"]

            path = str(PurePosixPath(sensor_name, remote_path))
            post_data["key"] = permission["extra"]["objectPrefix"] + path

            data_info: Dict[str, Any] = {
                "sensorName": sensor_name,
                "segmentName": self._name,
                "frameId": frame_id,
                "objectPath": path,
            }
            if hasattr(data, "timestamp"):
                data_info["timestamp"] = data.timestamp

            if frame_index is not None:
                data_info["frameIndex"] = frame_index

            post_data["x:incidental"] = base64.urlsafe_b64encode(
                json.dumps(data_info).encode()
            ).decode()

            try:
                response = self._post_multipart_formdata(
                    permission["extra"]["host"],
                    data.local_path,
                    remote_path,
                    post_data,
                )
                self._synchronize_upload_info(post_data, response)

            except GASException:
                self._clear_upload_permission()
                raise

    def list_frame_objects(self) -> List[Frame]:
        """List all frames in the segment client.

        :return: A list `Frame` object
        """
        response = self._list_frames()
        frames = []
        for i, response_frame in enumerate(response):
            frame = self._loads_frame_object(i, response_frame)
            frames.append(frame)

        return frames

    def _list_frame_objects_dict(self) -> Dict[int, Tuple[Frame, str]]:
        response = self._list_frames()
        frames: Dict[int, Tuple[Frame, str]] = {}
        for i, response_frame in enumerate(response):
            frame = self._loads_frame_object(i, response_frame)
            frame_index = response_frame[0]["frameIndex"]
            frame_id = response_frame[0]["frameId"]

            frames[frame_index] = (frame, frame_id)

        return frames

    def _list_frames(self, offset: int = 0, page_size: int = -1) -> List[List[Dict[str, Any]]]:
        post_data = {
            "contentSetId": self._contentset_id,
            "segmentName": self._name_wrapper.post_segment_name,
            "offSet": offset,
            "pageSize": page_size,
        }
        data = self._client.contentset_post("listFrames", post_data)
        return data["frames"]  # type: ignore[no-any-return]

    def _loads_frame_object(self, frame_index: int, loads: List[Dict[str, Any]]) -> Frame:
        frame = Frame()
        for data_info in loads:
            sensor_name = data_info["sensorName"]
            remote_path = self._name_wrapper.get_remote_path(data_info["objectPath"], sensor_name)
            timestamp = data_info["timestamp"] if data_info["timestamp"] != -1 else None
            tbrn = TBRN(
                self._contentset_name,
                self._name,
                frame_index,
                sensor_name,
                remote_path=remote_path,
            )
            data = Data(tbrn, timestamp=timestamp)
            frame[sensor_name] = data

        return frame

    def _delete_frames(self, frame_id: Union[str, List[str]]) -> None:
        if not isinstance(frame_id, list):
            frame_id = [frame_id]

        post_data = {"contentSetId": self._contentset_id, "frameIds": frame_id}
        self._client.contentset_post("deleteFrames", post_data)


class ContentsetClientBase:
    """This class defines the concept of a contentset and some operations on it.

    :param name: Dataset name
    :param contentset_id: Contentset id
    :param client: The client used for sending request to TensorBay
    """

    _PUBLISH_STATUS = 7

    def __init__(self, name: str, contentset_id: str, client: Client) -> None:
        self._contentset_name = name
        self._contentset_id = contentset_id
        self._client = client

    def upload_description(
        self,
        description: Optional[str] = None,
        collection_time: Optional[str] = None,
        collection_location: Optional[str] = None,
    ) -> None:
        """Upload description of the contentset.

        :param description: description of the contentset to upload
        :param collection_time: collected time of the contentset to upload
        :param collection_location: collected location of the contentset to upload
        """
        post_data = {}
        if description:
            post_data["desc"] = description
        if collection_time:
            post_data["collectedAt"] = collection_time
        if collection_location:
            post_data["collectedLocation"] = collection_location

        if not post_data:
            return

        post_data["contentSetId"] = self._contentset_id
        self._client.contentset_post("updateContentSet", post_data)

    def get_contentset_id(self) -> str:
        """Get the ID of this contentset."""
        return self._contentset_id

    def publish(self, version: Optional[str] = None) -> None:
        """Publish a new version of a contentset."""
        post_data = {"contentSetId": self._contentset_id}
        if version:
            post_data["version"] = version
        self._client.contentset_post("publishContentSet", post_data)

    def is_published(self) -> bool:
        """Gheck whether the contentset is published.

        :return: Return `True` if the contentset is publish, viceversa.
        """
        post_data = {"contentSetId": self._contentset_id}
        data = self._client.contentset_post("listContentSets", post_data)
        status = data["contentSets"][0]["contentSetResp"]["status"]
        return status == ContentsetClientBase._PUBLISH_STATUS  # type: ignore[no-any-return]

    def list_segments(self) -> List[str]:
        """List all segment names in a contentset.

        :return: A list of segment names
        """
        return self._list_segments()

    def _list_segments(self, segment_names: Optional[List[str]] = None) -> List[str]:
        post_data: Dict[str, Any] = {"contentSetId": self._contentset_id, "pageSize": -1}
        if segment_names:
            post_data["names"] = segment_names
        segments_info = self._client.contentset_post("listSegments", post_data)["segments"]
        return [SegmentNameWrapper.get_local_segment_name(info["name"]) for info in segments_info]

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
        if not isinstance(segment_names, list):
            segment_names = [segment_names]
        post_data = {
            "contentSetId": self._contentset_id,
            "names": segment_names,
            "forceDelete": force_delete,
        }
        self._client.contentset_post("deleteSegments", post_data)


class ContentsetClient(ContentsetClientBase):
    """contentset has only one sensor, supporting create segment."""

    def get_or_create_segment(self, name: str = "") -> ContentSegmentClient:
        """Create a segment set according to its name.

        :param name: Segment name, can not be "_default"
        :return: Created segment with given name, if not given name, Created default segment
        """
        if name and not self._list_segments([name]):
            post_data = {"contentSetId": self._contentset_id, "name": name}
            self._client.contentset_post("createOrUpdateSegment", post_data)
        return ContentSegmentClient(name, self._contentset_name, self._contentset_id, self._client)

    def get_segment(self, name: str = "") -> ContentSegmentClient:
        """Get a segment according to its name.

        :param name: The name of the desired segment
        :raises GASSegmentError: When the required segment does not exist
        :return: The desired segment
        """
        if not self._list_segments([name]):
            raise GASSegmentError(name)
        return ContentSegmentClient(name, self._contentset_name, self._contentset_id, self._client)

    def upload_segment_object(
        self,
        segment: Segment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> ContentSegmentClient:
        """Upload a `Segment` to the contentset,
        This function will upload all info contains in the input `Segment` object,
        which includes:
        - Create a segment using the name of input `Segment`
        - Upload all `Data` in the Segment to the contentset

        :param segment: The `Segment` object contains the information needs to be upload
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The client used for uploading the data in the `Segment`
        """
        segment_client = self.get_or_create_segment(segment.name)
        segment_filter: Iterable[Data]
        if skip_uploaded_files:
            done_set = set(segment_client.list_data())
            segment_filter = filter(lambda data: data.remote_path not in done_set, segment)
        else:
            segment_filter = segment

        multithread_upload(segment_client.upload_data_object, segment_filter, jobs=jobs)
        return segment_client


class FusionContentsetClient(ContentsetClientBase):
    """Client for fusion contentset which has multiple sensors,
    supporting create fusion segment.
    """

    def get_or_create_segment(self, name: str = "") -> FusionContentSegmentClient:
        """Create a fusion segment set according to the given name.

        :param name: Segment name, can not be "_default"
        :return: Created fusion segment with given name, if not given name, Created default segment
        """
        if name and not self._list_segments([name]):
            post_data = {"contentSetId": self._contentset_id, "name": name}
            self._client.contentset_post("createOrUpdateSegment", post_data)
        return FusionContentSegmentClient(
            name, self._contentset_name, self._contentset_id, self._client
        )

    def get_segment(self, name: str = "") -> FusionContentSegmentClient:
        """Get a fusion segment according to its name.

        :param name: The name of the desired fusion segment
        :raises GASSegmentError: When the required fusion segment does not exist
        :return: The desired fusion segment
        """
        if self._list_segments([name]):
            return FusionContentSegmentClient(
                name,
                self._contentset_name,
                self._contentset_id,
                self._client,
            )
        raise GASSegmentError(name)

    def upload_segment_object(
        self,
        segment: FusionSegment,
        *,
        jobs: int = 1,
        skip_uploaded_files: bool = False,
    ) -> FusionContentSegmentClient:
        """Upload a `FusionSegment` to the contentset,
        This function will upload all info contains in the input `FusionSegment` object,
        which includes:
        - Create a segment using the name of input `FusionSegment`
        - Upload all `Sensor` in the segment to the contentset
        - Upload all `Frame` in the segment to the contentset

        :param segment: The `Segment` object needs to be uploaded
        :param jobs: The number of the max workers in multithread upload
        :param skip_uploaded_files: Set it to `True` to skip the uploaded files
        :return: The client used for uploading the data in the `FusionSegment`
        """
        segment_client = self.get_or_create_segment(segment.name)
        sensors = segment.get_sensors()
        for sensor in sensors.values():
            segment_client.upload_sensor_object(sensor)

        segment_filter: Iterable[Tuple[int, Frame]]
        if skip_uploaded_files:
            segment_filter = self._existing_frame_generator(segment_client, segment)
        else:
            segment_filter = enumerate(segment)

        multithread_upload(
            lambda args: segment_client.upload_frame_object(args[1], args[0]),
            segment_filter,
            jobs=jobs,
        )

        return segment_client

    @staticmethod
    def _existing_frame_generator(
        segment_client: FusionContentSegmentClient,
        segment: FusionSegment,
    ) -> Generator[Tuple[int, Frame], None, None]:
        done_frame_dict = (
            segment_client._list_frame_objects_dict()  # pylint: disable=protected-access
        )
        for i, frame in enumerate(segment):
            if i in done_frame_dict:
                remote_frame, frame_id = done_frame_dict[i]
                if len(remote_frame) == len(frame):
                    continue

                segment_client._delete_frames(frame_id)  # pylint: disable=protected-access

            yield i, frame

#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines some exceptions about TensorBay."""

from requests import RequestException
from requests.models import Response

from .log import dump_request_and_response


class GASException(Exception):
    """This is the parent class to the following specified error classes."""


class GASRequestError(GASException):
    """Through this class which inherits from GASException,
    we can raise GASRequestError specifically.

    :param error: RequestException message
    """

    def __init__(self, error: RequestException) -> None:
        super().__init__()
        self._error = error

    def __str__(self) -> str:
        return str(self._error)


class GASResponseException(GASException):
    """Through this class which inherits from GASException,
    we can raise GASResponseException specifically.
    This is the parent class to response-related errors.

    :param response: The response of the request
    """

    def __init__(self, response: Response) -> None:
        super().__init__()
        self._response = response
        self.status_code = response.status_code

    def __str__(self) -> str:
        return dump_request_and_response(self._response)


class GASResponseError(GASResponseException):
    """Through this class which inherits from GASError,
    we can raise GASResponseError specifically.

    :param response: The response of the request
    """


class GASOSSError(GASResponseException):
    """Exception for OSS response error

    :param response: The response of the request
    """

    def __init__(self, response: Response) -> None:
        super().__init__(response)
        response_json = response.json()
        self.status = response_json["status"]


class GASTensorBayError(GASResponseException):
    """Exception for graviti TensorBay response error

    :param response: The response of the request
    """

    def __init__(self, response: Response) -> None:
        super().__init__(response)
        response_json = response.json()
        self.code = response_json["code"]
        self.message = response_json["message"]
        self.success = response_json["success"]


class GASDatasetError(GASException):
    """Through this class which inherits from GASException,
    we can raise GASDatasetError specifically.

    :param dataset_name: The name of the missing dataset
    """

    def __init__(self, dataset_name: str) -> None:
        super().__init__()
        self._dataset_name = dataset_name

    def __str__(self) -> str:
        return f"Dataset '{self._dataset_name}' does not exist"


class GASDatasetTypeError(GASException):
    """Through this class which inherits from GASException,
    we can raise GASDatasetTypeError specifically.

    :param dataset_name: The name of the dataset whose requested type is wrong
    :param is_fusion: whether the dataset is a fusion dataset
    """

    def __init__(self, dataset_name: str, is_fusion: bool) -> None:
        super().__init__()
        self._dataset_name = dataset_name
        self._is_fusion = is_fusion

    def __str__(self) -> str:
        return (
            f"Dataset '{self._dataset_name}' is {'' if self._is_fusion else 'not '}a fusion dataset"
        )


class GASLabelsetError(GASException):
    """Through this class which inherits from GASException,
    we can raise GASLabelsetError specifically.

    :param labelset_id: The labelset ID of the missing labelset
    """

    def __init__(self, labelset_id: str) -> None:
        super().__init__()
        self._labelset_id = labelset_id

    def __str__(self) -> str:
        return f"Labelset '{self._labelset_id}' does not exist"


class GASLabelsetTypeError(GASException):
    """Through this class which inherits from GASException,
    we can raise GASLabelsetTypeError specifically.

    :param labelset_id: The ID of the labelset whose requested type is wrong
    :param is_fusion: whether the labelset is a fusion labelset
    """

    def __init__(self, labelset_id: str, is_fusion: bool) -> None:
        super().__init__()
        self._labelset_id = labelset_id
        self._is_fusion = is_fusion

    def __str__(self) -> str:
        return (
            f"Labelset '{self._labelset_id}' is "
            f"{'' if self._is_fusion else 'not '}a fusion labelset"
        )


class GASSegmentError(GASException):
    """Through this class which inherits from GASException,
    we can raise GASSegmentError specifically.

    :param segment_name: The name of the missing segment_name
    """

    def __init__(self, segment_name: str) -> None:
        super().__init__()
        self._segment_name = segment_name

    def __str__(self) -> str:
        return f"Segment '{self._segment_name}' does not exist"


class GASPathError(GASException):
    """Throw this error when remote path does not follow linux style.

    :param remote_path: the invalid remote path
    """

    def __init__(self, remote_path: str) -> None:
        super().__init__()
        self._remote_path = remote_path

    def __str__(self) -> str:
        return f'Invalid path: "{self._remote_path}"\nRemote path should follow linux style.'


class GASFrameError(GASException):
    """Throw this error when the uploading frame has no timestamp and no frame_index """

    def __str__(self) -> str:
        return "Either data.timestamp or frame_index is required to sort frame in TensorBay"

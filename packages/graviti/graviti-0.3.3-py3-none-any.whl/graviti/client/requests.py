#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file define class Client and function read_data_from_file.
"""

import logging
import time
from concurrent.futures import FIRST_EXCEPTION, ThreadPoolExecutor, wait
from typing import Any, Callable, Dict, Iterable, Optional, TypeVar
from urllib.parse import urljoin

import requests

from .exceptions import GASOSSError, GASRequestError, GASResponseError, GASTensorBayError
from .log import dump_request_and_response

logger = logging.getLogger(__name__)


class Config:  # pylint: disable=too-few-public-methods
    """This is a base class defining the concept of Post Config

    :param max_retries: max retries of the post request
    :param timeout: timeout of the post request
    :param is_intern: whether the post request is from intern
    """

    def __init__(self, max_retries: int = 3, timeout: int = 15, is_intern: bool = False) -> None:

        self.max_retries = max_retries
        self.timeout = timeout
        self._is_intern = is_intern

    @property
    def is_intern(self) -> bool:
        """Return whether the post request is from intern.

        :return: whether the post request is from intern
        """
        return self._is_intern


default_config = Config()


class Client:
    """This is a base class defining the concept of Client,
    which contains functions to send post to content store and labelset store

    :param access_key: user's access key
    :param url: the url of the graviti gas website
    """

    _DEFAULT_URL_CN = "https://gas.graviti.cn/"
    _DEFAULT_URL_COM = "https://gas.graviti.com/"

    def __init__(self, access_key: str, url: str = "") -> None:
        if access_key.startswith("Accesskey-"):
            url = url if url else Client._DEFAULT_URL_CN
        elif access_key.startswith("ACCESSKEY-"):
            url = url if url else Client._DEFAULT_URL_COM
        else:
            raise TypeError("Wrong accesskey format!")

        self.gateway_url = urljoin(url, "gatewayv2/")
        self.access_key = access_key

        self._content_store = urljoin(self.gateway_url, "content-store/")
        self._label_store = urljoin(self.gateway_url, "label-store/")
        self._tensorbay_dataset = urljoin(self.gateway_url, "tensorbay-dataset/")

    def contentset_post(self, method: str, post_data: Dict[str, Any]) -> Any:
        """Send a POST request to the TensorBay content-store

        :param method: The method of the request
        :param post_data: Json data to send in the body of the request
        :return: Response of the request
        """
        url = urljoin(self._content_store, method)
        return post(url, json_data=post_data, access_key=self.access_key)

    def labelset_post(self, method: str, post_data: Dict[str, Any]) -> Any:
        """Send a POST request to the TensorBay label-store

        :param method: The method of the request
        :param post_data: Json data to send in the body of the request
        :return: Response of the request
        """
        url = urljoin(self._label_store, method)
        return post(url, json_data=post_data, access_key=self.access_key)

    def dataset_post(self, method: str, post_data: Dict[str, Any]) -> Any:
        """Send a POST request to the TensorBay Dataset API

        :param method: The method of the request
        :param post_data: Json data to send in the body of the request
        :return: Response of the request
        """
        url = urljoin(self._tensorbay_dataset, method)
        return post(url, json_data=post_data, access_key=self.access_key)


T = TypeVar("T")  # pylint: disable=invalid-name


def multithread_upload(
    function: Callable[[T], None],
    arguments: Iterable[T],
    *,
    jobs: int = 1,
) -> None:
    """multithread upload framework

    :param function: The upload function
    :param arguments: The arguments of the upload function
    :param jobs: The number of the max workers in multithread upload
    """
    with ThreadPoolExecutor(jobs) as executor:
        futures = []
        for argument in arguments:
            futures.append(executor.submit(function, argument))

        done, not_done = wait(futures, return_when=FIRST_EXCEPTION)
        for future in not_done:
            future.cancel()
        for future in done:
            future.result()


def post(
    url: str,
    *,
    data: Optional[bytes] = None,
    json_data: Optional[Dict[str, Any]] = None,
    content_type: Optional[str] = None,
    max_retries: Optional[int] = None,
    timeout: Optional[int] = None,
    access_key: Optional[str] = None,
) -> Any:
    """Send a POST requests

    :param url: URL for the request
    :param data: bytes data to send in the body of the request
    :param json_data: json data to send in the body of the request
    :param content_type: Content-Type to send in the header of the request
    :param max_retries: max_retries to send in the header of the request
    :param timeout: timeout to send in the header of the request
    :raises GASRequestError: When post request failed
    :raises GASResponseError: When response.ok is False
    :raises GASTensorBayError: When response content 'success' is False
    :raises GASOSSError: When response is return by AliyunOSS and content 'status' is not 'OK'
    :return: response of the request
    """

    if not max_retries:
        max_retries = default_config.max_retries
    if not timeout:
        timeout = default_config.timeout

    headers: Dict[str, str] = {}
    if access_key:
        headers["X-Token"] = access_key
    if content_type:
        headers["Content-Type"] = content_type

    # retry_strategy = Retry(
    #     total=max_retries,
    #     status_forcelist=[429, 500, 502, 503, 504],
    #     method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
    # )
    # adapter = TimeoutHTTPAdapter(max_retries=retry_strategy)
    # http = requests.Session()
    # http.mount("https://", adapter)
    # http.mount("http://", adapter)
    # response = http.post(url, data=data, json=json_data, headers=headers)
    # return _parser_response(response)

    for i in range(max_retries):
        try:
            response = requests.post(
                url, data=data, json=json_data, headers=headers, timeout=timeout
            )
            parser_response = _parser_response(response)
            return parser_response
        except (requests.RequestException, GASResponseError) as error:
            if i == max_retries - 1:
                raise error
            logger.warning(error)
            logger.warning("retrying: %d/%d", i + 1, max_retries)
            time.sleep(3)


def get(url: str, params: Dict[str, Any]) -> Any:
    """Send a GET requests

    :param url: URL for the request
    :param params: Dictionary to send in the query string for the `Request`
    :raises GASRequestError: When post request failed
    :raises GASResponseError: When response.ok is False
    :raises GASTensorBayError: When response content 'success' is False
    :return: response of the request
    """
    try:
        response = requests.get(url, params=params, headers={"Accept": "application/json"})
    except requests.RequestException as error:
        raise GASRequestError(error)

    return _parser_response(response)


def _parser_response(response: requests.Response) -> Any:
    if response.status_code != 200:
        raise GASResponseError(response)

    if response.headers.get("Server", None) == "AmazonS3":
        result: Dict[str, Any] = {
            "Server": response.headers["Server"],
            "etag": response.headers["etag"],
            "versionId": response.headers.get("x-amz-version-id", ""),
        }

        logger.debug(dump_request_and_response(response))
        return result

    content_type = response.headers["Content-Type"]
    if not content_type.startswith("application/json"):
        logger.debug(dump_request_and_response(response))
        return response.content

    result = response.json()

    if response.headers.get("Server", None) == "AliyunOSS":
        if result["status"] != "OK":
            raise GASOSSError(response)
        logger.debug(dump_request_and_response(response))
        return result

    if not result["success"]:
        raise GASTensorBayError(response)

    logger.debug(dump_request_and_response(response))
    return result["data"]

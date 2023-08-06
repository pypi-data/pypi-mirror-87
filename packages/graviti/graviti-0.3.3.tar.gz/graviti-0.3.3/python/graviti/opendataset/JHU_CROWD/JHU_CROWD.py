#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file define JHU_CROWD Dataloader"""

import glob
import os
from typing import Dict, Generator

from ...dataset import Data, Dataset
from ...label import Classification, LabeledBox2D, LabelType

SEGMENT_LIST = ["train", "val", "test"]
DATASET_NAME = "JHU-CROWD++"
_OCCLUSION_MAP = {1: "visible", 2: "partial-occlusion", 3: "full-occlusion"}
_WEATHER_CONDITION_MAP = {0: "no weather degradationi", 1: "fog/haze", 2: "rain", 3: "snow"}


def JHU_CROWD(path: str) -> Dataset:
    """Load the JHU-CROWD++ Dataset to TensorBay

    :param path: the root directory of the dataset
    The file structure should be like:
    <path>
        train/
            images/
                0000.jpg
                ...
            gt/
                0000.txt
                ...
            image_labels.txt
        test/
        val/

    :return: a loaded dataset
    """

    dataset = Dataset(DATASET_NAME)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables.json"))
    for segment_name in SEGMENT_LIST:
        segment = dataset.create_segment(segment_name)
        segment_path = os.path.join(path, segment_name)
        image_root_path = os.path.join(segment_path, "images")
        image_paths = glob.glob(os.path.join(image_root_path, "*.jpg"))
        if not image_paths:
            raise TypeError(f"No '.jpg' files found in {image_root_path}")
        image_paths.sort()
        image_label_map = _load_image_label(os.path.join(segment_path, "image_labels.txt"))
        for image_path in image_paths:
            data = Data(image_path)
            image_file = os.path.basename(image_path)
            label_file = image_file.replace("jpg", "txt")
            data.register_label(LabelType.BOX2D)
            for label in _load_box_label(os.path.join(segment_path, "gt", label_file)):
                data.append_label(label)
            data.append_label(image_label_map[os.path.splitext(image_file)[0]])
            segment.append(data)
    return dataset


def _load_box_label(file_path: str) -> Generator[LabeledBox2D, None, None]:
    with open(file_path) as f:
        lines = f.readlines()
    for line in lines:
        center_x, center_y, width, height, occlusion, blur = list(map(int, line.strip().split()))
        attributes = {"occlusion-level": _OCCLUSION_MAP[occlusion], "blur-level": bool(blur)}
        yield LabeledBox2D(
            x=center_x - width / 2,
            y=center_y - height / 2,
            width=width,
            height=height,
            attributes=attributes,
        )


def _load_image_label(file_path: str) -> Dict[str, Classification]:
    with open(file_path) as f:
        lines = f.readlines()
    label_map = {}
    for line in lines:
        img_index, count, scene, weather, distractor = line.strip().split(",")
        attributes = {
            "total-count": int(count),
            "scene-type": scene,
            "weather-condition": _WEATHER_CONDITION_MAP[int(weather)],
            "distractor": bool(int(distractor)),
        }
        label_map[img_index] = Classification(attributes=attributes)
    return label_map

#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file define the 17 Category Flower Dataloader"""

import glob
import os

from ...dataset import Data, Dataset
from ...label import Classification, LabelType

DATASET_NAME = "Flower17"
CATEFORIES = [
    "Daffodil",
    "Snowdrop",
    "Lily Valley",
    "Bluebell",
    "Crocus",
    "Iris",
    "Tigerlily",
    "Tulip",
    "Fritillary",
    "Sunflower",
    "Daisy",
    "Colts Foot",
    "Dandelalion",
    "Cowslip",
    "Buttercup",
    "Windflower",
    "Pansy",
]


def Flower17(path: str) -> Dataset:
    """Load the 17 Category Flower Dataset to TensorBay

    :param path: the root directory of the dataset
    The file structure should be like:
    <path>
        jpg/
            image_0001.jpg
            ...

    :return: a loaded dataset
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    image_paths = glob.glob(os.path.join(root_path, "jpg", "*.jpg"))
    if not image_paths:
        raise TypeError(f"No '.jpg' files found in {root_path}")
    image_paths.sort()

    dataset = Dataset(DATASET_NAME)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables.json"))
    segment = dataset.create_segment()

    for image_path in image_paths:
        data = Data(os.path.join(root_path, image_path))
        data.register_label(LabelType.CLASSIFICATION)

        # There are 80 images for each category
        index = int(image_path[6:11]) - 1
        data.append_label(Classification(category=CATEFORIES[index // 80]))
        segment.append(data)

    return dataset

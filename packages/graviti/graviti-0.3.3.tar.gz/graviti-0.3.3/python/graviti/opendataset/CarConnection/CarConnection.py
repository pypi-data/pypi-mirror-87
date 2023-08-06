#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file define the Car Connection Picture Dataloader"""

import os
from glob import glob
from typing import Union

from ...dataset import Data, Dataset
from ...label import Classification

DATASET_NAME = "CarConnection"

KEYS = [
    "Year",
    "MSRP",
    "Front Wheel Size (in)",
    "SAE Net Horsepower @ RPM",
    "Displacement (L)",
    "Engine Type (cylinder)",
    "Width, Max w/o mirrors (in)",
    "Height, Overall (in)",
    "Length, Overall (in)",
    "Gas Mileage (mpg)",
    "Drivetrain",
    "Passenger Capacity",
    "Passenger Doors",
    "Body Style",
]


def CarConnection(path: str) -> Dataset:
    """
    Load the Car Connection Picture Dataset to TensorBay
    :param path: the root directory of the dataset
    The file structure should be like:
    <path>
        <imagename>.jpg
        ...

    :return: a loaded dataset
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables.json"))
    segment = dataset.create_segment()

    image_paths = glob(os.path.join(root_path, "*.jpg"))
    if not image_paths:
        raise TypeError(f"No '.jpg' files found in {root_path}")
    image_paths.sort()

    for image_path in image_paths:
        data = Data(image_path)
        basename = os.path.basename(image_path)
        label = _extract_label_from_basename(basename)
        data.append_label(label)
        segment.append(data)

    return dataset


def _transfer_attribute_type(item: str) -> Union[int, str, None]:
    if item == "nan":
        return None
    if item.isnumeric():
        return int(item)

    return item


def _extract_label_from_basename(filename: str) -> Classification:
    make, model, *spec_values = filename.split("_")[:-1]

    attributes = dict(zip(KEYS, map(_transfer_attribute_type, spec_values)))

    category = ".".join((make, model))

    return Classification(attributes=attributes, category=category)

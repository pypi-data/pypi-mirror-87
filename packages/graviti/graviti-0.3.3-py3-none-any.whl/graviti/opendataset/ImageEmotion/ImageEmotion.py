#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#
# pylint: disable=invalid-name

"""This file handles with the ImageEmotion dataset"""

import csv
import os
from glob import glob

from ...dataset import Data, Dataset
from ...label import Classification

DATASET_NAME_ABSTRACT = "ImageEmotionAbstract"
DATASET_NAME_ARTPHOTO = "ImageEmotionArtphoto"


def ImageEmotionAbstract(path: str) -> Dataset:
    """ImageEmotionAbstract open dataset dataloader

    :param path: Path to ImageEmotionAbstract dataset
    The file structure should be like:
    <path>
        ABSTRACT_groundTruth.csv
        abstract_xxxx.jpg
        ...

    :return: load `Dataset` object
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME_ABSTRACT)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables_abstract.json"))
    segment = dataset.create_segment()

    csv_path = os.path.join(root_path, "ABSTRACT_groundTruth.csv")
    with open(csv_path, "r") as file:
        reader = csv.DictReader(file)
        reader.fieldnames = [
            field.strip("'") for field in reader.fieldnames  # type:ignore[union-attr]
        ]

        for row in reader:
            image_path = os.path.join(root_path, row.pop("").strip("'"))

            data = Data(image_path)

            values = {key: int(value) for key, value in row.items()}
            label = Classification(attributes=values)

            data.append_label(label)
            segment.append(data)

    return dataset


def ImageEmotionArtphoto(path: str) -> Dataset:
    """ImageEmotionArtphoto open dataset dataloader

    :param path: Path to ImageEmotionArtphoto dataset
    The file structure should be like:
    <path>
        <filename>.jpg
        ...

    :return: load `Dataset` object
    """
    root_path = os.path.abspath(os.path.expanduser(path))

    dataset = Dataset(DATASET_NAME_ARTPHOTO)
    dataset.load_label_tables(os.path.join(os.path.dirname(__file__), "labeltables_artphoto.json"))
    segment = dataset.create_segment()

    image_paths = glob(os.path.join(root_path, "*.jpg"))
    if not image_paths:
        raise TypeError(f"No '.jpg' files found in {root_path}")
    image_paths.sort()

    for image_path in image_paths:
        image_category = os.path.basename(image_path).split("_", 1)[0]

        data = Data(image_path)

        label = Classification(category=image_category)

        data.append_label(label)
        segment.append(data)

    return dataset

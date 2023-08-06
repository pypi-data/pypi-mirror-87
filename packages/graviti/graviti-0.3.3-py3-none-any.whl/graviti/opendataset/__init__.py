#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""OpenDataset dataloader collections."""

from .CarConnection import CarConnection
from .CoinImage import CoinImage
from .DownsampledImagenet import DownsampledImagenet
from .Flower17 import Flower17
from .ImageEmotion import ImageEmotionAbstract, ImageEmotionArtphoto
from .KylbergTexture import KylbergTexture
from .LISATrafficLight import LISATrafficLight

__all__ = [
    "CarConnection",
    "CoinImage",
    "DownsampledImagenet",
    "Flower17",
    "ImageEmotionAbstract",
    "ImageEmotionArtphoto",
    "KylbergTexture",
    "LISATrafficLight",
]

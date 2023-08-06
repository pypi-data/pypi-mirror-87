#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains invalidation which may be found in the dataset."""

from typing import Any, Union

from .location import (
    DataLocationForDataset,
    DataLocationForFusionDataset,
    LabelLocation,
    SegmentLocation,
)

DataLocationType = Union[DataLocationForDataset, DataLocationForFusionDataset]


class Invalidation:
    """This class defines the invalidation."""

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return "Info: Invalidation"


class DatasetInvalidation(Invalidation):
    """This class defines the invalidation in dataset."""

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return "Info: Dataset Invalidation"


class LabelTableInvalidation(Invalidation):
    """This class defines the invalidation in label table."""

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return "Info: LabelTable Invalidation"


class SegmentInvalidation(Invalidation):
    """This class defines the invalidation in segment.

    :param location: the location of segment in dataset(either Dataset or FusionDataset)
    """

    def __init__(self, location: SegmentLocation) -> None:
        self._location = location

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return "Location: '{self._location}' Info: Segment Invalidation"


class DataInvalidation(Invalidation):
    """This class defines the invalidation in data.

    :param location: the location of data in dataset(either Dataset or FusionDataset)
    """

    def __init__(self, location: DataLocationType) -> None:
        self._location = location

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return f"Location: '{self._location}' Info: Data Invalidation"


# FileInvalidation
class FileNotExistInvalidation(DataInvalidation):
    """This class defines the invalidation
    --"Files does not exist according to the given path".

    :param location: the location of data in dataset(either Dataset or FusionDataset)
    """

    def __init__(self, location: DataLocationType) -> None:
        DataInvalidation.__init__(self, location)

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return (
            f"Location: '{self._location}' Info: Files does not exist according to the given path"
        )


# LabelInvalidation
class CategoryNotExistInvalidation(DataInvalidation):
    """This class defines the invalidation
    --"Category cannot be found in the label table".

    :param location: the location of data in dataset(either Dataset or FusionDataset)
    :param label_location: the location of label in data
    """

    def __init__(self, location: DataLocationType, label_location: LabelLocation) -> None:
        super().__init__(location)
        self._label_location = label_location

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return (
            f"Location: '{self._location} {self._label_location}' "
            f"Info: Category cannot be found in the label table"
        )


class CategoryIsNoneInvalidation(DataInvalidation):
    """This class defines the invalidation
    --"Category cannot be None".

    :param location: the location of data in dataset(either Dataset or FusionDataset)
    :param label_location: the location of label in data
    """

    def __init__(self, location: DataLocationType, label_location: LabelLocation) -> None:
        super().__init__(location)
        self._label_location = label_location

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return f"Location: '{self._location} {self._label_location}' Info: Category cannot be None"


class AttributeNotExistInvalidation(DataInvalidation):
    """This class defines the invalidation --"Attribute cannot be found in the label table".

    :param location: the location of data in dataset(either Dataset or FusionDataset)
    :param label_location: the location of label in data
    :param attribute_name: the name of attribute in label
    """

    def __init__(
        self, location: DataLocationType, label_location: LabelLocation, attribute_name: str
    ) -> None:
        super().__init__(location)
        self._label_location = label_location
        self._attribute_name = attribute_name

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return (
            f"Location: '{self._location} {self._label_location}' "
            f"Info: Attribute does not exist(attribute_name: {self._attribute_name})"
        )


class AttributeValueOutOfBoundInvalidation(DataInvalidation):
    """This class defines the invalidation
    --"Value in the attribute is out of bound".

    :param location: the location of data in dataset(either Dataset or FusionDataset)
    :param label_location: the location of label in data
    :param attribute_name: the name of attribute in label
    :param attribute_key: the key of attribute according to label table
    :param attribute_name: the value of attribute in label
    """

    def __init__(
        self,
        location: DataLocationType,
        label_location: LabelLocation,
        attribute_name: str,
        attribute_key: str,
        attribute_value: Any,
    ) -> None:
        super().__init__(location)
        self._label_location = label_location
        self._attribute_name = attribute_name
        self._attribute_key = attribute_key
        self._attribute_value = attribute_value

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return (
            f"Location: '{self._location} {self._label_location}' "
            f"Info: Value in the attribute is out of bound"
            f"(attribute_name: {self._attribute_name}, "
            f"value: {self._attribute_value}, key: {self._attribute_key})"
        )


class AttributeValueTypeInvalidation(DataInvalidation):
    """This class defines the invalidation
    --"Value in the attribute does not match with type in the label table".

    :param location: the location of data in dataset(either Dataset or FusionDataset)
    :param label_location: the location of label in data
    :param attribute_name: the name of attribute in label
    :param attribute_name: the value of attribute in label
    """

    def __init__(
        self,
        location: DataLocationType,
        label_location: LabelLocation,
        attribute_name: str,
        attribute_value: Any,
        attribute_type: Any,
    ) -> None:
        super().__init__(location)
        self._label_location = label_location
        self._attribute_name = attribute_name
        self._attribute_value = attribute_value
        self._attribute_type = attribute_type

    def find_invalidation(self) -> None:
        """Find invalidation."""

    def __str__(self) -> str:
        return (
            f"Location: '{self._location} {self._label_location}' "
            f"Info: Value in the attribute does not match with type in the label table"
            f"(attribute_name: {self._attribute_name}, "
            f"value: {self._attribute_value}, type: {self._attribute_type})"
        )

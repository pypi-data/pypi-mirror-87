#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file contains checkhealth related functions."""

import os
from typing import Any, Callable, Dict, Generator, List, Optional, Tuple, Union

from ..label.label import Classification, Label, LabelType
from ..label.label_table import AttributeInfo, AttributeType, LabelTables
from .data import Data
from .dataset import Dataset, FusionDataset
from .invalidation import (
    AttributeNotExistInvalidation,
    AttributeValueOutOfBoundInvalidation,
    AttributeValueTypeInvalidation,
    CategoryIsNoneInvalidation,
    CategoryNotExistInvalidation,
    FileNotExistInvalidation,
)
from .location import DataLocationForDataset, DataLocationForFusionDataset, LabelLocation

DataLocationType = Union[DataLocationForDataset, DataLocationForFusionDataset]
FileReportInvalidationType = FileNotExistInvalidation
LabelReportInvalidationType = Union[
    AttributeValueTypeInvalidation,
    AttributeValueOutOfBoundInvalidation,
    AttributeNotExistInvalidation,
    CategoryIsNoneInvalidation,
    CategoryNotExistInvalidation,
]


class HealthReport:
    """This class defines a health report to a dataset in which invalidation is put"""

    def __init__(self) -> None:
        self._logging_max: int = 10
        self._file_report: List[FileReportInvalidationType] = []
        self._label_report: List[LabelReportInvalidationType] = []

    @property
    def file_report(self) -> List[FileReportInvalidationType]:
        """Return list of invalidation related to file check of the dataset
        (either Dataset or FusionDataset).

        :return: list of invalidation related to file check of the dataset
        (either Dataset or FusionDataset)
        """
        return self._file_report

    @property
    def label_report(self) -> List[LabelReportInvalidationType]:
        """Return list of invalidation related to label check of the dataset
        (either Dataset or FusionDataset).

        :return: list of invalidation related to label check of the dataset
        (either Dataset or FusionDataset)
        """
        return self._label_report

    def add_to_file_report(self, invalidation: FileReportInvalidationType) -> None:
        """Insert the invalidation into the report and
        restrict the count of logging the invalidation.

        :param invalidation: invalidation related to file check
        """
        self._file_report.append(invalidation)
        self._check_logging_count(self._file_report)

    def add_to_label_report(self, invalidation: LabelReportInvalidationType) -> None:
        """Insert the error into the report and
        restrict the count of logging the invalidation.

        :param invalidation: invalidation related to label check
        """
        self._label_report.append(invalidation)
        self._check_logging_count(self._label_report)

    def _check_logging_count(self, report: List[Any]) -> None:
        """Restrict the count of logging the invalidation.

        :param report: list of invalidation in terms of the check service which is implemented
        """
        report_length = len(report)
        if report_length <= self._logging_max:
            print(report[-1])
        if report_length == self._logging_max:
            print("more info shown in the report")


def checkhealth(dataset: Union[Dataset, FusionDataset]) -> HealthReport:
    """Check if a dataset(either Dataset or FusionDataset) is legal.

    :param dataset: Union[Dataset, FusionDataset]
    :return HealthReport
    """
    health_report = HealthReport()
    check_file_exist(dataset, health_report)
    check_labels(dataset, health_report)
    return health_report


def check_file_exist(dataset: Union[Dataset, FusionDataset], health_report: HealthReport) -> None:
    """Check if files shown in data exist.

    :param dataset: Union[Dataset, FusionDataset]
    :param health_report: HealthReport
    """
    print("- Check file existence start")

    # identify the dataset type
    func: Union[
        Callable[[Dataset], Generator[Tuple[Data, DataLocationForDataset], None, None]],
        Callable[[FusionDataset], Generator[Tuple[Data, DataLocationForFusionDataset], None, None]],
    ]
    if isinstance(dataset, Dataset):
        func = _traverse_data_in_dataset
    elif isinstance(dataset, FusionDataset):
        func = _traverse_data_in_fusion_dataset
    else:
        raise TypeError("It is not a DatasetBase type")

    # traverse data in the dataset
    data_iter = func(dataset)  # type: ignore[arg-type]
    for data, location in data_iter:
        _check_file_exist(data, health_report, location)

    # check if there is invalidation in file_report
    if len(health_report.file_report) != 0:
        print("FAIL")
    else:
        print("PASS")
    print("--------------------------")


def check_labels(dataset: Union[Dataset, FusionDataset], health_report: HealthReport) -> None:
    """Check if labels shown in data are legal.

    :param dataset: Union[Dataset, FusionDataset]
    :param health_report: HealthReport
    """
    print("- Check Labels start")

    label_tables = dataset.label_tables
    if not label_tables:
        print("No label tables")
        return

    # identify the dataset type
    func: Union[
        Callable[[Dataset], Generator[Tuple[Data, DataLocationForDataset], None, None]],
        Callable[[FusionDataset], Generator[Tuple[Data, DataLocationForFusionDataset], None, None]],
    ]
    if isinstance(dataset, Dataset):
        func = _traverse_data_in_dataset
    elif isinstance(dataset, FusionDataset):
        func = _traverse_data_in_fusion_dataset
    else:
        raise TypeError("It is not a DatasetBase type")

    # traverse data in the dataset
    data_iter = func(dataset)  # type: ignore[arg-type]
    for data, location in data_iter:
        _check_labels(data, label_tables, health_report, location)

    # check if there is invalidation in file_report
    if len(health_report.label_report) != 0:
        print("FAIL")
    else:
        print("PASS")
    print("--------------------------")


def _traverse_data_in_dataset(
    dataset: Dataset,
) -> Generator[Tuple[Data, DataLocationForDataset], None, None]:
    """Data traversal in the dataset(Dataset).

    :param dataset: Dataset
    :yield sequence of data and the location of data(Dataset)
    """
    for segment_index, segment in enumerate(dataset):
        for data_index, data in enumerate(segment):
            location = DataLocationForDataset(segment_index=segment_index, data_index=data_index)
            yield data, location


def _traverse_data_in_fusion_dataset(
    fusion_dataset: FusionDataset,
) -> Generator[Tuple[Data, DataLocationForFusionDataset], None, None]:
    """Data traversal in the dataset(FusionDataset).

    :param fusion_dataset: FusionDataset
    :yield sequence of data and the location of data(FusionDataset)
    """
    for segment_index, segment in enumerate(fusion_dataset):
        for frame_index, frame in enumerate(segment):
            for sensor_name, data in frame.items():
                location = DataLocationForFusionDataset(
                    segment_index=segment_index, frame_index=frame_index, sensor_name=sensor_name
                )
                yield data, location


def _check_file_exist(
    data: Data, health_report: HealthReport, data_location: DataLocationType
) -> None:
    """Realize the function of "check_file_exist".

    :param data: each single data in dataset(either Dataset or FusionDataset)
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    """
    local_path = data.local_path
    if not os.path.isfile(local_path):
        invalidation = FileNotExistInvalidation(data_location)
        health_report.add_to_file_report(invalidation)


def _check_labels(
    data: Data,
    label_tables: LabelTables,
    health_report: HealthReport,
    data_location: DataLocationType,
) -> None:
    """Realize the function of "check_labels".

    :param data: each single data in dataset(either Dataset or FusionDataset)
    :param label_tables: label tables of dataset(either Dataset or FusionDataset)
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    """
    for label_type, labels in data.items():
        if not isinstance(labels, Classification):
            for label_index, label in enumerate(labels):
                label_location = LabelLocation(label_type, label_index)
                _get_and_check_category_and_attributes(
                    label, label_tables, health_report, data_location, label_location
                )
        else:
            label_location = LabelLocation(label_type, 1)
            _get_and_check_category_and_attributes(
                labels, label_tables, health_report, data_location, label_location
            )


def _get_and_check_category_and_attributes(
    label: Label,
    label_tables: LabelTables,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Get category and attributes and check if they are legal.

    :param label: each label of data in dataset(either Dataset or FusionDataset)
    :param label_tables: label tables of dataset(either Dataset or FusionDataset)
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """

    category = label.category
    attributes = label.attributes
    if label_location.label_type != LabelType.SENTENCE:
        _check_category_legal(category, label_tables, health_report, data_location, label_location)
    _check_attributes_legal(
        category, attributes, label_tables, health_report, data_location, label_location
    )


def _check_attributes_legal(
    category: Optional[str],
    attributes: Optional[Dict[str, Any]],
    label_tables: LabelTables,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Check if attributes of single label are legal.

    :param category: category of label in data
    :param attributes: attributes of label in data
    :param label_tables: label tables of dataset(either Dataset or FusionDataset)
    :param health_report: LabelType
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """
    if not attributes:
        return

    for name, value in attributes.items():
        attribute_in_label_table = label_tables[label_location.label_type].attributes.get(name)

        if not attribute_in_label_table:
            attribute_not_exist_invalidation = AttributeNotExistInvalidation(
                data_location, label_location, name
            )
            health_report.add_to_label_report(attribute_not_exist_invalidation)
            continue

        _check_attribute_parent_categories_legal(
            attribute_in_label_table, category, health_report, data_location, label_location
        )

        _check_attribute_value_legal(
            attribute_in_label_table, value, health_report, data_location, label_location
        )


def _check_attribute_parent_categories_legal(
    attribute_in_label_table: AttributeInfo,
    category: Optional[str],
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Check if single attribute of data is legal parent_categories.

    :param attribute_in_label_table: single attribute in the label
    :param category: category of label in data
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """
    if attribute_in_label_table.parent_categories:
        if not category:
            pass

        elif category not in attribute_in_label_table.parent_categories:
            attribute_not_exist_invalidation = AttributeNotExistInvalidation(
                data_location, label_location, attribute_in_label_table.name
            )
            health_report.add_to_label_report(attribute_not_exist_invalidation)


def _check_attribute_value_legal(
    attribute_in_label_table: AttributeInfo,
    value: Any,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Check if attribute is legal in term of value factors.

    :param attribute_in_label_table: single attribute in the label table
    :param value: value of attribute in data
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """
    if not attribute_in_label_table.is_array:
        _check_simple_attribute_value_legal(
            attribute_in_label_table, value, health_report, data_location, label_location
        )
    else:
        if not isinstance(value, list):
            attribute_value_type_invalidation = AttributeValueTypeInvalidation(
                data_location, label_location, attribute_in_label_table.name, value, "not list"
            )
            health_report.add_to_label_report(attribute_value_type_invalidation)

        for each_value in value:
            _check_simple_attribute_value_legal(
                attribute_in_label_table,
                each_value,
                health_report,
                data_location,
                label_location,
            )


def _check_simple_attribute_value_legal(
    attribute_in_label_table: AttributeInfo,
    value: Any,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Check if simple value in attribute is legal

    :param attribute_in_label_table: single attribute in the label
    :param value: single value in the single attribute
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """
    _check_attribute_type_legal(
        attribute_in_label_table, value, health_report, data_location, label_location
    )
    _check_attribute_enum_legal(
        attribute_in_label_table, value, health_report, data_location, label_location
    )
    _check_attribute_maximum_legal(
        attribute_in_label_table, value, health_report, data_location, label_location
    )
    _check_attribute_minimum_legal(
        attribute_in_label_table, value, health_report, data_location, label_location
    )


def _check_attribute_type_legal(
    attribute_in_label_table: AttributeInfo,
    value: Any,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Check if value of single attribute of data is legal in term of "type".

    :param attribute_in_label_table: single attribute in the label
    :param value: single value in the single attribute
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """
    if attribute_in_label_table.attribute_type:
        if not isinstance(attribute_in_label_table.attribute_type, list):
            if attribute_in_label_table.attribute_type.value != AttributeType.instance:
                if not isinstance(value, attribute_in_label_table.attribute_type.value):
                    attribute_value_type_invalidation = AttributeValueTypeInvalidation(
                        data_location,
                        label_location,
                        attribute_in_label_table.name,
                        value,
                        attribute_in_label_table.attribute_type.value,
                    )
                    health_report.add_to_label_report(attribute_value_type_invalidation)
            else:
                if not isinstance(value, (str, int)):
                    attribute_value_type_invalidation = AttributeValueTypeInvalidation(
                        data_location,
                        label_location,
                        attribute_in_label_table.name,
                        value,
                        attribute_in_label_table.attribute_type.value,
                    )
                    health_report.add_to_label_report(attribute_value_type_invalidation)
        else:
            attribute_types_in_label_table: List[Any] = []
            for single_type in attribute_in_label_table.attribute_type:
                if single_type.value != "instance":
                    attribute_types_in_label_table.append(single_type.value)
                else:
                    attribute_types_in_label_table.append(str)
                    attribute_types_in_label_table.append(int)
            all_types = tuple(attribute_types_in_label_table)

            if not isinstance(value, all_types):
                attribute_value_type_invalidation = AttributeValueTypeInvalidation(
                    data_location, label_location, attribute_in_label_table.name, value, all_types
                )
                health_report.add_to_label_report(attribute_value_type_invalidation)


def _check_attribute_enum_legal(
    attribute_in_label_table: AttributeInfo,
    value: Any,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Check if value of single attribute of data is legal in term of "enum".

    :param attribute_in_label_table: single attribute in the label
    :param value: single value in the single attribute
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """
    if attribute_in_label_table.enum:
        if value not in attribute_in_label_table.enum:
            attribute_value_outbound_invalidation = AttributeValueOutOfBoundInvalidation(
                data_location, label_location, attribute_in_label_table.name, "enum", value
            )
            health_report.add_to_label_report(attribute_value_outbound_invalidation)


def _check_attribute_maximum_legal(
    attribute_in_label_table: AttributeInfo,
    value: Any,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Check if value of single attribute of data is legal in term of "maximum".

    :param attribute_in_label_table: single attribute in the label
    :param value: single value in the single attribute
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """
    if attribute_in_label_table.maximum:
        if value > attribute_in_label_table.maximum:
            attribute_value_outbound_invalidation = AttributeValueOutOfBoundInvalidation(
                data_location, label_location, attribute_in_label_table.name, "maximum", value
            )
            health_report.add_to_label_report(attribute_value_outbound_invalidation)


def _check_attribute_minimum_legal(
    attribute_in_label_table: AttributeInfo,
    value: Any,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    """Check if value of single attribute of data is legal in term of "minimum".

    :param attribute_in_label_table: single attribute in the label
    :param value: single value in the single attribute
    :param health_report: HealthReport
    :param data_location: the location of data in dataset(diverse in different dataset)
    :param label_location: the location of label in data
    """
    if attribute_in_label_table.minimum:
        if value < attribute_in_label_table.minimum:
            attribute_value_outbound_invalidation = AttributeValueOutOfBoundInvalidation(
                data_location, label_location, attribute_in_label_table.name, "minimum", value
            )
            health_report.add_to_label_report(attribute_value_outbound_invalidation)


def _check_category_legal(
    category: Optional[str],
    label_tables: LabelTables,
    health_report: HealthReport,
    data_location: DataLocationType,
    label_location: LabelLocation,
) -> None:
    if (category is None) and (not label_tables[label_location.label_type] is None):
        category_is_none_invalidation = CategoryIsNoneInvalidation(data_location, label_location)
        health_report.add_to_label_report(category_is_none_invalidation)
        return

    if (
        category
        not in label_tables[label_location.label_type].categories.keys()  # type: ignore[union-attr]
    ):
        category_not_exist_invalidation = CategoryNotExistInvalidation(
            data_location, label_location
        )
        health_report.add_to_label_report(category_not_exist_invalidation)

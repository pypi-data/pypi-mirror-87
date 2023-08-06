#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class TypeEnum and TypeClass"""

from enum import Enum
from typing import Any, Dict, Optional, Type


class TypeEnum(Enum):
    """This is a superclass for Enum which needs creating a mapping with class.
    The 'type' property is used for get the corresponding class of the Enum
    """

    __registry__: Dict["TypeEnum", Type[Any]] = {}

    def __init_subclass__(cls) -> None:
        cls.__registry__ = {}

    @property
    def type(self) -> Type[Any]:
        """Get the corresponding class"""
        return self.__registry__[self]


class TypeClass:  # pylint: disable=too-few-public-methods
    """This is a superclass for the class which needs to link with TypeEnum
    It provides the class variable 'TYPE' to access the corresponding TypeEnum
    """

    _TYPE: Any

    def __init_subclass__(cls, enum: Optional[Any] = None) -> None:
        if not enum:
            return

        cls._TYPE = enum
        enum.__registry__[enum] = cls

    @property
    def enum(self) -> Any:
        """Get the corresponding TypeEnum"""
        return self._TYPE

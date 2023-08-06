#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class TypeEnum and TypeClass"""

from enum import Enum
from typing import Any, Dict, Generic, Type, TypeVar


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


_T = TypeVar("_T", bound=TypeEnum)


class TypeClass(Generic[_T]):  # pylint: disable=too-few-public-methods
    """This is a superclass for the class which needs to link with TypeEnum
    It provides the class variable 'TYPE' to access the corresponding TypeEnum
    """

    _enum: _T

    @property
    def enum(self) -> _T:
        """Get the corresponding TypeEnum"""
        return self._enum


class TypeRegister:  # pylint: disable=too-few-public-methods
    """Decorator, used for registering TypeClass to TypeEnum

    :param enum: The corresponding TypeEnum of the TypeClass
    """

    def __init__(self, enum: TypeEnum) -> None:
        self._enum = enum

    def __call__(self, class_: Type[TypeClass[_T]]) -> Type[TypeClass[_T]]:
        class_._enum = self._enum
        self._enum.__registry__[self._enum] = class_
        return class_

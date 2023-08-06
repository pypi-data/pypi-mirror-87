#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class UserSequence, UserMutableSequence"""

from typing import (
    Any,
    Dict,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    List,
    Mapping,
    MutableMapping,
    MutableSequence,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    ValuesView,
    overload,
)

_T = TypeVar("_T")
_K = TypeVar("_K")
_V = TypeVar("_V")


class UserSequence(Sequence[_T]):
    """This class defines the concept of UserSequence,
    which contains a sequence of object.

    """

    _data: Tuple[_T, ...]

    @overload
    def __getitem__(self, index: int) -> _T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Tuple[_T, ...]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Tuple[_T, ...], _T]:
        return self._data.__getitem__(index)

    def __len__(self) -> int:
        return self._data.__len__()

    def index(self, value: _T, start: int = 0, end: int = -1) -> int:
        """
        Return first index of value.

        Raises ValueError if the value is not present.
        """
        return self._data.index(value, start, end)

    def count(self, value: _T) -> int:
        """ Return number of occurrences of value. """

        return self._data.count(value)


class UserMutableSequence(MutableSequence[_T]):
    """This class defines the concept of UserMutableSequence,
    which contains a mutable sequence of object.

    """

    _data: List[_T]

    @overload
    def __getitem__(self, index: int) -> _T:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[_T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[List[_T], _T]:
        return self._data.__getitem__(index)

    @overload
    def __setitem__(self, index: int, value: _T) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[_T]) -> None:
        ...

    def __setitem__(self, index: Union[int, slice], value: Union[_T, Iterable[_T]]) -> None:
        # https://github.com/python/mypy/issues/7858
        self._data.__setitem__(index, value)  # type: ignore[index, assignment]

    def __len__(self) -> int:
        return self._data.__len__()

    def __delitem__(self, index: Union[int, slice]) -> None:
        self._data.__delitem__(index)

    def insert(self, index: int, value: _T) -> None:
        """ Insert object before index. """

        self._data.insert(index, value)

    def append(self, value: _T) -> None:
        """ Append object to the end of the list. """

        self._data.append(value)

    def clear(self) -> None:
        """ Remove all items from list. """

        self._data.clear()

    def extend(self, value: Iterable[_T]) -> None:
        """ Extend list by appending elements from the iterable. """

        self._data.extend(value)

    def reverse(self) -> None:
        """ Reverse *IN PLACE*. """

        self._data.reverse()

    def pop(self, index: int = -1) -> _T:
        """
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range.
        """
        return self._data.pop(index)

    def remove(self, value: _T) -> None:
        """
        Remove first occurrence of value.

        Raises ValueError if the value is not present.
        """
        self._data.remove(value)

    def __iadd__(self, value: Iterable[_T]) -> List[_T]:
        return self._data.__iadd__(value)


class UserMapping(Mapping[_K, _V]):
    """This class defines the concept of UserSequence,
    which contains a sequence of object.

    """

    _data: Dict[_K, _V]

    def __getitem__(self, key: _K) -> _V:
        return self._data.__getitem__(key)

    @overload
    def get(self, key: _K) -> Optional[_V]:
        ...

    @overload
    def get(self, key: _K, default: Union[_V, _T] = ...) -> Union[_V, _T]:
        ...

    def get(self, key: _K, default: Any = None) -> Any:
        """ Return the value for key if key is in the dictionary, else default. """

        return self._data.get(key, default)

    def items(self) -> ItemsView[_K, _V]:
        """ D.items() -> a set-like object providing a view on D's items """

        return self._data.items()

    def keys(self) -> KeysView[_K]:
        """ D.keys() -> a set-like object providing a view on D's keys """

        return self._data.keys()

    def values(self) -> ValuesView[_V]:
        """ D.values() -> an object providing a view on D's values """

        return self._data.values()

    def __contains__(self, key: object) -> bool:
        return self._data.__contains__(key)

    def __iter__(self) -> Iterator[_K]:
        return self._data.__iter__()

    def __len__(self) -> int:
        return self._data.__len__()


class UserMutableMapping(UserMapping[_K, _V], MutableMapping[_K, _V]):
    """This class defines the concept of UserMutableMapping,
    which contains a mapping of object.

    """

    _data: Dict[_K, _V]

    def __setitem__(self, key: _K, value: _V) -> None:
        self._data.__setitem__(key, value)

    def __delitem__(self, key: _K) -> None:
        self._data.__delitem__(key)

    def clear(self) -> None:
        """ D.clear() -> None.  Remove all items from D. """

        self._data.clear()

    @overload
    def pop(self, key: _K) -> _V:
        ...

    @overload
    def pop(self, key: _K, default: Union[_V, _T] = ...) -> Union[_V, _T]:
        ...

    def pop(self, key: _K, default: Any = object()) -> Any:
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding value.
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        return self._data.pop(key, default)

    def popitem(self) -> Tuple[_K, _V]:
        """
        Remove and return a (key, value) pair as a 2-tuple.arc

        Pairs are returned in LIFO (last-in, first-out) order.
        Raises KeyError if the dict is empty.
        """
        return self._data.popitem()

    def setdefault(self, key: _K, default: _V = None) -> _V:  # type: ignore[assignment]
        """
        Insert key with a value of default if key is not in the dictionary.

        Return the value for key if key is in the dictionary, else default.
        """
        return self._data.setdefault(key, default)

    @overload
    def update(self, __m: Mapping[_K, _V], **kwargs: _V) -> None:
        ...

    @overload
    def update(self, __m: Iterable[Tuple[_K, _V]], **kwargs: _V) -> None:
        ...

    @overload
    def update(self, **kwargs: _V) -> None:
        ...

    def update(self, __m: Any = None, **kwargs: _V) -> None:
        """
        D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
        If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
        If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
        In either case, this is followed by: for k in F:  D[k] = F[k]
        """
        self._data.update(__m, **kwargs)

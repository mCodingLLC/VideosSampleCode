from collections.abc import MutableMapping, MutableSet
from typing import TypeVar

KeyT = TypeVar('KeyT')
ValT = TypeVar('ValT')


class IdMapping(MutableMapping[KeyT, ValT]):
    """A mapping that internally stores keys by their identity id(key).

    Keys can be ANYTHING, even non-hashable objects.
    Stores strong references to all keys and values.
    When determining if IdMappings are equal, keys are compared by identity, but values are compared by ==.
    Warning: key1 == key2 does NOT imply id(key1) == id(key2), which may be confusing if your keys are e.g. ints.

    >>> not_hashable = [1, 2, 3]
    >>> mapping = IdMapping()
    >>> mapping[not_hashable] = "hello"
    >>> not_hashable in mapping
    True
    >>> mapping[not_hashable]
    'hello'
    >>> not_hashable[0] = 0 # can even mutate the keys, it doesn't matter!
    >>> mapping[not_hashable]
    'hello'
    """

    def __init__(self, *args, **kwargs):
        self._data: dict[int, tuple[KeyT, ValT]] = {}
        """id(key) -> (key, value)"""

        self.update(*args, **kwargs)

    def __getitem__(self, item):
        try:
            key, val = self._data[id(item)]
        except KeyError as exc:
            raise KeyError(item) from exc
        return val

    def __setitem__(self, key, value):
        self._data[id(key)] = (key, value)

    def __delitem__(self, key):
        try:
            del self._data[id(key)]
        except KeyError as exc:
            raise KeyError(key) from exc

    def __iter__(self):
        for key, val in self._data.values():
            yield key

    def __len__(self):
        return len(self._data)

    def __eq__(self, other):
        if not isinstance(other, IdMapping):
            return super().__eq__(other)
        if len(self) != len(other):
            return False
        for key, val in self._data.values():
            try:
                if other[key] != val:
                    return False
            except KeyError:
                return False
        return True

    def equal_keys(self, other):
        if not isinstance(other, IdMapping):
            return self.keys() == other.keys()
        return self._data.keys() == other._data.keys()

    def clear(self) -> None:
        self._data.clear()


class IdSet(MutableSet[ValT]):
    """A set that internally stores values by their identity id(value).

    Values can be ANYTHING, even non-hashable objects.
    Stores strong references to all values.
    When determining if IdSets are equal, values are compared by identity, not by using ==.
    Warning: val1 == val2 does NOT imply id(val1) == id(val2), which may be confusing if your values are e.g. ints.

    >>> not_hashable = [1, 2, 3]
    >>> seen = IdSet()
    >>> seen.add(not_hashable)
    >>> not_hashable in seen
    True
    >>> not_hashable[0] = 0 # can even mutate the values, it doesn't matter!
    >>> not_hashable in seen
    True
    """

    def __init__(self, *others):
        self._data: dict[int, ValT] = {}
        """id(key) -> value"""

        self.update(*others)

    def __contains__(self, item):
        return id(item) in self._data

    def add(self, value: ValT) -> None:
        self._data[id(value)] = value

    def discard(self, value: ValT) -> None:
        self._data.pop(id(value), None)

    def __iter__(self):
        yield from self._data.values()

    def __len__(self):
        return len(self._data)

    def __le__(self, other):
        if not isinstance(other, IdSet):
            return super().__le__(other)
        return self._data.keys() <= other._data.keys()

    def __ge__(self, other):
        if not isinstance(other, IdSet):
            return super().__ge__(other)
        return self._data.keys() >= other._data.keys()

    def clear(self) -> None:
        self._data.clear()

    def update(self, *others):
        for other in others:
            self.__ior__(other)

    def intersection_update(self, *others):
        for other in others:
            self.__iand__(other)

    def difference_update(self, *others):
        for other in others:
            self.__isub__(other)

    def symmetric_difference_update(self, other):
        self.__ixor__(other)

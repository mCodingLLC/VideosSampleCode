from __future__ import annotations

from collections.abc import Iterable, MutableMapping, Mapping
from typing import TypeVar

KT = TypeVar('KT')
VT = TypeVar('VT')


class InvertibleDict(MutableMapping[KT, VT]):
    """A invertible (one-to-one) mapping.

    Attempting to set multiple keys to the same value will raise a ValueError.

    invariant: _forward and _backward are mathematical inverses
        i.e. _forward[a] == b if and only if _backward[b] == a
    """

    __slots__ = ('_forward', '_backward')

    _forward: dict[KT, VT]
    _backward: dict[VT, KT]

    def __init__(
            self,
            forward: dict[KT, VT] | None = None,
            /, *,
            _backward: dict[VT, KT] | None = None,
    ):
        if forward is None:  # empty init
            self._forward = {}
            self._backward = {}
        elif _backward is not None:  # inverse init (private)
            self._forward = forward
            self._backward = _backward  # private param, assume correct
        else:  # user-provided forward init
            self._forward = forward
            self._backward = {value: key for key, value in self._forward.items()}
            self._check_non_invertible()

    def _check_non_invertible(self):
        if len(self._backward) != len(self._forward):
            for key, value in self._forward.items():
                other_key = self._backward[value]
                if other_key != key:
                    self._raise_non_invertible(key, other_key, value)

    def _raise_non_invertible(self, key1: KT, key2: KT, value: VT):
        raise ValueError(f"non-invertible: {key1}, {key2} both map to: {value}")

    @property
    def inv(self) -> InvertibleDict[VT, KT]:
        """A mutable view of the inverse dict."""
        return self.__class__(self._backward, _backward=self._forward)

    def __getitem__(self, item: KT) -> VT:
        return self._forward[item]

    def __setitem__(self, key: KT, value: VT):
        missing = object()
        old_key = self._backward.get(value, missing)
        if old_key is not missing and old_key != key:  # {1: "a"} -> {1: "a", 2: "a"}
            # value is already mapped to a different key
            self._raise_non_invertible(old_key, key, value)

        old_value = self._forward.get(key, missing)  # {1: "a"}/{"a": 1} -> {1: "b"}/{"b": 1}
        if old_value is not missing:
            del self._backward[old_value]

        self._forward[key] = value
        self._backward[value] = key

    def __delitem__(self, key: KT):
        value = self._forward[key]
        del self._forward[key]
        del self._backward[value]

    def __iter__(self):
        return iter(self._forward)

    def __len__(self):
        return len(self._forward)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._forward!r})"

    def clear(self) -> None:
        self._forward.clear()
        self._backward.clear()


def basic_usage_example():
    fn = InvertibleDict({1: "a", 2: "b", 3: "c"})
    print(fn)
    print(fn.inv)

    assert fn[1] == "a"
    assert fn.inv["a"] == 1

    fn.inv["d"] = 4
    assert fn[4] == "d"
    assert fn.inv["d"] == 4

    print(fn)
    print(fn.inv)

    # fn[4] = "a" # ValueError
    # InvertibleDict({1: "a", 2: "a"}) # ValueError
    # fn = InvertibleDict({1: []}) # TypeError, need hashable values


def delete_min_key(d: MutableMapping) -> None:
    if not d:
        return
    key = min(d)
    del d[key]


def delete_min_example():
    fn = InvertibleDict({1: "a", 2: "b", 3: "c"})
    print(fn)

    delete_min_key(fn)
    print(fn)

    delete_min_key(fn.inv)
    print(fn)


def isinstance_example():
    fn = InvertibleDict({1: "a", 2: "b", 3: "c"})
    assert isinstance(fn, MutableMapping)
    assert issubclass(InvertibleDict, MutableMapping)

    assert isinstance(FakeMutableMapping(), MutableMapping)
    assert issubclass(FakeMutableMapping, MutableMapping)


def deep_min(d):
    if isinstance(d, Mapping):
        return min(deep_min(v) for v in d.values())
    elif isinstance(d, Iterable):
        return min(deep_min(v) for v in d)
    else:
        return d


class MyMapping:
    ...


Mapping.register(MyMapping)


def deep_min_example():
    fn = InvertibleDict({"a": frozenset({1, 2, 3}),
                         "b": frozenset({4, 5, 6}),
                         "c": frozenset({7, 8, 9})})
    print(deep_min(fn))
    assert deep_min(fn) == 1


def main():
    basic_usage_example()
    isinstance_example()
    delete_min_example()
    deep_min_example()


if __name__ == '__main__':
    main()

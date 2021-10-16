from __future__ import annotations

import json
import textwrap
import typing
from timeit import timeit
import attr
import sys


class Code(typing.Protocol):
    name: str
    define: str
    create: str
    getattr: str | None
    setattr: str | None

    supports_mutable: bool | str
    supports_immutable: bool | str
    supports_slots: bool | str
    supports_kw_getset: bool | str
    supports_converters: bool | str
    supports_validators: bool | str
    typesafe: bool | str
    stdlib: bool | str


support_keys = [
    'supports_mutable',
    'supports_immutable',
    'supports_slots',
    'supports_defaults',
    'supports_default_factory',
    'supports_kw_getset',
    'supports_converters',
    'supports_validators',
    'typesafe',
    'stdlib',
]


class TupleCode:
    name = 'tuple'
    define = "n, f, s = 42, 4.5, 'hello'"
    create = "x = n, f, s"
    getattr = "y = x[0]"
    setattr = None

    supports_mutable = False
    supports_immutable = True
    supports_slots = True
    supports_defaults = False
    supports_default_factory = False
    supports_kw_getset = False
    supports_converters = False
    supports_validators = False
    typesafe = False
    stdlib = True


class CollectionsNamedTupleCode:
    name = 'namedtuple'
    define = textwrap.dedent("""
        from collections import namedtuple
        T = namedtuple('T', ['n', 'f', 's'])
    """)
    create = "x = T(42, 4.5, 'hello')"
    getattr = "y = x[0]"
    setattr = None

    supports_mutable = False
    supports_immutable = True
    supports_slots = True
    supports_defaults = True
    supports_default_factory = False
    supports_kw_getset = True
    supports_converters = False
    supports_validators = False
    typesafe = False
    stdlib = True


class TypingNamedTupleCode:
    name = 'NamedTuple'
    define = textwrap.dedent("""
        from typing import NamedTuple
        class T(NamedTuple):
            n: int
            f: float
            s: str
    """)
    create = "x = T(42, 4.5, 'hello')"
    getattr = "y = x[0]"
    setattr = None

    supports_mutable = False
    supports_immutable = True
    supports_slots = True
    supports_defaults = True
    supports_default_factory = False
    supports_kw_getset = True
    supports_converters = False
    supports_validators = False
    typesafe = True
    stdlib = True


class DataClassCode:
    name = 'dataclass'
    define = textwrap.dedent("""
        from dataclasses import dataclass
        @dataclass
        class T:
            n: int
            f: float
            s: str
    """)
    create = "x = T(42, 4.5, 'hello')"
    getattr = "y = x.n"
    setattr = "x.n = 0"

    supports_mutable = True
    supports_immutable = True
    supports_defaults = True
    supports_slots = True
    supports_default_factory = True
    supports_kw_getset = True
    supports_converters = False
    supports_validators = False
    typesafe = True
    stdlib = True


class DataClassSlotsCode:
    name = 'dataclass (slots)'
    define = textwrap.dedent("""
        from dataclasses import dataclass
        @dataclass(slots=True)
        class T:
            n: int
            f: float
            s: str
    """)
    create = "x = T(42, 4.5, 'hello')"
    getattr = "y = x.n"
    setattr = "x.n = 0"

    supports_mutable = True
    supports_immutable = True
    supports_defaults = True
    supports_slots = True
    supports_default_factory = True
    supports_kw_getset = True
    supports_converters = False
    supports_validators = False
    typesafe = True
    stdlib = True


class DictCode:
    name = 'dict'
    define = ''
    create = "x = {'n': 42, 'f': 4.5, 's': 'hello'}"
    getattr = "y = x['n']"
    setattr = "x['n'] = 0"

    supports_mutable = True
    supports_immutable = False
    supports_slots = False
    supports_defaults = False
    supports_default_factory = False
    supports_kw_getset = "by str"
    supports_converters = False
    supports_validators = False
    typesafe = False
    stdlib = True


class SimpleNameSpaceCode:
    name = 'SimpleNamespace'
    define = textwrap.dedent("""
        from types import SimpleNamespace
    """)
    create = "x = SimpleNamespace(n=42, f=4.5, s='hello')"
    getattr = "y = x.n"
    setattr = "x.n = 0"

    supports_mutable = True
    supports_immutable = False
    supports_slots = False
    supports_defaults = False
    supports_default_factory = False
    supports_kw_getset = True
    supports_converters = False
    supports_validators = False
    typesafe = False
    stdlib = True


class PydanticBaseModelCode:
    name = 'pydantic'
    define = textwrap.dedent("""
        from pydantic import BaseModel
        class T(BaseModel):
            n: int
            f: float
            s: str
    """)
    create = "x = T(n=42, f=4.5, s='hello')"
    getattr = "y = x.n"
    setattr = "x.n = 0"

    supports_mutable = True
    supports_immutable = True
    supports_slots = True
    supports_defaults = True
    supports_default_factory = True
    supports_kw_getset = True
    supports_converters = True
    supports_validators = True
    typesafe = True
    stdlib = False


class PlainClassCode:
    name = 'plain class'
    define = textwrap.dedent("""
        class T:
            def __init__(self, n: int, f: float, s: str):
                self.n = n
                self.f = f
                self.s = s
    """)
    create = "x = T(42, 4.5, 'hello')"
    getattr = "y = x.n"
    setattr = "x.n = 0"

    supports_mutable = True
    supports_immutable = "manual"
    supports_slots = True
    supports_defaults = True
    supports_default_factory = True
    supports_kw_getset = True
    supports_converters = "manual"
    supports_validators = "manual"
    typesafe = True
    stdlib = True


class PlainClassSlotsCode:
    name = 'plain class (slots)'
    define = textwrap.dedent("""
        class T:
            __slots__ = 'n', 'f', 's'
            def __init__(self, n, f, s):
                self.n = n
                self.f = f
                self.s = s
    """)
    create = "x = T(42, 4.5, 'hello')"
    getattr = "y = x.n"
    setattr = "x.n = 0"

    supports_mutable = True
    supports_immutable = "manual"
    supports_slots = True
    supports_defaults = True
    supports_default_factory = True
    supports_kw_getset = True
    supports_converters = "manual"
    supports_validators = "manual"
    typesafe = True
    stdlib = True


class AttrClassCode:
    name = 'attr class'
    define = textwrap.dedent("""
        import attr
        
        @attr.s
        class T:
            n = attr.ib()
            f = attr.ib()
            s = attr.ib()
    """)
    create = "x = T(42, 4.5, 'hello')"
    getattr = "y = x.n"
    setattr = "x.n = 0"

    supports_mutable = True
    supports_immutable = True
    supports_slots = True
    supports_defaults = True
    supports_default_factory = True
    supports_kw_getset = True
    supports_converters = True
    supports_validators = True
    typesafe = True
    stdlib = False


class AttrClassSlotsCode:
    name = 'attr class (slots)'
    define = textwrap.dedent("""
        import attr

        @attr.s(slots=True)
        class T:
            n = attr.ib()
            f = attr.ib()
            s = attr.ib()
    """)
    create = "x = T(42, 4.5, 'hello')"
    getattr = "y = x.n"
    setattr = "x.n = 0"

    supports_mutable = True
    supports_immutable = True
    supports_slots = True
    supports_defaults = True
    supports_default_factory = True
    supports_kw_getset = True
    supports_converters = True
    supports_validators = True
    typesafe = True
    stdlib = False


code_classes = [
    TupleCode,
    TypingNamedTupleCode,
    CollectionsNamedTupleCode,
    DataClassCode,
    DataClassSlotsCode,
    DictCode,
    SimpleNameSpaceCode,
    PydanticBaseModelCode,
    PlainClassCode,
    PlainClassSlotsCode,
    AttrClassCode,
    AttrClassSlotsCode,
]


def run_timeit(name, stmt, setup, trials=1_000_000):
    total_time = timeit(stmt=stmt, setup=setup, number=trials, globals=globals())
    avg_time_s = total_time / trials
    avg_time_ns = avg_time_s * 1_000_000_000
    return name, avg_time_ns


def run_create(code: Code, trials=1_000_000) -> tuple[str, float]:
    setup = code.define
    stmt = code.create
    return run_timeit(code.name, stmt, setup, trials)


def run_getattr(code: Code, trials=1_000_000) -> tuple[str, float]:
    setup = code.define + '\n' + code.create
    stmt = code.getattr
    return run_timeit(code.name, stmt, setup, trials)


def run_setattr(code: Code, trials=1_000_000) -> tuple[str, float]:
    setup = code.define + '\n' + code.create
    stmt = code.setattr
    if stmt is None:
        return code.name, float('inf')
    return run_timeit(code.name, stmt, setup, trials)


import sys
from numbers import Number
from collections import deque
from collections.abc import Set, Mapping

ZERO_DEPTH_BASES = (str, bytes, Number, range, bytearray)


def getsize(obj_0):
    """Recursively iterate to sum size of object & members."""
    _seen_ids = set()

    def inner(obj):
        obj_id = id(obj)
        if obj_id in _seen_ids:
            return 0
        _seen_ids.add(obj_id)
        size = sys.getsizeof(obj)
        if isinstance(obj, ZERO_DEPTH_BASES):
            pass  # bypass remaining control flow and return
        elif isinstance(obj, (tuple, list, Set, deque)):
            size += sum(inner(i) for i in obj)
        elif isinstance(obj, Mapping) or hasattr(obj, 'items'):
            size += sum(inner(k) + inner(v) for k, v in getattr(obj, 'items')())
        # Check for custom object instances - may subclass above too
        if hasattr(obj, '__dict__'):
            size += inner(vars(obj))
        if hasattr(obj, '__slots__'):  # can have __slots__ with __dict__
            size += sum(inner(getattr(obj, s)) for s in obj.__slots__ if hasattr(obj, s))
        return size

    return inner(obj_0)


def run_sizeof(code: Code) -> tuple[str, int]:
    setup = code.define + '\n' + code.create + '\n'
    exec(setup)
    size = getsize(locals()['x'])
    return code.name, size


def run_all_tests_for_function(f, title, fmt):
    print(title)
    cases: list[tuple[str, float]] = []
    for cls in code_classes:
        cases.append(f(cls))
    cases.sort(key=lambda x: x[1])
    for i, (name, t) in enumerate(cases):
        print(fmt.format(i, name, t))
    print()
    return cases


def test_creation_speeds():
    return run_all_tests_for_function(run_create, "creation speeds", '{}: {} - {:.0f} ns')


def test_getattr_speeds():
    return run_all_tests_for_function(run_getattr, "getattr speeds", '{}: {} - {:.0f} ns')


def test_setattr_speeds():
    return run_all_tests_for_function(run_setattr, "setattr speeds", '{}: {} - {:.0f} ns')


def test_mem_usage():
    return run_all_tests_for_function(run_sizeof, "mem usage", '{}: {} - {} bytes')


def test_key(key):
    return [(code.name, getattr(code, key)) for code in code_classes]


def main():
    create_cases = test_creation_speeds()
    getattr_cases = test_getattr_speeds()
    setattr_cases = test_setattr_speeds()
    mem_cases = test_mem_usage()
    data = {
        'create': create_cases,
        'getattr': getattr_cases,
        'setattr': setattr_cases,
        'mem': mem_cases
    }

    for key in support_keys:
        data[key] = test_key(key)

    with open('results.out', 'w', encoding='utf-8') as f:
        json.dump(data, f)


if __name__ == '__main__':
    main()

def plain_class_example():
    class T:
        def __init__(self, n: int, f: float, s: str):
            self.n = n
            self.f = f
            self.s = s

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')
    y = x.n
    x.n = 0


def dataclass_example():
    from dataclasses import dataclass

    @dataclass(slots=True)
    class T:
        n: int
        f: float
        s: str

    x = T(42, 4.5, 'hello')
    x = T(24, f=4.5, s='hello')
    y = x.n
    x.n = 0


def attr_class_example():
    import attr

    @attr.s
    class T:
        n: int = attr.ib(converter=int)  # verbose
        f: float = attr.ib(validator=attr.validators.instance_of(float))
        s: str = attr.ib(default="")
        l: list = attr.ib(default_factory=list)

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')
    # can convert or validate but not required

    y = x.n
    x.n = 0


def tuple_example():
    x = 42, 4.5, 'hello'
    y = x[0]  # access by index error-prone
    # immutable


def namedtuple_example():
    from collections import namedtuple

    T = namedtuple('T', ['n', 'f', 's'])

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')

    y = x[0]
    y = x.n
    # immutable


def NamedTuple_example():
    from typing import NamedTuple

    class T(NamedTuple):
        n: int
        f: float
        s: str

    x = T(42, 4.5, 'hello')
    x = T(42, f=4.5, s='hello')

    y = x[0]
    y = x.n
    # immutable




def dict_example():
    x = {
        'n': 42,
        'f': 4.5,
        's': 'hello'
    }
    y = x['n']  # access by str error-prone
    x['n'] = 0






def SimpleNameSpace_example():
    from types import SimpleNamespace

    x = SimpleNamespace(n=42, f=4.5, s='hello')  # must be kwargs

    class NS:
        pass
    y = NS()

    y = x.n
    x.n = 0









def pydantic_example():
    from pydantic import BaseModel

    class T(BaseModel):
        n: int
        f: float
        s: str

    x = T(n=42, f=4.5, s='hello')  # must be kwargs
    y = x.n
    x.n = 0
    # args always converted to given types, type-checked at runtime

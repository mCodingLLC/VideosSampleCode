from __future__ import annotations

import typing


class Node:
    data: int
    next: Node | None


print(Node.__annotations__)
print(typing.get_type_hints(Node))
print("hello, world!")


def sub():
    yield 2
    return  # oops!
    yield 3


def gen():
    yield 1
    subgen = sub()
    yield next(subgen)
    yield next(subgen)  # raises StopIteration!
    yield 4


for x in gen():
    print(x)

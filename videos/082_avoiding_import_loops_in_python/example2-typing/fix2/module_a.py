from __future__ import annotations

from typing import TYPE_CHECKING

from module_b import func_b1

if TYPE_CHECKING:
    from module_b import B


def func_a():
    b: B = func_b1()
    ...


class A:
    def __init__(self, b: B):
        self.b = b

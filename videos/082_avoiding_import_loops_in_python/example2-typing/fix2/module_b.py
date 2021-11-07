from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from module_a import A


def func_b1():
    ...


class B:
    def __init__(self, a: A):
        self.a = a

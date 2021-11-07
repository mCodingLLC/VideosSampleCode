from __future__ import annotations

import module_b


def func_a():
    b: module_b.B = module_b.func_b1()
    ...


class A:
    def __init__(self, b: module_b.B):
        self.b = b

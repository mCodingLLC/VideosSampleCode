from module_b import func_b1, B


def func_a():
    b: B = func_b1()
    ...


class A:
    def __init__(self, b: B):
        self.b = b

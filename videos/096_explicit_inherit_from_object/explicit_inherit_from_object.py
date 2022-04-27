class A:
    pass


class B():
    pass


class C(object):

    @property
    def x(self):
        return ...

    def __new__(cls, *args, **kwargs):
        return ...

    def f(self):
        super(C, self).f()


assert all(object in cls.__bases__ for cls in [A, B, C])

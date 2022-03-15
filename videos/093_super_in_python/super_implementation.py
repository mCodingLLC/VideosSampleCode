import inspect


class Super:
    """
    A crazy implementation of the builtin super from within Python.
    Probably full of bugs, for instructional purposes only.
    """

    def __init__(self, cls=None, obj_or_cls=None, /):
        if cls is None and obj_or_cls is None:
            frame = inspect.currentframe()
            caller_locals = frame.f_back.f_locals
            assert frame.f_back.f_code.co_argcount > 0
            obj_or_cls = next(iter(caller_locals.values()))
            try:
                cls = caller_locals['__class__']  # depends on caller user __class__
            except KeyError:
                raise RuntimeError(
                    "For zero-argument Super, you need to put __class__ in the same function "
                    "that Super is used to make compiler magic work, the real super "
                    "doesn't have this restriction")

        assert inspect.isclass(cls), "cls must be a class"
        self.__thisclass__ = cls
        self._bind_self(cls, obj_or_cls)

    def _bind_self(self, cls, obj_or_cls, /):
        if obj_or_cls is None:
            self.__self__ = None
            self.__self_class__ = None
        elif inspect.isclass(obj_or_cls):
            assert issubclass(obj_or_cls, cls), "obj_or_cls is a class but not a subclass of cls"
            self.__self__ = obj_or_cls
            self.__self_class__ = obj_or_cls
        else:
            assert isinstance(obj_or_cls, cls), "obj_or_cls is an object but not an instance of cls"
            self.__self__ = obj_or_cls
            self.__self_class__ = type(obj_or_cls)

    def __get__(self, instance, owner=None):
        if self.__self__ is not None:
            return self
        if instance is not None:
            obj_or_cls = instance
        else:
            assert owner is not None, "cannot bind to None"
            obj_or_cls = owner

        self._bind_self(self.__self_class__, obj_or_cls)
        return self

    def __getattr__(self, item):
        if item == "__class__":
            return self.__class__

        if self.__self__ is None:
            raise AttributeError(item)

        mro = self.__self_class__.__mro__
        n = len(mro)
        i = mro.index(self.__thisclass__) + 1

        while i < n:
            cls = mro[i]
            try:
                res = cls.__dict__[item]
            except KeyError:
                pass
            else:
                try:
                    get = type(res).__get__  # get(self, instance, owner)
                except AttributeError:
                    return res
                else:
                    return get(res,
                               None if self.__self__ == self.__self_class__ else self.__self__,
                               self.__self_class__)

            i += 1
        raise AttributeError(item)


class A:
    def f(self):
        return ["A"]


class B(A):
    def f(self):
        __class__  # adds __class__ to locals
        return ["B"] + Super().f()


class B_super(A):
    def f(self):
        return ["B"] + super().f()


class C(B):
    def f(self):
        __class__
        return ["C"] + Super().f()


class C_super(B):
    def f(self):
        return ["C"] + super().f()


class E(A):
    def f(self):
        __class__
        return ["E"] + Super().f()


class E_super(A):
    def f(self):
        return ["E"] + super().f()


class F(C, E):
    def f(self):
        __class__
        return ["F"] + Super().f()


class F_super(C, E):
    def f(self):
        return ["F"] + super().f()


class G(F):
    pass


class H(G):
    def f(self):
        __class__
        return ["H"] + Super().f()


class H_super(G):
    def f(self):
        return ["H"] + super().f()


def main():
    print(B().f())
    print(B_super().f())
    print(C().f())
    print(C_super().f())
    print(E().f())
    print(E_super().f())
    print(F().f())
    print(F_super().f())
    print(H().f())
    print(H_super().f())


if __name__ == '__main__':
    main()

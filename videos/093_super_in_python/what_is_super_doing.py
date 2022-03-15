import inspect


def noarg_super_cannot_be_used_outside_a_class():
    x = super()  # error
    print(x)


def what_is_noarg_super():
    class A:
        def f(self):
            print(f"called A.f, self is {self}")

    class B(A):
        def f(self):
            print(f"called B.f, self is {self}")
            sup = super()
            print(type(sup), sup)
            sup.f()

    B().f()


def simple_proxy_example():
    class SimpleProxyObj:
        def __init__(self, obj):
            self.obj = obj

        def __getattr__(self, item):  # called when you proxy.abc
            return getattr(self.obj, item)

    obj = [1, 2, 3]
    proxy = SimpleProxyObj(obj)
    proxy.append(4)  # append forwarded to obj
    print(obj)
    print(proxy)
    assert obj == [1, 2, 3, 4]


def kinda_super_proxy_example():
    class KindaSuperProxyObj:
        def __init__(self, cls, obj):
            self.obj = obj
            self.cls = cls

        def __getattr__(self, item):
            attr = getattr(self.cls, item)
            if hasattr(type(attr), '__get__'):
                attr = attr.__get__(self.obj)
            return attr

    class A:
        def f(self):
            print("A")

    class B:
        def f(self):
            print("B")
            super().f()

    obj = B()
    obj.f()


def print_callers_locals():
    frame = inspect.currentframe()
    caller_locals = frame.f_back.f_locals
    print(f"caller's locals: {caller_locals}")


def know_your_caller():
    x = 5
    s = "subscribe"
    print_callers_locals()


def know_your_caller_class():
    class KnowYourCaller:
        def f(self):
            super
            print("current class", __class__)
            print_callers_locals()

    c = KnowYourCaller()
    c.f()


class Magic:
    def normal_method(self):
        print("normal method")
        x = 5
        s = "subscribe"
        print_callers_locals()

    def uses_class(self):
        print("uses class")
        x = 5
        s = "subscribe"
        __class__
        print_callers_locals()

    def uses_super(self):
        print("uses super")
        x = 5
        s = "subscribe"
        super
        print_callers_locals()


def compiler_class_magic():
    x = Magic()
    x.normal_method()
    x.uses_class()
    x.uses_super()


class A:
    def f(self):
        print(f"called A.f, self is {self}")


class B(A):
    def f(self):
        print(f"called B.f, self is {self}")


def twoarg_super_can_be_used_anywhere():
    b = B()
    sup = super(A, b)
    print("super(B, b)")

    print("super self", sup.__self__)
    print("super self class", sup.__self_class__)
    print("super thisclass", sup.__thisclass__)


def main():
    # noarg_super_cannot_be_used_outside_a_class()
    # what_is_noarg_super()
    # simple_proxy_example()
    # kinda_super_proxy_example()
    # know_your_caller()
    # know_your_caller_class()
    # compiler_class_magic()
    twoarg_super_can_be_used_anywhere()


if __name__ == '__main__':
    main()

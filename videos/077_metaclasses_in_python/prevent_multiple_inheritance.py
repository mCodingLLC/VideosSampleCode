class NoMultipleInheritanceMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        if len(bases) > 1:
            raise ValueError('Multiple inheritance is not allowed! :(')
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class NoMultipleInheritance(metaclass=NoMultipleInheritanceMeta):
    pass


class A(NoMultipleInheritance):
    pass


class B(A):
    pass


class C(A):
    pass


class A(B, C):  # Error, multiple inheritance not allowed
    pass


def main():
    a = A()
    b = B()
    c = C()  # This is NOT where the error raises


if __name__ == '__main__':
    main()

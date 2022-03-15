def super_does_not_access_parent():
    class Root:
        def f(self):
            print("Root.f", self)

    class A(Root):
        pass

    class B(A):
        def f(self):
            print("B.f", self)
            super().f()

    b = B()
    b.f()


def super_can_access_sibling():
    class Root:
        def f(self):
            print("Root.f", self)
            assert not hasattr(super(), 'f'), "You forgot to inherit from Root"

    class A(Root):
        def f(self):
            print("A.f", self)
            super().f()

    class B(Root):
        def f(self):
            print("B.f", self)
            super().f()

    class C(A, B):
        def f(self):
            print("C.f", self)
            super().f()

    C().f()


def what_is_mro():
    class Root:
        f = "Root"

    class A(Root):
        fx = "A"

    class B(Root):
        fx = "B"

    class C(A, B):
        fx = "C"

    print(C.__mro__)
    print([cls.__name__ for cls in C.__mro__])


def the_properties_of_mro_you_should_care_about():
    class A:  # (A, object)
        pass

    class B:  # (B, object)
        pass

    class C(A, B):  # (C, A, B, object)
        pass  # (A,    object)
        #       (B, object)

    class D(A, C):  # error
        pass


def main():
    # mro_example()
    # what_is_mro()
    super_can_access_sibling()
    # the_properties_of_mro_you_should_care_about()


if __name__ == '__main__':
    main()

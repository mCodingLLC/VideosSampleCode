def print_type_vs_class(obj):
    print(f"type={type(obj).__name__}, "
          f"__class__={obj.__class__.__name__}, "
          f"matches: {type(obj) is obj.__class__}")


class Animal:
    def __init__(self, name):
        self.name = name

    def __copy__(self):
        return type(self)(self.name)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.name == other.name

    def __repr__(self):
        return f"{type(self).__name__}({self.name})"

    # def __copy__(self):
    #     return self.__class__(self.name)
    #
    # def __eq__(self, other):
    #     if self.__class__ is not other.__class__:
    #         return NotImplemented
    #     return self.name == other.name
    #
    # def __repr__(self):
    #     return f"{self.__class__.__name__}({self.name})"


class Dog(Animal):
    pass


class Car:
    pass


def normal_usage():
    a = Animal("Bork")
    # d = Dog("Spot")
    # print(a, d)
    print_type_vs_class(a)


class SomeClass:
    pass


class Liar:
    # __class__ = SomeClass

    # @property
    # def __class__(self):
    #     return SomeClass

    def __getattribute__(self, item):
        if item == "__class__":
            return object

        return super().__getattribute__(item)


def lie_about_class():
    a = Liar()
    print_type_vs_class(a)


def become_subclass():
    a = Animal("Bork")
    print_type_vs_class(a)
    a.__class__ = Dog
    print_type_vs_class(a)


def become_superclass():
    b = Dog("Spot")
    print_type_vs_class(b)
    b.__class__ = Animal
    print_type_vs_class(b)


def become_unrelated_class():
    a = Animal("Bork")
    print_type_vs_class(a)
    a.__class__ = Car
    print_type_vs_class(a)


class Vec3:
    __slots__ = ("x", "y", "z")


class Vec4:
    __slots__ = ("x", "y", "z", "w")
    __class__ = Vec3


class Vec3T:
    __slots__ = ("x", "y", "z", "t")


def must_be_compatible():
    v = Vec3()
    # v.__class__ = Vec4 # Error

    v = Vec4()
    # v.__class__ = Vec3T # Error
    # v.__class__ = Vec3  # Error


class A:
    pass


def cant_change_to_or_from_immutables():
    a = A()
    a.__class__ = int  # Error


def verbose_module_example():
    import module_example
    module_example.x = 5


class Blank:
    pass


class SomeData:
    def __init__(self, x):
        self.x = x
        self._internal = 0

    def __repr__(self):
        return f"{self.__class__.__name__}(x={self.x})"

    def func(self):
        self._internal += 1


def read_pre_initialized_data():
    state = {"x": 1, "_internal": 4}
    obj = Blank()
    obj.__dict__.update(state)
    obj.__class__ = SomeData
    print_type_vs_class(obj)


def main():
    normal_usage()
    become_subclass()
    become_superclass()
    become_unrelated_class()
    lie_about_class()
    must_be_compatible()
    cant_change_to_or_from_immutables()
    verbose_module_example()
    read_pre_initialized_data()


if __name__ == '__main__':
    main()

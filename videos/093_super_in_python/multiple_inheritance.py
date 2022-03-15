import pytest

"""
Note: all these classes that derive from set only properly implement super calls in add and init.
If you wanted to use these for real, you would need super calls in all the methods
that add elements, e.g. update.
"""


class ValidatedSet(set):
    def __init__(self, *args, validators=None, **kwargs):
        self.validators = list(validators) if validators is not None else []
        if args:
            (elements,) = args
            self.validate_many(elements)
        super().__init__(*args, **kwargs)

    def validate_one(self, element):
        for f in self.validators:
            if not f(element):
                raise ValueError(f"invalid element: {element}")

    def validate_many(self, elements):
        if not self.validators:
            return
        for elem in elements:
            self.validate_one(elem)

    def add(self, element):
        self.validate_one(element)
        super().add(element)


def is_int(x):
    return isinstance(x, int)


def validated_set_example():
    print("VALIDATED SET EXAMPLE")
    ints = ValidatedSet([1, 2, 3], validators=[is_int])
    ints.add("5")
    print(ints)
    print()


class ReducedSet(set):
    def __init__(self, *args, reducer=None, **kwargs):
        self.reducer = reducer
        if args:
            (elements,) = args
            if reducer is not None:
                args = (map(reducer, elements),)

        super().__init__(*args, **kwargs)

    def add(self, element):
        if self.reducer is not None:
            element = self.reducer(element)
        super().add(element)


def reduced_set_example():
    print("REDUCED SET EXAMPLE")
    lens = ReducedSet(reducer=len)
    lens.add("hello")
    assert 5 in lens
    print()


class ModularSet(ValidatedSet, ReducedSet):
    def __init__(self, *args, n, **kwargs):
        def reduce_mod_n(x):
            return x % n

        super().__init__(*args, validators=[is_int], reducer=reduce_mod_n, **kwargs)


def modular_set_example():
    print("MODULAR SET EXAMPLE")

    mod5 = ModularSet([0, 1, 2, 5, 10], n=5)
    print(ModularSet.__mro__)
    print(mod5)

    print()


def main():
    # validated_set_example()
    # reduced_set_example()
    modular_set_example()


if __name__ == '__main__':
    main()

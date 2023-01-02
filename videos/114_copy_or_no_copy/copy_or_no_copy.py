import collections.abc
import typing


def list_example():
    l = [1, 2, 3, 4]

    for x in reversed(l):
        print(x)


class MyContainer:
    def __init__(self, l):
        self.l = l

    def __getitem__(self, item):
        return self.l[item]

    def __len__(self):
        return len(self.l)

    def __iter__(self):
        return iter(self.l)


def custom_container_example():
    l = [1, 2, 3, 4]
    container = MyContainer(l)
    print(f"{list(container)=}")
    print(reversed(container))
    # print(reversed(reversed(l))) # ERROR

    it = reversed(l)
    print(list(it))
    print(list(it))


class reversed:
    def __init__(self, seq):
        self.seq = seq
        self.n = len(seq) - 1
        if not hasattr(seq, '__getitem__'):
            raise TypeError("not reversible")

    def __iter__(self):
        return self

    def __next__(self):  # called by next()
        if self.n == -1:
            raise StopIteration
        n = self.n
        self.n = n - 1
        return self.seq[n]


def reversed(seq):
    n = len(seq) - 1
    if not hasattr(seq, '__getitem__'):
        raise TypeError("not reversible")
    while n != -1:
        yield seq[n]
        n -= 1


def copy_or_no_copy():
    l = [("a", 1), ("b", 2), ("c", 3)]
    d = dict(l)

    makes_a_copy = [
        dict(l),
        frozenset(l),
        list(l),
        set(l),
        sorted(l),
        tuple(l),
        l[::-1],  # or any slice
        [x for x in l],
    ]
    for x in makes_a_copy:
        print(x)

    doesnt_make_a_copy = [
        enumerate(l),
        filter(None, l),
        iter(l),
        map(lambda x: x, l),
        reversed(l),
        zip(l, l),
        d.keys(),
        d.values(),
        d.items(),
        (x for x in l),
    ]
    for x in doesnt_make_a_copy:
        print(x)


def numpy_example():
    import numpy as np

    arr = np.array([1, 2, 3])
    rev = arr[::-1]

    print(arr)
    print(rev)

    print(arr.data)
    print(rev.data)

    print(arr.strides)
    print(rev.strides)


def sometimes_you_want_a_copy_example():
    d = {"a": 1, "b": 2, "c": 3}

    for char, val in list(d.items()):
        d[char.upper()] = val

    print(d)


def iterable_vs_Iterable():
    container = MyContainer([1, 2, 3])
    print(isinstance(container, typing.Iterable))
    print(isinstance(container, collections.abc.Iterable))

    print(iter(container))
    # print(container.__iter__)


def main():
    list_example()
    custom_container_example()
    copy_or_no_copy()
    numpy_example()
    sometimes_you_want_a_copy_example()
    iterable_vs_Iterable()


if __name__ == '__main__':
    main()

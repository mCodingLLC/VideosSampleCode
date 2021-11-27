import itertools
import pathlib
import ipaddress
import multiprocessing.pool
import importlib.abc
import datetime
from dataclasses import dataclass


class StaticMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func

    def __call__(self, *args, **kwargs):  # New in Python 3.10
        return self.func(*args, **kwargs)


class ClassMethod:
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        return self.func.__get__(owner, type(owner))


class A:
    def normal(self, *args, **kwargs):
        print(f"normal({self=}, {args=}, {kwargs=})")

    @staticmethod
    def f1(*args, **kwargs):
        print(f"f1({args=}, {kwargs=})")

    @StaticMethod
    def f2(*args, **kwargs):
        print(f"f2({args=}, {kwargs=})")

    @classmethod
    def g1(cls, *args, **kwargs):
        print(f"g1({cls=}, {args=}, {kwargs=})")

    @ClassMethod
    def g2(cls, *args, **kwargs):
        print(f"g2({cls=}, {args=}, {kwargs=})")


@staticmethod
def h1(*args, **kwargs):
    print(f"h1({args=}, {kwargs=})")


@StaticMethod
def h2(*args, **kwargs):
    print(f"h2({args=}, {kwargs=})")


@classmethod
def j(cls, *args, **kwargs):
    print(f"j({cls=}, {args=}, {kwargs=})")


@dataclass
class Matrix:
    shape: tuple[int, int]

    @staticmethod
    def can_multiply(a, b):
        n, m = a.shape
        k, l = b.shape
        return m == k

    @staticmethod
    def can_multiply(*matrices):
        """Does m0 @ m1 @ ... @ mn make sense?"""
        for a, b in itertools.pairwise(matrices):
            n, m = a.shape
            k, l = b.shape
            if m != k:
                return False
        return True

    def can_multiply_by(self, other):
        return self.can_multiply(self, other)


class Stream:

    def extend(self, other):
        # modify self using other
        ...

    @classmethod
    def from_file(cls, file):
        ...

    @classmethod
    def concatenate(cls, *streams):
        s = cls()
        for stream in streams:
            s.extend(stream)
        return s

    @staticmethod
    def total_bytes(*streams):
        return sum(s.size for s in streams)


class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    @classmethod
    def from_json(cls, filename):
        pass

    @staticmethod
    def is_weekend(dt):
        pass


def staticmethod_example():
    A.f1()
    A.f2()

    A().f1()
    A().f2()

    print(f'{A.f1=}')
    print(f'{A.f2=}')

    print(A().f1)
    print(A().f2)

    print(f'{type(A.f1)=}')
    print(f'{type(A.f2)=}')


def classmethod_example():
    A.g1()
    A.g2()

    A().g1()
    A().g2()

    print(f'{A.g1=}')
    print(f'{A.g2=}')

    print(f'{A().g1=}')
    print(f'{A().g2=}')

    print(f'{type(A.g1)=}')
    print(f'{type(A.g2)=}')


def free_function_example():
    h1()
    h2()

    print(f'{h1=}')
    print(f'{h2=}')

    print(f'{type(h1)=}')
    print(f'{type(h2)=}')


def main():
    staticmethod_example()
    classmethod_example()
    free_function_example()


if __name__ == '__main__':
    main()

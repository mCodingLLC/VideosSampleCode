from typing import overload


def lucky(x: int = 42):
    print(x)


def tempting(arr: list, x: int = None, options: dict = None):
    x = x or len(arr)

    if not options:
        options = {"option": "value"}


def normal(arr: list, x: int = None, options: dict = None):
    x = x if x is not None else len(arr)

    if options is not None:
        options = {"option": "value"}


MISSING = object()


@overload
def tricky():
    ...


@overload
def tricky(x: None):
    ...


@overload
def tricky(x: int):
    ...


def tricky(x=MISSING):
    if x is MISSING:
        x = 42
    elif x is None:
        x = 43

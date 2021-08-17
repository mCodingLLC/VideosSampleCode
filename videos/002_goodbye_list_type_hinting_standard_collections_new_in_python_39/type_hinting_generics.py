from types import GenericAlias
from typing import List, TypeVar

if __name__ == '__main__':
    # List
    x: List[int] = []
    # list
    x: list[int] = []
    x = list[int]()
    print(type(x))
    print(list[int] == list)
    # origin and args
    print(list[int])
    t = list[int]
    print(t.__origin__)
    print(t.__args__)

    d: dict[str, int] = {}
    print(dict[str, int].__args__)

    # parameters
    T = TypeVar('T')
    print(T)
    t = dict[str, T]
    print(t)
    print(t.__parameters__)

    # comparing types
    # print(isinstance([1, 2, 3], list[int]))
    # print(issubclass(list, list[int]))
    print(isinstance(list[int], GenericAlias))

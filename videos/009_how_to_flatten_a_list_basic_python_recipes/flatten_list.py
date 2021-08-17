import functools
import itertools
import operator
import random
import time


def flatten0(lst: list[list]) -> list:
    flat = []
    for l in lst:
        for x in l:
            flat.append(x)
    return flat

def flatten1(lst: list[list]) -> list:
    flat = []
    for l in lst:
        flat.extend(l)
    return flat


def flatten2(lst: list[list]) -> list:
    flat = []
    for l in lst:
        flat += l
    return flat

def flatten3(lst: list[list]) -> list:
    return [x for l in lst for x in l]

def flatten4(lst: list[list]) -> list:
    return list(itertools.chain.from_iterable(lst))

def flatten5(lst: list[list]) -> list:
    return functools.reduce(operator.iconcat, lst, [])
                            # +=

def time_f(f):
    elapsed = 0.0
    n = 100
    M = 1000
    N = 100
    for _ in range(n):
        lst = [[random.randint(0,1000000) for j in range(N)] for i in range(M)]
        start = time.perf_counter()
        f(lst)
        elapsed += time.perf_counter() - start
    print(elapsed/n * 1000, 'ms')

if __name__ == '__main__':
    time_f(flatten0)
    time_f(flatten1)
    time_f(flatten2)
    time_f(flatten3)
    time_f(flatten4)
    time_f(flatten5)
import functools
import itertools
import operator
from string import ascii_lowercase


def itertools_permutations_example():
    n, r = 5, 5
    for perm in itertools.permutations(range(n), r):
        print(perm)


def itertools_permutations(iterable, r=None):
    # https://docs.python.org/3/library/itertools.html#itertools.permutations
    # permutations('ABCD', 2) --> AB AC AD BA BC BD CA CB CD DA DB DC
    # permutations(range(3)) --> 012 021 102 120 201 210
    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r
    if r > n:
        return
    indices = list(range(n))
    cycles = list(range(n, n - r, -1))
    yield tuple(pool[i] for i in indices[:r])
    while n:  # BLACK MAGIC, DO NOT EDIT
        for i in reversed(range(r)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                yield tuple(pool[i] for i in indices[:r])
                break
        else:
            return


def count_permutations(n, r):
    """
    How many r-permutations are there?

    [0, 1, 2, ..., n-1]

    Pick the first element (n choices).
    Pick the second element (n-1 choices).
    ...
    Pick the r-th element (n-r+1 choices).
    n * (n-1) * ... * (n-r+1)

    E.g. for n=5, r=3
    5 * 4 * 3

    Idea to list them:

    For each choice of first element
    [ 0 | 1, 2, ..., n-1]
    list all (r-1)-permutations of remaining elements
    [ 0 , 1 | 2, ..., n-1]
    """
    if r > n:
        return 0
    if r < 0:
        raise ValueError("r must be non-negative")
    return functools.reduce(operator.mul, range(n, n - r, -1), 1)


def _permutations_recursive(items, i, r):
    """
    Modifies items in-place, yielding at each permutation
    Assumes items is [0, ..., n-1].
    Invariant: items is unchanged after this function returns.

    [| 0, 1, 2, ..., n-1]
    i=0

    For each choice of first element
    [ 1 | 0, 2, ..., n-1]
        i=1

    list all (r-1)-permutations of remaining elements
    [ 0 , 1 | 2, ..., n-1]
            i=2

    [ 0 | 1, 2, 3, ..., n-1]
    [ 1 | 0, 2, 3, ..., n-1]
    [ 2 | 0, 1, 3, ..., n-1]
    [ 3 | 0, 1, 2, ..., n-1]
    [n-1| 0, 1, 2, ..., n-2]

    """
    if r == 0:
        yield
        return

    for j in range(i, len(items)):
        # if i != j:
        #     print(swap_msg(i, j, len(items)))
        items[i], items[j] = items[j], items[i]  # swap i, j
        for _ in _permutations_recursive(items, i + 1, r - 1):
            yield
        # or better:
        # yield from _permutations_recursive(items, i + 1, r - 1)

    # print(push_to_back_msg(i, len(items)))

    items.append(items.pop(i))  # move i to back


def permutations_recursive(iterable, r=None):
    """Does error checking and reduces arbitrary case to [0, ..., n-1]"""
    items = tuple(iterable)
    n = len(items)
    r = n if r is None else r
    if r > n:
        return
    if r < 0:
        raise ValueError("r must be non-negative")
    indices = list(range(n))

    for _ in _permutations_recursive(indices, 0, r):
        yield tuple(items[indices[i]] for i in range(r))


def issue_with_permutations_recursive():
    n, r = 2000, 2000
    print(count_permutations(n, r))

    for idx, perm in enumerate(permutations_recursive(range(n), r)):  # recursion error!
        print(perm)
        if idx == 100:
            break


def swap_msg(i, j, n):
    return '|'.join(''.join(['i' if i == x else '', 'j' if j == x else '', ' ' if x not in [i, j] else '']) for x in range(n)) + f" swap {i} {j}"


def push_to_back_msg(i, n):
    return '|'.join(''.join(['x' if i == x else '', 'i' if x == n - 1 else '', ' ' if x not in [i, n - 1] else '']) for x in range(n)) + f" shift {i}"


def _permutations_iterative_with_stack(items, r0):  # cut from video :(
    n = len(items)
    stack = [(0, r0, 0)]  # (i, r, j)
    while stack:
        i, r, j = stack.pop()
        if r == 0:
            yield
        elif j < n:
            items[i], items[j] = items[j], items[i]
            stack.append((i, r, j + 1))
            stack.append((i + 1, r - 1, i + 1))
        elif j == n:
            items.append(items.pop(i))
        else:
            raise RuntimeError("uh oh")


def _permutations_iterative_no_stack(items, r0):
    n = len(items)
    yield
    for i, ticks in countdown(n, r0):
        tick = ticks[i]
        if tick == 0:
            items.append(items.pop(i))
        else:
            j = n - tick
            items[i], items[j] = items[j], items[i]
            yield


def countdown(n, r):
    """
    n=5, r=3
    543
    542
    541
    540
    533
    532
    531
    530
    523
    522
    521
    520
    """

    ticks = list(range(n, n - r, -1))  # (n, n-1, n-2, ..., n-r+1), len == r
    while True:
        for i in reversed(range(r)):  # start from the back, indexing over (n, n-1, n-2, ..., n-r+1)
            ticks[i] -= 1
            yield i, ticks
            if ticks[i] == 0:  # carry
                ticks[i] = n - i
            else:
                break
        else:
            return


def permutations_iterative(iterable, r=None):
    items = tuple(iterable)
    n = len(items)
    r = n if r is None else r
    if r > n:
        return
    if r < 0:
        raise ValueError("r must be non-negative")
    indices = list(range(n))

    for _ in _permutations_iterative_no_stack(indices, r):
        yield tuple(items[indices[i]] for i in range(r))


def main():
    N = 6

    # check our implementations agree with itertools
    for n, r in itertools.product(range(N), range(N + 1)):
        items = ascii_lowercase[:n]
        expected = list(itertools.permutations(items, r))
        actual_recursive = list(permutations_recursive(items, r))
        assert actual_recursive == expected, (actual_recursive, expected)

        actual_iterative = list(permutations_iterative(items, r))
        assert actual_iterative == expected, (actual_iterative, expected)

        assert count_permutations(n, r) == len(expected), (count_permutations(n, r), len(expected))


if __name__ == '__main__':
    main()

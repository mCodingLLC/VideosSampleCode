import asyncio
import collections
import contextlib
import math
from collections.abc import Iterator
from typing import NamedTuple


def get_values():
    yield "hello"
    yield "world"
    yield 123
    # return 42  # very uncommon to return something


def example_get_values():
    for x in get_values():
        print(x)

    print(list(get_values()))

    gen = get_values()
    print(next(gen))
    print(next(gen))
    print(next(gen))

    # print(next(gen)) StopIteration


class Range:
    def __init__(self, stop: int):
        self.start = 0
        self.stop = stop

    def __contains__(self, item):
        return isinstance(item, int) and 0 <= item < self.stop

    def __iter__(self) -> Iterator[int]:
        curr = self.start
        while curr < self.stop:
            yield curr
            curr += 1


def range_example():
    print(42 in Range(100000000000000000000000000))

    for n in Range(5):
        print(n)


class MyDataPoint(NamedTuple):
    x: float
    y: float
    z: float


def mydata_reader(file):
    for row in file:
        cols = row.rstrip().split(",")
        cols = [float(c) for c in cols]
        yield MyDataPoint._make(cols)


def example_reader():
    with open("mydata.txt") as file:
        for row in mydata_reader(file):
            print(row)


def collatz(n):
    while True:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        yield n
        if n == 1:
            break


def collatz_list(n):
    result = []
    while True:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        result.append(n)
        if n == 1:
            break

    return result


def collatz_len(n):
    count = 0
    while True:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        count += 1
        if n == 1:
            break

    return count


def example_collatz():
    n = 27
    # seq = list(collatz(n))
    step_length = sum(1 for _ in collatz(n))
    # step_length = len(collatz_list(n)) # VERY INEFFICIENT

    print(f"{n} took {step_length} iterations to hit 1")


def powers_of_two():
    x = 1
    while True:
        yield x
        x *= 2


def example_composable():
    with open("nums.txt") as file:
        nums = (row.partition("#")[0].rstrip() for row in file)  # strip trailing comments
        nums = (row for row in nums if row)  # remove empty lines
        nums = (float(row) for row in nums)
        nums = (x for x in nums if math.isfinite(x))
        nums = (max(0., x) for x in nums)
        s = sum(nums)
        print(f"the sum is {s}")


def pairwise(it):
    try:
        a = next(it)
        b = next(it)
    except StopIteration:
        return
    yield a, b
    while True:
        try:
            a, b = b, next(it)
        except StopIteration:
            return
        yield a, b


def consecutive_sums(it):
    for a, b in pairwise(it):
        yield a + b


def pascals_triangle(n):
    yield 1
    if n == 1:
        return
    # for s in consecutive_sums(pascals_triangle(n - 1)):
    #     yield s
    yield from consecutive_sums(pascals_triangle(n - 1))
    yield 1


def example_pascal():
    print(list(pascals_triangle(1)))
    print(list(pascals_triangle(2)))
    print(list(pascals_triangle(3)))
    print(list(pascals_triangle(4)))
    print(list(pascals_triangle(5)))
    print(list(pascals_triangle(6)))
    print(list(pascals_triangle(7)))


def opposite_signs(x, y):
    return x * y <= 0.


def find_root(f, a, b):
    fa, fb = f(a), f(b)
    assert opposite_signs(fa, fb), "f must change signs"

    while True:
        m = (a + b) / 2.
        fm = f(m)
        if opposite_signs(fa, fm):
            b, fb = m, fm
        else:
            a, fa = m, fm
        yield m, fm


def p(x):
    return (x - 12.) * (x - 7.) * (x + 1.) * (x + 7.)


def example_find_root():
    for x, fx in find_root(p, -5., 5.):
        print(f"{x:.04f}, {fx:.04f}")
        if abs(fx) < .001:
            break


async def async_video_when():
    await asyncio.sleep(42)


def worker(f):
    tasks = collections.deque()
    value = None
    while True:
        batch = yield value
        value = None
        if batch is not None:
            tasks.extend(batch)
        else:
            if tasks:
                args = tasks.popleft()
                value = f(*args)


def quiet_worker(f):
    while True:
        w = worker(f)
        try:
            yield from w
        except Exception as exc:
            print(f"ignoring {exc.__class__.__name__}")


def example_worker():
    w = quiet_worker(str)
    w.send(None)
    w.send([("starting up",), (1,), (2,), (3,)])
    print(next(w))
    print(next(w))
    print(next(w))
    print(next(w))

    w.send([(4,), (5,)])
    print(next(w))
    print(next(w))

    w.throw(ValueError)

    w.send([(7,), (8,)])
    print(next(w))
    print(next(w))

    w.close()
    print(next(w))


def acquire_resource():
    ...


def cleanup_resource():
    ...


@contextlib.contextmanager
def my_resource(*args):
    resource = acquire_resource(*args)
    try:
        yield resource
    finally:
        cleanup_resource(resource)


def main():
    example_get_values()
    # example_collatz()
    # example_reader()
    # example_find_root()
    # example_pascal()
    # example_composable()
    # example_worker()


if __name__ == '__main__':
    main()

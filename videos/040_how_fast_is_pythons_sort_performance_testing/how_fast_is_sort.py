import operator
import random
import string
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from itertools import product

import matplotlib.axes
import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np
from pandas import DataFrame, read_pickle


def is_sorted(a: list, *, key=None, reverse=False) -> bool:
    if not a:
        return True
    b = a if key is None else map(key, a)
    cmp = operator.le if not reverse else operator.ge
    head = iter(b)
    tail = iter(b)
    next(tail)
    return all(cmp(x, y) for x, y in zip(head, tail))


class DataMaker(ABC):

    @abstractmethod
    def make(self, size, seed) -> list:
        return []

    def compatible_keys(self):
        return [None]

    def compatible_sort_kwargs(self):
        keys = self.compatible_keys()
        kwargs_list = []
        if None in keys:
            kwargs_list += [None, {"reverse": True}]
        kwargs_list += [{"key": key, "reverse": True} for key in keys if key is not None]
        kwargs_list += [{"key": key} for key in keys if key is not None]
        return kwargs_list


class UniformIntMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        return list(np.random.randint(low=0, high=2 ** 31 - 1, size=size))


class SortedUniformIntMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        return sorted(np.random.randint(low=0, high=2 ** 31 - 1, size=size))


class NearlySortedUniformIntMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        data = sorted(np.random.randint(low=0, high=2 ** 31 - 1, size=size))
        if len(data) < 3:
            return data
        for _ in range(10):
            i, j = np.random.randint(low=0, high=size - 1, size=2)
            data[i], data[j] = data[j], data[i]
        return data


class UniformFloatMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        return list(np.random.random(size=size))


class SortedUniformFloatMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        return sorted(np.random.random(size=size))


class GaussianFloatMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        return list(np.random.normal(size=size))


class AFewIntMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        return list(np.random.randint(low=0, high=32, size=size))


def random_str(size):
    return ''.join(random.choices(string.printable, k=size))


class GeometricStringMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        lengths = np.random.geometric(p=1 / 5, size=size)
        strs = [random_str(l) for l in lengths]
        return strs


class SortedGeometricStringMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        lengths = np.random.geometric(p=1 / 5, size=size)
        strs = [random_str(l) for l in lengths]
        return sorted(strs)


@dataclass(frozen=True, order=True)
class TwoIntsAndAString:
    x: int
    y: int
    s: str


class UniformTwoIntsAndAGeometricStringMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        xs = np.random.randint(low=0, high=2 ** 31 - 1, size=size)
        ys = np.random.randint(low=0, high=2 ** 31 - 1, size=size)
        lengths = np.random.geometric(p=1 / 5, size=size)
        strs = (random_str(l) for l in lengths)
        data = [TwoIntsAndAString(x, y, s) for x, y, s in zip(xs, ys, strs)]
        return data


class UniformTwoIntsAndAGeometricStringTupleMaker(DataMaker):
    def make(self, size, seed):
        np.random.seed(seed)
        xs = np.random.randint(low=0, high=2 ** 31 - 1, size=size)
        ys = np.random.randint(low=0, high=2 ** 31 - 1, size=size)
        lengths = np.random.geometric(p=1 / 5, size=size)
        strs = (random_str(l) for l in lengths)
        data = [(x, y, s) for x, y, s in zip(xs, ys, strs)]
        return data


@dataclass
class SortingTestCase:
    size: int
    seed: int
    data_maker: DataMaker
    sort_kwargs: dict = None
    times_ns: list[int] = field(default_factory=list)

    def as_tuple(self) -> tuple:
        return (self.size, self.seed, self.data_maker.__class__.__name__, self.sort_kwargs, self.times_ns)

    def run(self) -> None:
        data = self.data_maker.make(self.size, self.seed)
        kwargs = self.sort_kwargs
        if kwargs:
            start = time.perf_counter_ns()
            data.sort(**kwargs)
            end = time.perf_counter_ns()
            assert is_sorted(data, **kwargs)
        else:
            start = time.perf_counter_ns()
            data.sort()
            end = time.perf_counter_ns()
            assert is_sorted(data)
        elapsed = end - start
        self.times_ns.append(elapsed)


def make_all_test_cases(sizes: list[int], seeds: list[int],
                        data_makers: list[DataMaker], use_kwargs: bool) -> list[SortingTestCase]:
    tests: list[SortingTestCase] = []

    for size, seed, data_maker in product(sizes, seeds, data_makers):
        if use_kwargs:
            for sort_kwargs in data_maker.compatible_sort_kwargs():
                tests.append(SortingTestCase(size=size, seed=seed, data_maker=data_maker, sort_kwargs=sort_kwargs))
        else:
            tests.append(SortingTestCase(size=size, seed=seed, data_maker=data_maker, sort_kwargs=None))

    return tests


def run_tests_n_times(tests: list[SortingTestCase], trials: int, shuffler: random.Random) -> None:
    for i in range(trials):
        print(f'starting epoch {i + 1}/{trials}')
        shuffler.shuffle(tests)
        for test in tests:
            test.run()


def test_data_to_df(tests: list[SortingTestCase]) -> DataFrame:
    df = DataFrame.from_records(data=map(lambda test: test.as_tuple(), tests),
                                columns=["size", "seed", "data_maker", "sort_kwargs", "time"])
    df['sort_kwargs'] = df['sort_kwargs'].astype(str)
    df['data_maker'] = df['data_maker'].astype(str)
    df = df.explode("time")
    df['time'] = df['time'].astype(float)
    df['time'] /= 10 ** 3  # convert to microseconds
    df['reverse'] = df['sort_kwargs'].str.contains("reverse")
    return df


def make_plot(df: DataFrame):
    fig: matplotlib.figure.Figure
    ax: matplotlib.axes.Axes
    fig, ax = plt.subplots()
    ax.set_title("Sorting Times")
    ax.set_xlabel("Number of elements to sort")
    ax.set_ylabel("Time (microseconds)")
    lines = []
    grouped = df.groupby(["data_maker", "sort_kwargs"])
    for name, group in grouped:
        means = group.groupby("size")["time"].mean()
        cls, kwargs = name
        label = str(cls) if kwargs == "None" else f'{cls}, {kwargs}'
        line, = ax.plot(means, label=label)
        lines.append(line)

    leg = ax.legend(fancybox=True, shadow=True)
    lined = {}  # maps legend lines to original lines.
    for legline, origline in zip(leg.get_lines(), lines):
        legline.set_picker(True)
        lined[legline] = origline

    def on_pick(event):
        legline = event.artist
        origline = lined[legline]
        visible = not origline.get_visible()
        origline.set_visible(visible)
        legline.set_alpha(1.0 if visible else 0.2)
        ax.relim(visible_only=True)
        ax.autoscale_view()
        fig.canvas.draw()

    fig.canvas.mpl_connect('pick_event', on_pick)
    plt.show()


def main():
    recompute_results = True
    pkl_filename = "sort_times_df.pkl"
    include_reverse_when_plotting = False
    sizes = list(range(1024))
    seeds = list(range(10))
    trials = 20  # lower this if you don't want to wait as long, 1 is fine "just to see"

    # add in or comment out data makers
    data_makers: list[DataMaker] = [
        UniformIntMaker(),
        # AFewIntMaker(),
        # SortedUniformIntMaker(),
        # NearlySortedUniformIntMaker(),

        UniformFloatMaker(),
        # SortedUniformFloatMaker(),
        # GaussianFloatMaker(),

        GeometricStringMaker(),
        # SortedGeometricStringMaker(),

        UniformTwoIntsAndAGeometricStringMaker(),
        UniformTwoIntsAndAGeometricStringTupleMaker(),
    ]

    if recompute_results:
        tests = make_all_test_cases(sizes=sizes, seeds=seeds, data_makers=data_makers, use_kwargs=True)
        shuffle_random = random.Random(1)
        run_tests_n_times(tests, trials, shuffle_random)
        df = test_data_to_df(tests)
        df.to_pickle(pkl_filename)
    else:
        df = read_pickle(pkl_filename)
        maker_names = [maker.__class__.__name__ for maker in data_makers]
        df = df[df['data_maker'].isin(maker_names)]
    if not include_reverse_when_plotting:
        df = df[df['reverse'] == False]

    make_plot(df)


if __name__ == '__main__':
    main()

# Performance changes with
# 1. How much to sort
# 2. The type of data
# 3. Parameters of the sort
# 4. The distribution of the data

# Performance can also depend on
# 1. Your computer hardware, operating system, etc.
# 2. The version of Python 3.8, 3.9 etc.
# 3. Which type of Python CPython, PyPy etc.
# 4. The order you run the tests in
# 5. What else is running at the same time
# 6. Random events, temperature, nearby electomagnetic fields
# 7. Many more things...

from collections.abc import Callable
from typing import TypeVar
import operator

import matplotlib.pyplot as plt

import numpy as np

T = TypeVar('T')
BinOp = Callable[[T, T], T]

"""
Idea:
    n == 2 * n // 2 + n % 2
Therefore:
    x ** n == x ** (n % 2) * (x ** (n//2)) ** 2
E.g.
    x ** 31 == x * (x ** 15) ** 2
"""


def slow_pow(x, n: int):
    res = 1
    for _ in range(n):
        res *= x
    return res


def fast_pow(x, n: int):
    if n == 0:
        return 1
    half_n, rem = divmod(n, 2)  # n // 2, n % 2
    res = fast_pow(x, half_n)
    res = res * res
    return x * res if rem else res


def fast_pow_monoid_strategy(mul: BinOp[T], identity: T, x: T, n: int) -> T:
    if n < 0:
        raise ValueError(f"n must be >= 0, but got {n}")
    if n == 0:
        return identity
    half_n, rem = divmod(n, 2)
    res = fast_pow_monoid_strategy(mul, identity, x, half_n)
    res = mul(res, res)
    return mul(x, res) if rem else res


def fast_pow_semigroup_strategy(mul: BinOp[T], x: T, n: int) -> T:
    if n < 1:
        raise ValueError(f"n must be > 0, but got {n}")
    if n == 1:
        return x
    half_n, rem = divmod(n, 2)
    res = fast_pow_semigroup_strategy(mul, x, half_n)
    res = mul(res, res)
    return mul(x, res) if rem else res


def fast_pow_int_examples():
    assert slow_pow(1, 100) == 1
    assert slow_pow(5, 3) == 125
    assert slow_pow(2, 11) == 2048

    assert fast_pow(1, 100) == 1
    assert fast_pow(5, 3) == 125
    assert fast_pow(2, 11) == 2048


def fast_pow_monoid_examples():
    assert fast_pow_monoid_strategy(operator.mul, 1, 1, 100) == 1
    assert fast_pow_monoid_strategy(operator.mul, 1, 5, 3) == 125
    assert fast_pow_monoid_strategy(operator.mul, 1, 2, 11) == 2048

    assert fast_pow_monoid_strategy(operator.add, 0, 1, 100) == 100
    assert fast_pow_monoid_strategy(operator.add, 0, 5, 3) == 15
    assert fast_pow_monoid_strategy(operator.add, 0, 2, 11) == 22

    assert fast_pow_monoid_strategy(operator.concat, "", "abc", 5) == "abcabcabcabcabc"


def fast_pow_semigroup_examples():
    assert fast_pow_semigroup_strategy(operator.mul, 1, 100) == 1
    assert fast_pow_semigroup_strategy(operator.mul, 5, 3) == 125
    assert fast_pow_semigroup_strategy(operator.mul, 2, 11) == 2048

    assert fast_pow_semigroup_strategy(operator.add, 1, 100) == 100
    assert fast_pow_semigroup_strategy(operator.add, 5, 3) == 15
    assert fast_pow_semigroup_strategy(operator.add, 2, 11) == 22

    assert fast_pow_semigroup_strategy(operator.concat, "abc", 5) == "abcabcabcabcabc"

    n_samples = 1000
    x = np.linspace(0, 1, n_samples)
    uniform_dist = np.ones_like(x) / n_samples
    assert np.isclose(np.sum(uniform_dist), 1.0), np.sum(uniform_dist)

    for n in [1, 2, 3, 4, 5]:
        smoothed_dist = fast_pow_semigroup_strategy(np.convolve, uniform_dist, n)
        assert np.isclose(np.sum(smoothed_dist), 1.0), np.sum(smoothed_dist)
        xn = np.linspace(x[0] * n, x[-1] * n, len(smoothed_dist))
        normalizing_constant = len(smoothed_dist) / (xn[-1] - xn[0])
        plt.plot(xn, smoothed_dist * normalizing_constant)

    plt.show()


def main():
    fast_pow_int_examples()
    fast_pow_monoid_examples()
    fast_pow_semigroup_examples()


if __name__ == '__main__':
    main()

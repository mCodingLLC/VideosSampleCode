import math
from fractions import Fraction

import pytest

from cfrac import ComplexFraction


def test_construction():
    assert ComplexFraction() == ComplexFraction(0)
    assert ComplexFraction() == 0
    assert ComplexFraction() == 0.0
    assert ComplexFraction(1, 1) == 1 + 1j
    assert ComplexFraction.from_complex(1 + 1j) == ComplexFraction(1, 1)


def test_conversions():
    assert complex(ComplexFraction(0)) == 0
    assert abs(complex(ComplexFraction(1, 2)) - (1 + 2j)) < 1e-6
    assert ComplexFraction(1, 2).as_fraction_pair() == (1, 2)


def test_arithmetic():
    assert ComplexFraction(1) + ComplexFraction(2) == ComplexFraction(3)
    assert ComplexFraction(1, 2) + ComplexFraction(3, 4) == ComplexFraction(4, 6)
    assert ComplexFraction(1, 2) - ComplexFraction(3, 4) == ComplexFraction(-2, -2)
    assert ComplexFraction(1, 2) * ComplexFraction(3, 4) == ComplexFraction(-5, 10)
    assert ComplexFraction(1, 2) / ComplexFraction(3, 4) == ComplexFraction(Fraction(11, 25), Fraction(2, 25))
    assert +ComplexFraction(1, 2) == ComplexFraction(1, 2)
    assert -ComplexFraction(1, 2) == ComplexFraction(-1, -2)
    assert ComplexFraction(1, 2).conjugate() == ComplexFraction(1, -2)
    assert ComplexFraction(1, 2).norm_squared() == 5
    assert math.isclose(abs(ComplexFraction(1, 2)), math.sqrt(5))
    z = ComplexFraction(1)
    z += 1j
    assert z == ComplexFraction(1, 1)


def test_operator_fallbacks():
    assert ComplexFraction(1) + 1 == 2
    assert type(ComplexFraction(1) + 1) == ComplexFraction

    assert 1 + ComplexFraction(1) == 2
    assert type(1 + ComplexFraction(1)) == ComplexFraction

    assert abs(ComplexFraction(1) + 1.5 - 2.5) < 1e-6
    assert type(ComplexFraction(1) + 1.5) == complex


def test_pow():
    assert ComplexFraction(1, 2) ** 0 == 1
    assert ComplexFraction(1, 2) ** 5 == ComplexFraction(41, -38)
    assert ComplexFraction(1, 2) ** -5 == ComplexFraction(Fraction(41, 3125), Fraction(38, 3125))
    assert ComplexFraction(0, 1) ** 1000 == 1

    with pytest.raises(ValueError):
        ComplexFraction(0) ** 0


def test_hash():
    assert hash(ComplexFraction(0)) == hash(0)
    assert hash(ComplexFraction(42)) == hash(42)
    assert hash(ComplexFraction(Fraction(1, 2))) == hash(Fraction(1, 2))
    assert hash(ComplexFraction(0, 1)) == hash(1j)

    d = {ComplexFraction(0, 1): "a", ComplexFraction(1, 0): "b", ComplexFraction(1, 1): "c"}
    assert d[1j] == "a"
    assert d[1] == "b"
    assert d[1 + 1j] == "c"


def test_bool():
    assert not bool(ComplexFraction(0))
    assert bool(ComplexFraction(1))
    assert bool(ComplexFraction(0, 1))


def test_comparisons_raise():
    with pytest.raises(TypeError):
        ComplexFraction() < ComplexFraction()

    with pytest.raises(TypeError):
        ComplexFraction() <= ComplexFraction()

    with pytest.raises(TypeError):
        ComplexFraction() > ComplexFraction()

    with pytest.raises(TypeError):
        ComplexFraction() >= ComplexFraction()

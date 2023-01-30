from __future__ import annotations

import operator
import sys
import typing
from decimal import Decimal
from fractions import Fraction
from numbers import Complex, Rational

_HASH_M = 2 ** (sys.hash_info.width - 1)


def _fast_pow(x, n: int):
    if n == 1:  # assume n >= 1
        return x
    half_n, remainder = divmod(n, 2)
    result = _fast_pow(x, half_n)
    result *= result
    return x * result if remainder else result


def _operator_fallbacks(monomorphic_operator, fallback_operator):
    # See https://docs.python.org/3/library/numbers.html
    def forward(a, b):
        if isinstance(b, (Rational, ComplexFraction)):
            return monomorphic_operator(a, b)
        elif isinstance(b, (float, complex)):
            return fallback_operator(complex(a), b)
        else:
            return NotImplemented

    forward.__name__ = f'__{fallback_operator.__name__}__'
    forward.__doc__ = monomorphic_operator.__doc__

    def reverse(b, a):
        if isinstance(a, (Rational, ComplexFraction)):
            return monomorphic_operator(a, b)
        elif isinstance(a, Complex):
            return fallback_operator(complex(a), complex(b))
        else:
            return NotImplemented

    reverse.__name__ = f'__r{fallback_operator.__name__}__'
    reverse.__doc__ = monomorphic_operator.__doc__

    return forward, reverse


SupportsFrac = typing.Union[Rational, float, str, Decimal]


class ComplexFraction(Complex):
    """Complex numbers of the form p + qi, where p and q are rational.

     Also called Gaussian rationals.
     """

    __slots__ = ("_real", "_imag")

    def __new__(cls,
                real: SupportsFrac = Fraction(0),
                imag: SupportsFrac = Fraction(0)):
        self = super().__new__(cls)
        self._real = Fraction(real)
        self._imag = Fraction(imag)
        return self

    @property
    def real(self):
        return self._real

    @property
    def imag(self):
        return self._imag

    @classmethod
    def from_complex(cls, z):
        return cls(Fraction.from_float(z.real), Fraction.from_float(z.imag))

    def as_fraction_pair(self):
        return self.real, self.imag

    def __complex__(self):
        """complex(self)"""
        return float(self.real) + 1j * float(self.imag)

    def __repr__(self):
        """repr(self)"""
        return f'{self.__class__.__name__}({self.real!r}, {self.imag!r})'

    def __str__(self):
        """str(self)"""
        return f'({self.real} + {self.imag}j)'

    def _add(self, other):
        """self + other"""
        return ComplexFraction(self.real + other.real, self.imag + other.imag)

    __add__, __radd__ = _operator_fallbacks(_add, operator.add)

    def _sub(self, other):
        """self - other"""
        return ComplexFraction(self.real - other.real, self.imag - other.imag)

    __sub__, __rsub__ = _operator_fallbacks(_sub, operator.sub)

    def _mul(self, other):
        """self * other"""
        return ComplexFraction(self.real * other.real - self.imag * other.imag,
                               self.imag * other.real + self.real * other.imag)

    __mul__, __rmul__ = _operator_fallbacks(_mul, operator.mul)

    def _truediv(self, other):
        """self / other"""
        denominator = other.real * other.real + other.imag * other.imag
        return ComplexFraction(
            (self.real * other.real + self.imag * other.imag) / denominator,
            (self.imag * other.real - self.real * other.imag) / denominator
        )

    __truediv__, __rtruediv__ = _operator_fallbacks(_truediv, operator.truediv)

    def __pow__(self, exponent):
        """self ** exponent"""
        if not isinstance(exponent, Rational):
            return complex(self) ** exponent
        if exponent.denominator != 1:  # not an integer exponent
            return complex(self) ** complex(exponent)
        exponent = exponent.numerator
        if exponent == 0:
            if self == 0:
                raise ValueError("math domain error")
            else:
                return ComplexFraction(1)
        if exponent < 0:
            return 1 / (self ** (-exponent))
        return _fast_pow(self, exponent)

    def __rpow__(self, base):
        """base ** self"""
        if self.imag == 0:
            return base ** self.real

        return base ** complex(self)

    def __pos__(self):
        """+self"""
        return self

    def __neg__(self):
        """-self"""
        return ComplexFraction(-self.real, -self.imag)

    def __abs__(self):
        """abs(self)"""
        if self.imag == 0:
            return abs(self.real)
        elif self.real == 0:
            return abs(self.imag)
        return self.norm_squared() ** .5

    def norm_squared(self):
        """Square of Euclidean norm"""
        return self.real * self.real + self.imag * self.imag

    def conjugate(self):
        """p + qi -> p - qi"""
        return ComplexFraction(self.real, -self.imag)

    def __hash__(self):
        """hash(self)"""
        # See https://docs.python.org/3/library/stdtypes.html
        hash_value = hash(self.real) + sys.hash_info.imag * hash(self.imag)
        hash_value = (hash_value & (_HASH_M - 1)) - (hash_value & _HASH_M)
        if hash_value == -1:
            hash_value = -2
        return hash_value

    def __eq__(self, other):
        """self == other"""
        if not isinstance(other, Complex):
            return NotImplemented

        return self.real == other.real and self.imag == other.imag

    def __bool__(self):
        """bool(self)"""
        return self.real != 0 or self.imag != 0

    def __reduce__(self):
        return self.__class__, (self._real, self._imag)

    def __copy__(self):
        if type(self) == ComplexFraction:
            return self  # immutable
        return self.__class__(self._real, self._imag)

    def __deepcopy__(self, memo):
        if type(self) == ComplexFraction:
            return self  # immutable components
        return self.__class__(self._real, self._imag)

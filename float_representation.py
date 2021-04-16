import struct
from decimal import Decimal


# Reference on floats
# https://en.wikipedia.org/wiki/Double-precision_floating-point_format
# https://en.wikipedia.org/wiki/IEEE_754
# https://docs.python.org/3/library/stdtypes.html?highlight=float

def float_to_bin(f) -> str:
    # d for double precision (64 bit) floating point,
    # > for big-endian (the way we usually write numbers in math)
    fmt = ">d"
    bz = struct.pack(fmt, f)
    return "".join(f"{b:08b}" for b in bz)


def every_n_characters(s, n):
    for i in range(0, len(s), n):
        yield s[i:i + n]


def bits_to_float(bits) -> float:
    fmt = ">d"
    bz = bytes([int(chars, base=2) for chars in every_n_characters(bits, 8)])
    t = struct.unpack(fmt, bz)
    return t[0]


def sign_exponent_fraction(s):
    return s[0:1], s[1:12], s[12:64]


def pretty_float_bits(f) -> str:
    return " ".join(sign_exponent_fraction(float_to_bin(f)))


def addition_fail():
    print(".1 + .2:", .1 + .2)
    print(".1 + .2 == .3", .1 + .2 == .3)
    print(f".1:\t\t{pretty_float_bits(.1)}")
    print(f".2:\t\t{pretty_float_bits(.2)}")
    print(f".3:\t\t{pretty_float_bits(.3)}")
    print(f".1+.2:\t{pretty_float_bits(.1 + .2)}")


def one_and_negative_one():
    print(f'1.:\t\t{pretty_float_bits(1.)}')
    print(f'-1.:\t{pretty_float_bits(-1.)}')


def zero_and_negative_zero():
    print(f'0.:\t\t{pretty_float_bits(0.)}')
    print(f'-0.:\t{pretty_float_bits(-0.)}')
    x, y = 0., -0.
    print("0. == -0.?", x == y)
    print("0. is -0.?", x is y)

    x, y = 0, -0
    print("0 is 0?", x is y)


def infinities():
    print(f'2**1023:\t{pretty_float_bits(2. ** 1023)}')
    print(f'2**1024:\t{pretty_float_bits(2. ** 1023 * 2)}')
    print(f'inf:\t\t{pretty_float_bits(float("inf"))}')
    print(f'-inf:\t\t{pretty_float_bits(float("-inf"))}')


def nans():
    print(f'nan:\t\t{pretty_float_bits(float("nan"))}')
    print(f'inf*0.:\t\t{pretty_float_bits(float("inf") * 0.)}')
    my_nan = bits_to_float("0111111111111000000000000001000000000000010000000000000000000000")
    print(f'mynan:\t\t{pretty_float_bits(my_nan)}')

    print("nan == nan?", float("nan") == float("nan"))


def denormalized_numbers():
    print(f'2**-1022:\t{pretty_float_bits(2 ** -1022)}')
    print(f'2**-1023:\t{pretty_float_bits(2 ** -1023)}')
    print(f'2**-1024:\t{pretty_float_bits(2 ** -1024)}')
    print(f'2**-1074:\t{pretty_float_bits(2 ** -1074)}')
    print(f'2**-1075:\t{pretty_float_bits(2 ** -1075)}')
    print(f'2**-1076:\t{pretty_float_bits(2 ** -1076)}')


def almost_equal(x, y, eps=10 ** -6):
    return abs(x - y) < eps


def main():
    addition_fail()

    one_and_negative_one()
    zero_and_negative_zero()
    infinities()
    nans()
    denormalized_numbers()

    print(almost_equal(.1 + .2, .3))

    print(repr(Decimal(".1")))
    print(Decimal(".1") + Decimal(".2") == Decimal(".3"))


if __name__ == '__main__':
    main()

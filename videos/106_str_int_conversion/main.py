import math
# import sys


def char(digit):  # 0 -> "0"
    return chr(digit + 48)


def digit(character):  # "0" -> 0
    return ord(character) - 48


def int_to_str(n):  # requires n >= 0
    digits = []
    while True:
        n, r = divmod(n, 10)  # n // 10, n % 10
        digits.append(char(r))
        if n == 0:
            break

    return "".join(reversed(digits))


def str_to_int(s):  # requires result >= 0
    n = 0
    for ch in s:
        n = 10 * n + digit(ch)
    return n


def main():
    # sys.set_int_max_str_digits(0)
    answer = math.factorial(10000)
    print(f"{answer=}")


if __name__ == '__main__':
    main()

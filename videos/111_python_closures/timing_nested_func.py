import timeit


def is_str(x) -> bool:
    return isinstance(x, str)


def accepts_func(func, s):
    if func(s):
        return 0
    else:
        return 42


def f1():
    return accepts_func(is_str, "hello")


def f2():
    return accepts_func((lambda x: isinstance(x, str)), "hello")


def main():
    number = 1000000
    t1 = timeit.timeit(stmt="f1()", globals=globals(), number=number)
    t2 = timeit.timeit(stmt="f2()", globals=globals(), number=number)

    print(f"{t1=}")
    print(f"{t2=}")
    print(f"{t1/t2=}")
    print(f"{t2/t1=}")


if __name__ == '__main__':
    main()

import timeit


def bool_convert(x):
    return bool(x)


def notnot_convert(x):
    return not not x


def dunder_bool_convert(x):
    return x.__bool__()


def if_x(x):
    if x:
        pass


def if_notnot_x(x):
    if not not x:
        pass


def nop(x):
    pass


def main():
    trials = 10_000_000
    kwargs = {
        'setup': 'x=42',
        'globals': globals(),
        'number': trials,
    }

    notnot_time = timeit.timeit("notnot_convert(x)", **kwargs)
    bool_time = timeit.timeit("bool_convert(x)", **kwargs)
    dunder_bool_time = timeit.timeit("dunder_bool_convert(x)", **kwargs)
    if_x_time = timeit.timeit("if_x(x)", **kwargs)
    if_notnot_x_time = timeit.timeit("if_notnot_x(x)", **kwargs)
    function_call_time = timeit.timeit("nop(x)", **kwargs)

    print(f'{bool_time=:.02f}')
    print(f'{dunder_bool_time=:.02f}')
    print(f'{notnot_time=:.02f}')
    print(f'{if_x_time=:.02f}')
    print(f'{if_notnot_x_time=:.02f}')
    print(f'{function_call_time=:.02f}')


if __name__ == '__main__':
    main()

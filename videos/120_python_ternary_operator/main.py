def form(a, cond, b):
    # cond ? a : b
    return a if cond else b


def abs_example(x):
    return x if x >= 0 else -x


def division_example(value):
    x = 1 / value if value != 0 else 0

    if value != 0:
        x = 1 / value
    else:
        x = 0


def list_example(vals: list):
    result = vals[-1] if vals else 0


def default_arg(some_arg=None):
    some_arg = [] if some_arg is None else some_arg


def beware_precedence(x):
    z = x + 1 if x > 0 else 2 * x - 1  # x+1 or 2x-1
    z = (x + 1) if x > 0 else (2 * x - 1)  # x+1 or 2x-1
    z = x + (1 if x > 0 else 2 * x - 1)  # x+1 or 3x-1
    z = x + (1 if x > 0 else 2 * x) - 1  # x or 2x-1

from timeit import timeit


def f(a, b, c):
    print(f'{a=}, {b=}, {c=}')


def either_way_works_example():
    f(1, 2, 3)
    f(a=1, b=2, c=3)
    f(c=3, a=1, b=2)
    f(1, c=3, b=2)

    # f(c=3, 1, b=2) # SyntaxError


def cannot_repeat_args():
    # f(1, a=1, b=2, c=3) # TypeError

    # f(a=1, a=1, b=2, c=3) # SyntaxError, errors before you even call the function

    kwargs = {'a': 1}
    # f(a=1, b=2, c=3, **kwargs)  # TypeError


def g(a, b, *, kw_only):
    print(f'{a=}, {b=}, {kw_only=}')


def g(a, b, *args, kw_only):
    if args:
        raise ValueError(f"unexpected positional arguments: {args}")
    print(f'{a=}, {b=}, {kw_only}')


def func(a, b, c, *args, kw1, kw2, k3, **kwargs):
    pass


def force_keyword_argument():
    # g(1, 2, 3) # SyntaxError
    g(1, b=2, kw_only=3)
    g(a=1, b=2, kw_only=3)
    g(kw_only=3, a=1, b=2)

    # g(b=2, 1, kw_only=3) # SyntaxError

    # Using * better than *args
    # g(1, 2, "oops", kw_only=3)


def eat_args(*args):
    print(args, "yum")


def eat_kwargs(**kwargs):
    print(kwargs, "yum!")


def args_will_not_eat_kwargs_and_vice_versa():
    eat_args(kw=3)  # TypeError
    eat_kwargs(1, 2)  # TypeError


def combine(a, b):
    result = []
    result.extend(a)
    result.extend(b)
    return result


def combine(a, b, *, validator=None, key=None):
    if key is not None:
        a = map(key, a)
        b = map(key, b)
    result = []
    result.extend(a)
    result.extend(b)
    if validator is not None:
        if not all(map(validator, result)):
            raise ValueError("invalid elements")
    return result


def why_kw_only_args_were_added():
    x = combine(["s", "u", "b"], ("s", "c", "r", "i", "b", "e"))
    # bad = combine([1, 2, 3], (4, 5, 6), [7, 8, 9]) # TypeError
    # bad = combine([1, 2, 3], (4, 5, 6), "oops", key=len) # TypeError

    y = combine(["s", "u", "b"], ("s", "c", "r", "i", "b", "e"), key=len)
    y = combine(["s", "u", "b"], ("s", "c", "r", "i", "b", "e"), key=len, validator=(lambda n: n > 0))


def place_order(*, item, price, quantity):
    print(f"placing order for {quantity} units of {item} at {price} price")
    # would be very bad for someone to mix up these arguments, consider forcing them to be kw_only
    # ordering 10 units at price of 1000 vs order 1000 units at price of 10


def kws_with_no_defaults(val=None, *, kw1, kw2=None, kw3, kw4=None):
    pass


def check_truthy(x, /):  # should someone be able to pass this by name??
    if not x:
        raise ValueError(f"expected truthy object, got: {x}")


def check_truthy(*vals):
    for v in vals:
        if not v:
            raise ValueError(f"expected truthy object, got: {v}")


def power_mod(x, y, /, *, mod):
    return (x ** y) % mod  # Note: this is a very slow way to do it, instead use fast pow but reduce mod n each step


def force_positional_arguments():
    check_truthy("subscribe")
    check_truthy(True)
    # check_truthy(x=5)
    check_truthy(1, 2, [3])
    z = power_mod(3, 50, mod=17)


def mix_and_match_most_general(pos_1, pos_2, /, pos_or_kw_1, pos_or_kw_2, *, kw_1, kw_2, **kwargs):
    pass


def position_only_builtin_examples():
    # Many examples of positional-only
    d = {"a": 1, "b": 2}
    x = d.get("c", "missing")
    y = d.get("c", default="missing")  # Error!!! default is positional only


def kw_only_builtin_examples():
    # Many examples of kw-only
    # json.load
    def load(fp, *, cls=None, object_hook=None, parse_float=None, parse_int=None, parse_constant=None, object_pairs_hook=None, **kw):
        pass

    # os.path.realpath
    def realpath(path, *, strict=False):
        pass

    # pprint.pprint
    def pprint(object, stream=None, indent=1, width=80, depth=None, *, compact=False, sort_dicts=True, underscore_numbers=False):
        pass


def both_pos_and_kw_only_builtin_examples():
    # ZERO examples I could find (outside tests) that use both

    # Some examples that use /, * with nothing inbetween
    def dataclass(cls=None, /, *, init=True, repr=True, eq=True, order=False,
                  unsafe_hash=False, frozen=False, match_args=True,
                  kw_only=False, slots=False):
        pass

    @dataclass
    class A:
        x: int


def speed_differences():
    def func(a, b, c):
        pass

    trials = 10 ** 7
    display_scale = 10 ** 9  # nanoseconds

    t1 = timeit(stmt="func(1, 2, 3)", globals={'func': func}, number=trials) / trials * display_scale
    t2 = timeit(stmt="func(a=1, b=2, c=3)", globals={'func': func}, number=trials) / trials * display_scale
    t3 = timeit(stmt="func(c=3, a=1, b=2)", globals={'func': func}, number=trials) / trials * display_scale
    t4 = timeit(stmt="func(1, c=3, b=2)", globals={'func': func}, number=trials) / trials * display_scale

    def func(a, b, c, /):
        pass

    t5 = timeit(stmt="func(1, 2, 3)", globals={'func': func}, number=trials) / trials * display_scale

    def func(*, a, b, c):
        pass

    t6 = timeit(stmt="func(a=1, b=2, c=3)", globals={'func': func}, number=trials) / trials * display_scale
    t7 = timeit(stmt="func(c=3, b=2, a=1)", globals={'func': func}, number=trials) / trials * display_scale

    print("normal func")
    print(f'{t1=:.2f}\t\t func(1, 2, 3)')
    print(f'{t2=:.2f}\t\t func(a=1, b=2, c=3)')
    print(f'{t3=:.2f}\t\t func(c=3, a=1, b=2)')
    print(f'{t4=:.2f}\t\t func(1, c=3, b=2)')
    print()

    print("pos only")
    print(f'{t5=:.2f}\t\t func(1, 2, 3)')
    print()

    print("kw only")
    print(f'{t6=:.2f}\t\t func(a=1, b=2, c=3)')
    print(f'{t7=:.2f}\t\t func(c=3, b=2, a=1)')


def main():
    pass
    # either_way_works_example()
    # cannot_repeat_args()
    # force_keyword_argument()
    # why_kw_only_args_were_added()
    # args_will_not_eat_kwargs_and_vice_versa()
    speed_differences()


if __name__ == '__main__':
    main()

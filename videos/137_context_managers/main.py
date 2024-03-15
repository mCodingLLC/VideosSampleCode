import copy
import decimal
import os
import socket
import sys
import tempfile
import threading
from contextlib import ExitStack, contextmanager, suppress

lock = threading.Lock()
global_state = []


def hello():
    with open(...) as fp:
        ...

    fp = open(...)
    try:
        ...
    finally:
        fp.close()


def non_cm_examples():
    fp = open("test.txt", "w")
    fp.write("Hello World")
    fp.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1.0)  # seconds
    s.connect(("mcoding.io", 80))
    s.close()

    fp = tempfile.NamedTemporaryFile()
    fp.write(b"Hello World")
    fp.close()

    lock.acquire()
    global_state.append(42)
    lock.release()


def cm_examples():
    with open("test.txt", "w") as fp:
        fp.write("Hello World")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(1.0)  # seconds
        s.connect(("mcoding.io", 80))

    with tempfile.TemporaryFile() as fp:
        fp.write(b"Hello World")

    with lock:
        global_state.append(42)


def cm_multi_example():
    with open("test.txt") as fp:
        with open("test2.txt", "w") as fp2:
            fp2.write(fp.read())

    with open("test.txt") as fp, open("test2.txt", "w") as fp2:
        fp2.write(fp.read())


def exit_stack_example():
    filenames = [f"test{n}.txt" for n in range(3)]
    with ExitStack() as stack:
        fps = [stack.enter_context(open(filename, "w")) for filename in filenames]
        ...


def file_example_no_cm():
    fp = open("test.txt", "w")
    fp.write("Hello World")
    fp.close()


def file_example_no_cm_early_return(early_return_condition):
    fp = open("test.txt", "w")
    if early_return_condition:
        return
    ...  # many lines later
    fp.close()


def file_example_cm():
    with open("test.txt", "w") as fp:
        fp.write("Hello World")


def add_print_to_close(obj):
    old_close = obj.close

    def new_close():
        print("closing")
        old_close()

    obj.close = new_close
    return obj


def file_example_cm():
    fp = open("test.txt", "w")
    fp = add_print_to_close(fp)

    print("before with")
    with fp:
        print("inside with")
        fp.write("Hello World")
    print("after with")


def file_example_cm_with_exc():
    fp = open("test.txt", "w")
    fp = add_print_to_close(fp)

    try:
        print("before with")
        with fp:
            print("inside with")
            raise ValueError("bad")
        print("after with")
    except ValueError as exc:
        print("caught exception", exc)


def file_example_cm_with_return():
    def inner():
        fp = open("test.txt", "w")
        fp = add_print_to_close(fp)

        print("before with")
        with fp:
            print("inside with")
            return print("returning!")
        print("after with")

    inner()
    print("after return")


def file_example_try_finally():
    fp = open("test.txt", "w")
    try:
        fp.write("Hello World")
    finally:
        fp.close()


def file_example_try_except_finally():
    fp = open("test.txt", "w")
    print("before try")
    try:
        raise ValueError("bad")
    except ValueError as exc:
        print("caught exception", exc)
    finally:
        print("closing")
        fp.close()
    print("after try")


def file_example_try_finally_interrupt():
    fp = open("test.txt", "w")
    try:
        return "inside"
    finally:
        fp.close()
        return "finally"


def try_finally_infinite_loop():
    while True:
        print("loop")
        try:
            return "inside"
        finally:
            continue


def file_example_try_finally_lost_exc():
    fp = open("test.txt", "w")
    try:
        raise ValueError("bad")
    finally:
        fp.close()
        return  # exception is now gone


def with_statement_semantics():
    with open("test.txt", "w") as fp:
        fp.write("Hello World")

    # same as
    manager = open("test.txt", "w")
    enter = type(manager).__enter__
    exit = type(manager).__exit__
    value = enter(manager)
    hit_except = False

    try:
        fp = value
        fp.write("Hello World")
    except:
        hit_except = True
        if not exit(manager, *sys.exc_info()):
            raise
    finally:
        if not hit_except:
            exit(manager, None, None, None)


def try_finally_vs_with_statement():
    fp = open("test.txt", "w")
    try:
        fp.write("Hello World")
    finally:
        fp.close()

    with open("test.txt", "w") as fp:
        fp.write("Hello World")


class MyContextManager:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        ...


def my_cm_example():
    with MyContextManager() as cm:
        raise ValueError


def suppress_example():
    # remove it if it exists,
    # otherwise I don't care

    with suppress(OSError):
        os.remove("test.txt")


def _api_begin(arg):
    print(f"api begin: {arg}")
    return {"status": "ok"}


def _api_end():
    print("api end")


def api_begin(arg):
    val = _api_begin(arg)
    return _ExternalAPIContextManager(val)


class _ExternalAPIContextManager:
    def __init__(self, val):
        self.val = val

    def __enter__(self):
        return self.val

    def __exit__(self, exc_type, exc_val, exc_tb):
        _api_end()


def external_api_example():
    val = _api_begin("arg")
    print(f"use val: {val}")
    _api_end()

    # instead
    with api_begin("arg") as val:
        print(f"use val: {val}")


@contextmanager
def api_begin2(arg):
    val = _api_begin(arg)
    yield val
    _api_end()


@contextmanager
def api_begin3(arg):
    val = _api_begin(arg)
    try:
        yield val
    finally:
        _api_end()


class ActualContextManager:
    def __enter__(self):
        global global_state
        self.saved = global_state
        global_state = copy.deepcopy(global_state)
        # mutate copy if desired
        return global_state

    def __exit__(self, exc_type, exc_val, exc_tb):
        global global_state
        global_state = self.saved
        self.saved = None


def pi():
    # https://docs.python.org/3/library/decimal.html#module-decimal
    decimal.getcontext().prec += 2
    three = decimal.Decimal(3)
    lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
    while s != lasts:
        lasts = s
        n, na = n + na, na + 8
        d, da = d + da, da + 32
        t = (t * n) / d
        s += t
    decimal.getcontext().prec -= 2
    return +s


def decimal_example():
    print(pi())

    with decimal.localcontext(prec=100):
        print(pi())


def nice_exit_example():
    try:
        sys.exit(1)
    finally:
        print("printing on the way out...")


def not_nice_exit_example():
    try:
        os._exit(1)
    finally:
        print("this does not print")


class UnluckyContextManager:
    def __enter__(self):
        lock.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        lock.release()


def unlucky_context_manager_example():
    try:
        while True:  # interrupt me!
            with lock:
                pass
    finally:
        print(f"lock released on exit? {not lock.locked()}")


def main():
    # cm_examples()
    # non_cm_examples()
    # cm_multi_example()
    # file_example_cm()
    # file_example_cm_with_exc()
    # file_example_cm_with_return()
    # file_example_try_finally_lost_exc()
    # try_finally_infinite_loop()
    # with_statement_semantics()
    # try_finally_vs_with_statement()
    # my_cm_example()
    # suppress_example()
    # external_api_example()
    # decimal_example()
    # nice_exit_example()
    # not_nice_exit_example()
    unlucky_context_manager_example()


if __name__ == "__main__":
    main()

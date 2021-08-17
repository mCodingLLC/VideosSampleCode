import os
import sys
import time


def try_raising_a_string():
    raise "error"  # Error, not a BaseException


def sys_exit_example():
    try:
        sys.exit()
    except:
        print("handling exception...")
    print("process did not exit due to sys.exit")


def sleep_loop_cancel_example():
    while True:
        try:
            print("doing work")
            time.sleep(1)
        except Exception:
            print("handling exception...")


def close_despite_exception_handling():
    try:
        os._exit(1)
    except:
        print("os exit cannot be caught, this will not print")


def gen():
    try:
        yield 0
    except GeneratorExit:
        print("gen exit")
        raise


def gen_exit_example():
    g = gen()
    next(g)
    g.close()


def main():
    # try_raising_a_string()
    # sys_exit_example()
    # sleep_loop_cancel_example()
    # close_despite_exception_handling()
    gen_exit_example()


if __name__ == '__main__':
    main()

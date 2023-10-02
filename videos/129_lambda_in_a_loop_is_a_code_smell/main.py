import functools
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, Future

io_lock = threading.Lock()


def print_ts(*args):
    with io_lock:
        print(*args)


def print_task_completed(future: Future, task_id: str):
    if future.exception() is None:
        print_ts(f"completed")
    else:
        print_ts(f"completed with error")


def dispatch_work(work: list[tuple[str, Callable]]):
    with ThreadPoolExecutor(max_workers=4) as executor:
        for task_id, func in work:
            future = executor.submit(func)
            future.add_done_callback(
                functools.partial(print_task_completed, task_id=task_id)
            )
            # future.add_done_callback(
            #     lambda fut: print_task_completed(fut, task_id)
            # )


def some_work(arg):
    time.sleep(0.0)  # simulate work
    print_ts(arg)


def main():
    work = [
        ("task_a", functools.partial(some_work, "A")),
        ("task_b", functools.partial(some_work, "B")),
        ("task_c", functools.partial(some_work, "C")),
        ("task_d", functools.partial(some_work, "D")),
    ]
    dispatch_work(work)
    print("all done")


if __name__ == '__main__':
    main()

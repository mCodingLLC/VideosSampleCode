import random
import time

import pytest


def basic_syntax_for():
    for x in range(3):
        if x == 2:
            break
        print(x)
    else:
        print("DONE")


def basic_syntax_while():
    x = 0
    while x < 3:
        if x == 2:
            break
        print(x)
        x += 1
    else:
        print("DONE")


def the_intuition():
    x = 0
    # START
    if x < 3:
        ...  # a break would GOTO END
        x += 1
        # GOTO START
    else:  # no break
        print("while terminated without break or exception")
    # END


def index_foundflag(seq, target):
    found = False
    for idx, val in enumerate(seq):
        if val == target:
            found = True
            break
    if not found:
        raise ValueError(f'{target} is not in the sequence')
    return idx


def index_forelse(seq, target):
    for idx, val in enumerate(seq):
        if val == target:
            break
    else:  # no break
        raise ValueError(f'{target} is not in the sequence')
    return idx


def index_return(seq, target):
    for idx, val in enumerate(seq):
        if val == target:
            return idx
    raise ValueError(f'{target} is not in the sequence')


def countdown_flag(groups, ticks_per_group):
    ticks = [ticks_per_group - 1] * groups
    yield tuple(ticks)
    keep_going = True
    while keep_going:
        keep_going = False
        for group in reversed(range(groups)):
            if ticks[group] != 0:  # can subtract 1 from this group
                ticks[group] -= 1
                yield tuple(ticks)
                keep_going = True
                break
            ticks[group] = ticks_per_group - 1  # reset


def countdown_forelse(groups, ticks_per_group):
    ticks = [ticks_per_group - 1] * groups
    yield tuple(ticks)
    while True:
        for group in reversed(range(groups)):
            if ticks[group] != 0:  # can subtract 1 from this group
                ticks[group] -= 1
                yield tuple(ticks)
                break
            ticks[group] = ticks_per_group - 1  # reset
        else:
            return


def random_error():
    return random.random() > .9


def process_for_5_seconds_errorflag():
    random.seed(4)
    start = time.perf_counter()
    target_time = start + 5

    errored = False
    while (now := time.perf_counter()) < target_time:
        print(f"keep working, it's only been {now - start:.2f}s")
        if random_error():
            errored = True
            break
        time.sleep(.5)

    if errored:
        print("handling error...")
    else:
        print("done!")


def process_for_5_seconds_whileelse():
    random.seed(4)
    start = time.perf_counter()
    target_time = start + 5

    while (now := time.perf_counter()) < target_time:
        print(f"keep working, it's only been {now - start:.2f}s")
        if random_error():
            break
        time.sleep(.5)
    else:  # no break
        print("done!")
        return
    print("handling error...")


def not_all_elses_are_bad(x, y):
    try:
        z = x / y
        ...
    except ZeroDivisionError:
        # was it the x / y that raised?
        # or something in the ...?
        return float('nan')

    try:
        z = x / y
    except ZeroDivisionError:
        return float('nan')
    else:
        ...  # safe to use z


def main():
    assert index_forelse([0, 1, 2, 3], 0) == 0
    assert index_forelse([3, 2, 1, 0], 0) == 3
    assert index_forelse([3, 1, 0, 2], 0) == 2
    with pytest.raises(ValueError):
        index_forelse([0, 1, 2, 3], 5)

    # better to use builtin .index of list
    assert [0, 1, 2, 3].index(0) == 0


if __name__ == '__main__':
    main()

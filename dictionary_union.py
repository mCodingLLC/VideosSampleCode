import random
import time


def test_combining_list_set():
    d = [1, 2, 3]
    e = [4]
    assert d + e == [1, 2, 3, 4]

    d = {1, 2, 3}
    e = {4}
    assert d | e == {1, 2, 3, 4}


def test_dict_or_disjoint_keys():
    d = {'spam': 1, 'eggs': 2, 'cheese': 3}
    e = {'extra': 4}

    assert d | e == {'spam': 1, 'eggs': 2, 'cheese': 3, 'extra': 4}
    assert d == {'spam': 1, 'eggs': 2, 'cheese': 3}
    assert e == {'extra': 4}


def test_dict_or_non_disjoint_keys():
    d = {'spam': 1, 'eggs': 2, 'cheese': 3}
    e = {'cheese': 5, 'extra': 4}

    assert d | e == {'spam': 1, 'eggs': 2, 'cheese': 5, 'extra': 4}
    assert d == {'spam': 1, 'eggs': 2, 'cheese': 3}
    assert e == {'cheese': 5, 'extra': 4}


def test_dict_or_not_commutative():
    d = {'spam': 1, 'eggs': 2, 'cheese': 3}
    e = {'cheese': 5, 'extra': 4}

    assert d | e == {'spam': 1, 'eggs': 2, 'cheese': 5, 'extra': 4}
    assert e | d == {'spam': 1, 'eggs': 2, 'cheese': 3, 'extra': 4}
    assert d | e != e | d


def test_not_even_plain_or_is_commutative():
    a = True
    b = 1

    assert a is not b
    assert a or b is a
    assert b or a is b


def test_dict_ior_syntax():
    d = {'spam': 1, 'eggs': 2, 'cheese': 3}
    e = {'extra': 4}

    d |= e
    # same as d.update(e)

    assert d == {'spam': 1, 'eggs': 2, 'cheese': 3, 'extra': 4}

    # syntax error
    # (d |= e) == {'spam': 1, 'eggs': 2, 'cheese': 3, 'extra': 4}


def test_time_dict_aggregation():
    M = 1000000
    size = 1000000
    a = {x: random.randint(0, M) for x in range(size)}
    b = {x: random.randint(0, M) for x in range(size)}
    c = {x: random.randint(0, M) for x in range(size)}
    d = {x: random.randint(0, M) for x in range(size)}

    start = time.perf_counter()
    e = a | b | c | d
    elapsed1 = time.perf_counter() - start
    print()
    print(elapsed1)

    start = time.perf_counter()
    e = {}
    for other in [a, b, c, d]:
        e |= other
    elapsed2 = time.perf_counter() - start
    print(elapsed2)

    improvement = elapsed1 - elapsed2
    assert improvement > 0

    print(f'Improvement of {elapsed1 - elapsed2} seconds')

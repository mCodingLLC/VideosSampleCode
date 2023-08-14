import pytest

from id_mapping import IdMapping, IdSet


def test_id_mapping_set_get_list():
    counts = [1, 2, 3]

    mapping = IdMapping()
    assert not mapping
    assert len(mapping) == 0

    mapping[counts] = 1234

    assert mapping
    assert len(mapping) == 1
    assert mapping[counts] == 1234
    assert counts in mapping
    assert counts in mapping.keys()
    assert list(mapping.keys())[0] is counts

    del mapping[counts]
    assert not mapping
    assert len(mapping) == 0


def test_id_set_set_get_list():
    counts = [1, 2, 3]

    id_set = IdSet()

    assert not id_set
    assert len(id_set) == 0

    id_set.add(counts)

    assert len(id_set) == 1
    assert counts in id_set
    assert list(id_set)[0] is counts

    id_set.add(counts)

    assert len(id_set) == 1
    assert counts in id_set
    assert list(id_set)[0] is counts

    id_set.remove(counts)

    assert counts not in id_set
    assert len(id_set) == 0
    assert not id_set


def test_compare_to_normal_set():
    s = set()
    s.add(frozenset({1, 2, 3}))
    assert len(s) == 1
    s.add(frozenset({1, 2, 3}))
    assert len(s) == 1

    s = IdSet()
    s.add(frozenset({1, 2, 3}))
    assert len(s) == 1
    s.add(frozenset({1, 2, 3}))
    assert len(s) == 2

    s = IdSet()
    item = frozenset({1, 2, 3})
    s.add(item)
    assert len(s) == 1
    s.add(item)
    assert len(s) == 1


def do_once(stuff, op):
    seen = set()
    for x in stuff:
        if x in seen:
            continue
        op(x)


def test_ints_trouble():
    mapping = IdMapping()

    mapping[257] = "find me"
    with pytest.raises(KeyError):
        mapping[int(float(257))]  # even though the keys are equal, they have different ids!


def test_python_doesnt_let_you_store_things():
    x = set()

    with pytest.raises(TypeError):
        x.add([])

    class A:
        pass

    x.add(A())  # OK

    class B:
        def __eq__(self, other):
            return self is other

    with pytest.raises(TypeError):
        x.add(B())

    class C:
        def __eq__(self, other):
            return self is other

        def __hash__(self):
            return 42  # bad hash!

    x.add(C())  # OK, even though hash is bad

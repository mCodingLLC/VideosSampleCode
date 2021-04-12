class BadList(list):

    def __add__(self, other):
        print("running custom add")
        return BadList(super(BadList, self).__add__(other))

    def __iadd__(self, other):
        print("running custom iadd")
        return self + other


def plusequals_may_change_pointers():
    x = 1
    print(id(x))
    x += 1
    print(id(x), "changed")

    x = []
    print(id(x))
    x += [1]
    print(id(x), "not changed")

    bad = BadList()
    print(bad, "before append")
    bad += [1, 2, 3]  # manual extend
    append_some_to_list(bad)  # might do nothing?
    print(bad, "after append")


def append_some_to_list(l):
    l += [4, 5, 6]


def plusequals_meaning(x, y):
    # x += y
    result = x.__iadd__(y)
    x = result

    # x[0] += y
    result = x[0].__iadd__(y)  # calls __getitem__
    x[0] = result  # calls __setitem__

    # x.val += y
    result = x.val.__iadd__(y)  # calls __getattr__
    x.val = result  # calls __setattr__


def tuple_what():
    # a_tuple = (1, 2)
    # a_tuple[0] += 1  # obvious error, tuple immutable

    pros_and_cons = (["subscribing helps James", "subscribing feels good"],
                     ["I have to click"])
    pros = pros_and_cons[0]
    pros += ["big numbers are cool"]  # fine

    try:
        pros_and_cons[0] += ["James is cool"]  # maybe?
    except TypeError:
        print("Error!")
    print(pros_and_cons)  # wat?


def main():
    # tuple_what()
    plusequals_may_change_pointers()


if __name__ == '__main__':
    main()

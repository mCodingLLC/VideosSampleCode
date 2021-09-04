def chained_comparisons_good_uses(x, y, z):
    if 0 < x < 1:
        print("x in range (0,1)")

    if 0 <= x < 1:
        print("x in range [0,1)")

    if x <= y <= z:
        print("y in range [x,z]")

    if x >= y >= 1:
        print("y in range [1,x]")

    if x == y == z:
        print("x,y,z all equal")


def chained_comparisons_ok_to_questionable_uses(x, y, z):
    if 0 < x < y == z < 1:
        print("x,y in (0,1) with x<y and z==y")

    if x <= y <= z != 1:
        print("y in range(x,z) with z != 1")

    if x == y == z != 1:
        print("x,y,z all equal something that isn't 1")

    if x is y is z:
        print("x,y,z all identical")

    if x is y is z in [1, 2, 3]:
        print("x,y,z all identical and in [1,2,3]")


def chained_comparisons_bad_uses(x, y, z):
    if x < y > z:
        print("y > max(x,z)")

    if x != y != z:
        print("kinda looks like x,y,z all distinct, but may have x==z")

    if 0 > x < y != z > 1:
        print("WHY??")

    if 0 < x > 1 >> y << 1 < z > 1:
        print("please remove this from the language")


def maybe_someday():
    import numpy as np
    x = np.arange(10)
    y = x[3 < x < 5] # not today
    y = x[(3 < x) & (x < 5)]


def rules_of_thumb(x, y, z):
    pass
    # my personal rules of thumb for chained comparisons
    # feel free to use <, <=, and == together
    # feel free to use >, >=, and == together
    # do not use <, <= with >, >=
    # feel free to use multiple == in a row
    # do not use != anywhere in a chain
    # do not use "is" or "in" in a chain


def main():
    x, y, z = 0, 1, 2

    if x < y > z:
        print(True)
    else:
        print(False)

    comparisons = ['<', '>', '<=', '>=', '==', '!=', 'is', 'is not', 'in', 'not in']


if __name__ == '__main__':
    main()

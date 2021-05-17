from itertools import zip_longest


def basic_zip():
    x = [1, 2, 3]
    y = ['a', 'b', 'c']

    z = zip(x, y)
    print(type(z), repr(z))  # zip is lazy and it is an iterable

    for pair in zip(x, y):
        print(pair)

    for l, r in zip(x, y):
        print(f'{l=}, {r=}')

    for t in zip(x, x, x, x, x):
        print(t)


def zip_shortest_behavior():
    x = [1, 2, 3, 4, 5, 6]
    y = ['a', 'b', 'c']
    print(list(zip(x, y)))


def zip_strict_behavior():
    # new in python 3.10
    x = [1, 2, 3, 4, 5, 6]
    y = ['a', 'b', 'c']
    # print(list(zip(x, y, strict=True))) # raises due to different lengths


def zip_longest_behavior():
    x = [1, 2, 3, 4, 5, 6]
    y = ['a', 'b', 'c']
    print(list(zip_longest(x, y)))
    print(list(zip_longest(x, y, fillvalue='?')))


def main():
    # basic_zip()
    # zip_shortest_behavior()
    # zip_strict_behavior()
    zip_longest_behavior()


if __name__ == '__main__':
    main()

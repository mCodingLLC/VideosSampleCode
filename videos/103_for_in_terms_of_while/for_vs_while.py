def main():
    expr = [1, 2, 3]

    for x in expr:
        print(x)


def main():
    expr = [1, 2, 3]

    it = iter(expr)
    while True:
        x = next(it)
        print(x)


def main():
    expr = [1, 2, 3]

    it = iter(expr)
    while True:
        try:
            x = next(it)
            print(x)
        except StopIteration:
            break


def main():
    expr = [1, 2, 3]

    it = iter(expr)
    while True:
        try:
            x = next(it)
        except StopIteration:
            break
        else:
            print(x)


def main():
    expr = [1, 2, 3]

    it = iter(expr)
    for x in it:
        print(x)


if __name__ == '__main__':
    main()

def multiple_assignment_expresssions():
    (a := (b := (c := (d := 0))))
    print(a, b, c, d)


def multiple_assignments():
    a = b = c = d = []
    print(a, b, c, d)
    print(a is b)

    tmp = []
    a = tmp
    b = tmp
    c = tmp
    d = tmp


def tricky_assignments():
    a, b = a[:] = [[]], []
    print(a, b)

    tmp = [[]], []
    a, b = tmp
    a[:] = tmp
    print(a is a[0])


def tricky_assignments2():
    a, b = a[b] = a = [1, 2, 3], 2
    print(a, b)


def main():
    multiple_assignments()
    tricky_assignments()
    multiple_assignment_expresssions()
    tricky_assignments2()


if __name__ == '__main__':
    main()

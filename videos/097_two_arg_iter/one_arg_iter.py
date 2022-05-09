class LucasSequence:
    """Represents the sequence: x_n = p * x_{n-1} - q * x_{n-2}"""

    def __init__(self, x0, x1, p, q):
        self.x0, self.x1 = x0, x1
        self.p, self.q = p, q

    def __iter__(self):
        a, b = self.x0, self.x1
        yield a
        yield b
        p, q = self.p, self.q
        while True:
            a, b = b, p * b - q * a
            yield b


def main():
    fib = LucasSequence(0, 1, 1, -1)
    for n in fib:
        print(n)
        if n == 3:
            break


if __name__ == '__main__':
    main()

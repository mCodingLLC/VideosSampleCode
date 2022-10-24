import math
import random


def fuzz_test(func, trials):
    for _ in range(trials):
        a = random.randint(-100, 100)
        b = random.randint(-100, 100)
        c = random.randint(-100, 100)
        try:
            func(a, b, c)
        except Exception as exc:
            exc.add_note(f"Found exception with input {(a, b, c)=}")
            raise


def quadratic_solve(a, b, c):
    return [
        (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a),
        (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a),
    ]


def add_note_example():
    random.seed(0)

    fuzz_test(quadratic_solve, 1000)


if __name__ == "__main__":
    add_note_example()

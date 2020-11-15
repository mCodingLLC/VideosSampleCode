import heapq
from random import sample, random


def sample_stream(iterable, n):
    return heapq.nlargest(n, iterable, key=lambda _: random())

def main():
    print(sample(range(100000), 10))
    with open('words.txt') as f:
        print(sample_stream(f, 10))


if __name__ == '__main__':
    main()

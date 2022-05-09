import functools
import time


def something():
    return 42


def useless_example():
    it = iter(something, 42)
    print(next(it))
    print(next(it))


def two_arg_iter(f, sentinel):
    while True:
        val = f()
        if val == sentinel:
            return
        yield val


class ChunkedReader:
    def __init__(self, f, chunk_size=64):
        self.f = f
        self.chunk_size = chunk_size

    def read_chunk(self):
        return self.f.read(self.chunk_size)


def chunk_example():
    with open('example.txt', 'rb') as f:
        reader = ChunkedReader(f, 4)
        for chunk in iter(reader, b''):
            print(f"chunk: {chunk}")


def alternate_way_to_chunk_example():
    with open('example.txt', 'rb') as f:
        for chunk in iter(functools.partial(f.read, 4), b''):
            print(f"chunk: {chunk}")


def preferred_way_to_do_chunk_example():
    with open('example.txt', 'rb') as f:
        while (chunk := f.read(4)) != b'':
            print(f"chunk: {chunk}")


def beyond_what_two_arg_iter_can_do():
    t0 = time.perf_counter()
    while (t := time.perf_counter()) < t0 + 1.:
        print(f"it has been {t - t0} seconds")
        time.sleep(.1)


def thx():
    pass


def main():
    # useless_example()
    chunk_example()
    # alternate_way_to_chunk_example()
    # preferred_way_to_do_chunk_example()
    # beyond_what_two_arg_iter_can_do()
    # async iter does NOT have 2-arg form


if __name__ == '__main__':
    main()

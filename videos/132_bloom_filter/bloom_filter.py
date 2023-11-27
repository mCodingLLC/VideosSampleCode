import array
import hashlib
import itertools
import math
import random
import string
import time
from collections.abc import Callable, Iterable, MutableSequence
from dataclasses import dataclass


def _8_bools_to_int(bools) -> int:
    bin_str = ''.join('1' if b else '0' for b in reversed(bools))
    return int(bin_str, 2)


@dataclass
class BitArray:
    data: array.array[int]
    size: int

    @classmethod
    def _to_bytes(cls, iterable, iter_len_out: list):
        iterable = (bool(x) for x in iterable)
        iterable = itertools.batched(iterable, 8)
        iter_len = 0
        for x in iterable:
            iter_len += len(x)
            yield _8_bools_to_int(x)

        iter_len_out[0] = iter_len

    @classmethod
    def from_iterable(cls, iterable: Iterable):
        iter_len = [0]
        iterable = cls._to_bytes(iterable, iter_len_out=iter_len)
        data = array.array('B', iterable)
        size = iter_len[0]
        return cls(data=data, size=size)

    @classmethod
    def zeros(cls, n: int):
        arr_size, remainder = divmod(n, 8)
        if remainder:
            arr_size += 1
        data = array.array('B', (0 for _ in range(arr_size)))
        return cls(data=data, size=n)

    def _check_index(self, n):
        if not isinstance(n, int):
            raise TypeError("expected int")
        if not 0 <= n < self.size:
            raise IndexError(n)

    def __getitem__(self, n):
        self._check_index(n)
        arr_idx, bit_idx = divmod(n, 8)
        return (self.data[arr_idx] >> bit_idx) & 0b1

    def __setitem__(self, n, bit):
        self._check_index(n)
        arr_idx, bit_idx = divmod(n, 8)
        data = self.data[arr_idx]
        data &= ~(1 << bit_idx)  # clear bit
        data |= (bool(bit) * (1 << bit_idx))  # set bit
        self.data[arr_idx] = data

    def __repr__(self):
        return f"{self.__class__.__name__}({list(self)})"

    def __len__(self):
        return self.size


@dataclass
class BloomFilter[T]:
    mem: MutableSequence[int]
    calc_hashes: Callable[[T], Iterable[int]]

    @staticmethod
    def estimate_false_positive_rate(n_hashes: int, mem_size: int, n_items: int):
        return (1.0 - math.exp(- n_hashes * n_items / mem_size)) ** n_hashes

    def add(self, item: T):
        for h in self.calc_hashes(item):
            self.mem[h % len(self.mem)] = 1

    def __contains__(self, item: T):
        return all(self.mem[h % len(self.mem)] for h in self.calc_hashes(item))


def split_long_hash[T](
        hash_fn: Callable[[T], int],
        digest_size: int,
        hashes: int,
        bytes_per_hash: int,
) -> Callable[[T], list[int]]:
    if digest_size // hashes < bytes_per_hash:
        raise ValueError("digest not long enough")

    def calc_hashes(item):
        item_hash = hash_fn(item)
        hash_bytes = item_hash.to_bytes(digest_size)
        return [
            int.from_bytes(hash_bytes[i * bytes_per_hash:(i + 1) * bytes_per_hash])
            for i in range(hashes)
        ]

    return calc_hashes


nice_chars = string.printable


def random_str(length: int) -> str:
    return ''.join(random.choices(nice_chars, k=length))


def bitarray_example():
    bits = BitArray.from_iterable([1, 1, 0, 1, 1, 1, 0, 1])
    print(len(bits))
    # bits[0] = 0
    print(bits)
    print(BitArray.zeros(2))


@dataclass
class Timer:
    msg: str
    start: float = 0.0
    end: float = 0.0

    def __enter__(self):
        print(self.msg, end=": ")
        self.start = time.perf_counter()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.perf_counter()
        print(f"{self.end - self.start:.02f}s")


def bloom_example():
    def long_hash(s: str) -> int:
        h = hashlib.sha256()
        h.update(s.encode())
        return int.from_bytes(h.digest())

    n_hashes = 5
    bytes_per_hash = 6

    calc_hashes = split_long_hash(
        long_hash,
        digest_size=256 // 8,
        hashes=n_hashes,
        bytes_per_hash=bytes_per_hash)

    mem_size = 80_000_000
    elem_count = 10_000_000

    # mem = [0] * mem_size # ~ 8 bytes per element, (each element is a pointer)
    mem = BitArray.zeros(mem_size)  # ~ 1 bit per element
    bloom = BloomFilter[str](mem=mem, calc_hashes=calc_hashes)

    with Timer("Making strs"):
        strs = {random_str(16) for _ in range(elem_count)}

    with Timer("Adding strs"):
        for s in strs:
            bloom.add(s)

    with Timer("checking no false negatives"):
        assert all(s in bloom for s in strs)

    with Timer("checking false positives"):
        false_positives = sum((random_str(15) in bloom) for _ in range(elem_count))

    fpr_estimated = bloom.estimate_false_positive_rate(n_hashes, mem_size, elem_count)
    print(f"False positive estimate: {fpr_estimated * 100:.03f}%")

    fpr_empirical = false_positives / elem_count
    print(f"False positives: {false_positives} ({fpr_empirical * 100:.03f}%)")


def main():
    # bitarray_example()
    bloom_example()


if __name__ == '__main__':
    main()

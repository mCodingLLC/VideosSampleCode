from bisect import bisect_right
from collections.abc import Sequence
from typing import TypeVar, Optional, List

T = TypeVar('T')


def longest_increasing_subsequence(seq: Sequence[T]) -> List[T]:
    if not seq:
        return []

    idx_prev_longest: List[Optional[int]] = []  # index of prev in longest inc subseq ending at i
    idx_minimal: List[int] = []  # the index of the smallest val ending a subseq of a given len+1
    val_minimal: List[T] = []  # the smallest value ending a subseq of given len+1

    for i, curr in enumerate(seq):
        len_longest_extendable = bisect_right(val_minimal, curr)

        if len_longest_extendable == len(val_minimal):
            idx_minimal.append(i)
            val_minimal.append(curr)
        elif curr < val_minimal[len_longest_extendable]:
            idx_minimal[len_longest_extendable] = i
            val_minimal[len_longest_extendable] = curr

        idx_longest_extendable = idx_minimal[len_longest_extendable - 1] if len_longest_extendable else None
        idx_prev_longest.append(idx_longest_extendable)

    longest_subsequence_indices = make_subsequence_indices(prev_indices=idx_prev_longest,
                                                           terminal_idx=idx_minimal[-1])

    return [seq[idx] for idx in longest_subsequence_indices]


def make_subsequence_indices(prev_indices, terminal_idx):
    indices = []
    idx = terminal_idx
    while idx is not None:
        indices.append(idx)
        idx = prev_indices[idx]
    return reversed(indices)


def test_longest_increasing_subsequence():
    assert longest_increasing_subsequence([]) == []
    assert longest_increasing_subsequence([1, 2, 3]) == [1, 2, 3]
    assert longest_increasing_subsequence([1, 2, 0, 3]) == [1, 2, 3]

    assert longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == [2, 3, 7, 18]
    assert longest_increasing_subsequence([0, 8, 4, 12, 2, 10, 6, 14, 1,
                                           9, 5, 13, 3, 11, 7, 15]) == [0, 2, 6, 9, 11, 15]
    assert longest_increasing_subsequence([5]) == [5]
    assert longest_increasing_subsequence([5, 5, 5, 5, 5, 5]) == [5, 5, 5, 5, 5, 5]
    assert longest_increasing_subsequence([5, 5, 5, 5, 5, 5, 4, 3, 2, 1]) == [5, 5, 5, 5, 5, 5]


def main():
    test_longest_increasing_subsequence()


if __name__ == '__main__':
    main()

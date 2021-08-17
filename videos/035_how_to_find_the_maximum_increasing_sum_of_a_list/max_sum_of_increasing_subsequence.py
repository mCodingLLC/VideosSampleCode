def max_sum_of_increasing_subseq(seq: list[int]) -> int:
    """
    O(n^2) time, O(n) extra space
    """
    if not seq:
        return 0

    max_sum = [0 for _ in seq]  # the answer to the question if you have end on index i
    # max sum ending on index i is seq[i] + prev biggest sum, corresponding to some j < i
    for i in range(len(seq)):
        for j in range(i):
            if seq[j] <= seq[i]:
                max_sum[i] = max(max_sum[i], max_sum[j])
        max_sum[i] += seq[i]

    return max(max_sum)


class IntsAndSum:
    def __init__(self, ints: list[int], precomputed_sum: int = None):
        self.ints: list[int] = ints
        self.sum: int = precomputed_sum if precomputed_sum is not None else sum(ints)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.ints}, sum={self.sum})'

    @staticmethod
    def max(*args):
        return max(args, key=lambda x: x.sum)

    def append(self, i: int) -> None:
        self.ints.append(i)
        self.sum += i

    def copy(self):
        return IntsAndSum(ints=self.ints.copy(), precomputed_sum=self.sum)


def max_sum_of_increasing_subseq_with_elements(seq: list[int]) -> IntsAndSum:
    """
    O(n^2) time, O(n^2) extra space
    """
    if not seq:
        return IntsAndSum(ints=[])

    max_sum = [IntsAndSum(ints=[]) for _ in seq]  # the answer to the question if you have end on index i
    # max sum ending on index i is seq[i] + prev biggest sum, corresponding to some j < i
    for i in range(len(seq)):  # loop invariant: max_sum[i] is fully computed/ constant after ith iteration
        for j in range(i):
            if seq[j] <= seq[i]:
                max_sum[i] = IntsAndSum.max(max_sum[i], max_sum[j])
        max_sum[i] = max_sum[i].copy()
        max_sum[i].append(seq[i])

    return IntsAndSum.max(*max_sum)


def main():
    s0 = max_sum_of_increasing_subseq([])  # should be 0
    s1 = max_sum_of_increasing_subseq([6, 5, 7, 2, 3, 200, 4, 5])  # should be 6+7+200 = 213
    s2 = max_sum_of_increasing_subseq([3, 4, 5, 6, 20])  # should be 3+4+5+6+20 = 38

    print(s0, s1, s2)

    s0 = max_sum_of_increasing_subseq_with_elements([])  # should be 0
    s1 = max_sum_of_increasing_subseq_with_elements([6, 5, 7, 2, 3, 200, 4, 5])  # should be 6+7+200 = 213
    s2 = max_sum_of_increasing_subseq_with_elements([3, 4, 5, 6, 20])  # should be 3+4+5+6+20 = 38

    print(s0)
    print(s1)
    print(s2)

    s3 = max_sum_of_increasing_subseq([8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11]) # should be 8+12+14 = 34
    l3 = max_sum_of_increasing_subseq_with_elements([8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11])

    print(s3)
    print(l3)


if __name__ == '__main__':
    main()

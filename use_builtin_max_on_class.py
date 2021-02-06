class IntsAndSum:
    def __init__(self, ints: list[int], precomputed_sum: int = None):
        self.ints: list[int] = ints
        self.sum: int = precomputed_sum if precomputed_sum is not None else sum(ints)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.ints}, sum={self.sum})'

    # not needed, defined __gt__ instead, use builtin max
    # @staticmethod
    # def max(*args):
    #     return max(args, key=lambda x: x.sum)

    def append(self, i: int) -> None:
        self.ints.append(i)
        self.sum += i

    def copy(self):
        return IntsAndSum(ints=self.ints.copy(), precomputed_sum=self.sum)
    #
    # def __gt__(self, other):
    #     return self.sum > other.sum

    def __lt__(self, other):
        return self.sum < other.sum

def main():
    ias = [
        IntsAndSum([1, 6, 1]),
        IntsAndSum([2, 5, 1, 1, 0]),
        IntsAndSum([0, 1, 0])
    ]
    print(ias)
    # print(IntsAndSum.max(*ias))
    print("\n".join(dir(0)))
    print(max(ias))


if __name__ == '__main__':
    main()

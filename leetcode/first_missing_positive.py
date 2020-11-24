from typing import List


# Could you implement an algorithm that runs in O(n) time and uses constant extra space?
# Constraints:
#
# 0 <= nums.length <= 300
# -2^31 <= nums[i] <= 2^31 - 1

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        found = [True] + [False] * 300
        for x in nums:
            if 0 < x < 301:
                found[x] = True

        for i, f in enumerate(found):
            if not f:
                return i

        return 301

def main():
    soln = Solution()
    assert soln.firstMissingPositive([]) == 1
    assert soln.firstMissingPositive([1, 2, 0]) == 3
    assert soln.firstMissingPositive([3, 4, -1, 1]) == 2
    assert soln.firstMissingPositive([7, 8, 9, 11, 12]) == 1
    assert soln.firstMissingPositive(list(range(1, 301))) == 301


if __name__ == '__main__':
    main()

from typing import List

import numpy as np

cum_max = np.maximum.accumulate


class Solution:
    def trap(self, height: List[int]) -> int:
        if not height:
            return 0
        a = np.array(height)
        m_idx = np.argmax(a)
        return int(np.sum(cum_max(a[:m_idx]) - a[:m_idx], dtype=np.int64) + \
                   np.sum(cum_max(a[:m_idx:-1]) - a[:m_idx:-1], dtype=np.int64))


if __name__ == '__main__':
    soln = Solution()
    assert soln.trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert soln.trap([4, 2, 0, 3, 2, 5]) == 9
    assert soln.trap([]) == 0
    assert soln.trap([1]) == 0
    assert soln.trap([1, 2]) == 0
    assert soln.trap([0, 2, 1, 2, 0]) == 1

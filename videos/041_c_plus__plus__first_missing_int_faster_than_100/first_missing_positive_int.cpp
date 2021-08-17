#include <vector>

class Solution
{
public:
    int firstMissingPositive(std::vector<int> &nums)
    {
        const long long N = nums.size();
        long long curr, next;
        for (int i = 0; i < N; ++i)
        {
            curr = nums[i];
            while (0 <= curr - 1 && curr - 1 < N && curr != (next = nums[curr - 1]))
            {
                nums[curr - 1] = curr;
                curr = next;
            }
        }
        for (int i = 0; i < N; ++i)
        {
            if (nums[i] != i + 1)
                return i + 1;
        }
        return N + 1;
    }
};
def bisect_left(arr: list, x, lo=0, hi=None) -> int:
    hi = hi if hi is not None else len(arr)
    assert 0 <= lo <= hi <= len(arr)
    while lo < hi:
        mid = (lo + hi)//2 # lo + (hi-lo)//2
        if arr[mid] < x:
            lo = mid+1
        else:
            hi = mid
    return lo

def bisect_index_of(arr:list, x) -> int:
    i = bisect_left(arr, x)
    if i != len(arr) and arr[i] == x:
        return i
    raise ValueError

def test_bisections():
    assert bisect_left([], 0) == 0
    assert bisect_right([], 0) == 0
    assert bisect_left([0], 0) == 0
    assert bisect_right([0], 0) == 1
    assert bisect_left([0, 0, 0], 0) == 0
    assert bisect_right([0, 0, 0], 0) == 3
    assert bisect_left([2, 3, 3, 4, 6, 7, 8, 9], 7) == 5
    assert bisect_right([2, 3, 3, 4, 6, 7, 8, 9], 7) == 6
    assert bisect_left([2, 3, 3, 4, 6, 8, 9], 7) == 5
    assert bisect_right([2, 3, 3, 4, 6, 8, 9], 7) == 5

def main():
    T, F = True, False
    [2, 3, 3, 4, 6, 7, 8, 9]  # remaining: 8
    [T, T, T, T, T, F, F, F]  # <7?
    [T, T, T, T, T, T, F, F]  # <=7?
    [            6, 7, 8, 9]  # remaining: 4
    [            6, 7      ]  # remaining: 2
    [               7      ]  # remaining: 1

# N/2^k == 1 -> done, k = log_2(N)
# log_2(1 million) ~ 20

if __name__ == '__main__':
    test_bisections()
    main()
    from bisect import bisect_left, bisect_right

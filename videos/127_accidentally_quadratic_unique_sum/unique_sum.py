import random
import time


def list_in(lst, x):
    for y in lst:
        if y == x:
            return True
    return False


def set_in(set_mem, x):
    idx = hash(x) % len(set_mem)
    link = set_mem[idx]
    while link is not None:
        if link.value == x:
            return True
        link = link.next
    return False


def unique_sum_list(nums):
    total = 0
    seen = []
    for n in nums:
        if n in seen:
            continue
        total += n
        seen.append(n)
    return total


def unique_sum_tuple(nums):
    total = 0
    seen = ()
    for n in nums:
        if n in seen:
            continue
        total += n
        seen = (*seen, n)
    return total


def unique_sum_set(nums):
    total = 0
    seen = set()
    for n in nums:
        if n in seen:
            continue
        total += n
        seen.add(n)
    return total


def unique_sum_dict(nums):
    total = 0
    seen = {}
    for n in nums:
        if n in seen:
            continue
        total += n
        seen[n] = None
    return total


def unique_sum_set_faster(nums):
    return sum(set(nums))


def unique_sum_dict_faster(nums):
    return sum(dict.fromkeys(nums))


def main():
    n = 1000
    nums = [random.randint(0, 2 << 32) for _ in range(n)]
    for unique_sum in [
        unique_sum_tuple,
        unique_sum_list,
        unique_sum_set,
        unique_sum_dict,
    ]:
        start = time.perf_counter()
        total = unique_sum(nums)
        elapsed = time.perf_counter() - start
        print(f"{unique_sum.__name__}: {elapsed * 1000:.2f}")


if __name__ == '__main__':
    main()

    #
    # for unique_sum in [
    #     unique_sum_tuple,  # .9s, 93 s
    #     unique_sum_list,  # .4s, 43 s
    #     unique_sum_set,  # 1 ms, 15 ms
    #     unique_sum_set_faster,  # 0.6 ms, 13 ms
    #     unique_sum_dict,  # 1ms, 21 ms
    #     unique_sum_dict_faster,  # .6ms,  16 ms
    # ]:

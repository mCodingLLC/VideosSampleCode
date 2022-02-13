import sys


def capacity(l: list):
    return (sys.getsizeof(l) - 56) // 8


def capacity_of_some_lists():
    x = []
    for i in range(100):
        x.append(i)
        print(f'{len(x)=}, {capacity(x)=}')


def compute_overallocation_ratios():
    x = [0]
    last_capacity = 1
    for _ in range(100000):
        x.append(0)
        new_capacity = capacity(x)
        if new_capacity != last_capacity:
            print(f'ratio={new_capacity / last_capacity:.3f}')
            last_capacity = new_capacity

    print(f'approaching {9/8=}')


def basic_compare_lists():
    x = [0, 0, 0]
    n = len(x)
    y = [0] * n
    z = [0 for _ in range(n)]

    x[:] = y[:] = z[:] = range(1000)
    x[:] = y[:] = z[:] = range(499)

    print(capacity(x))
    print(capacity(y))
    print(capacity(z))


def list_internal_structure():
    # Garbage collection info (before object)
    _gc_next = ...  # 8 bytes
    _gc_prev = ...  # 8 bytes

    # PyObject info
    ob_refcnt = ...  # 8 bytes
    ob_type = ...  # 8 bytes

    # PyVarObject info
    ob_size = ...  # 8 bytes

    # PyListObject info
    ob_item = ...  # 8 bytes
    allocated = ...  # 8 bytes


def getsizeof_list():
    n = 56  # 7 fields * 8 bytes = 56 bytes
    n += 8 * allocated


def sizeof_some_lists():
    print(sys.getsizeof([]))


def main():
    basic_compare_lists()
    # sizeof_some_lists()
    # capacity_of_some_lists()
    # compute_overallocation_ratios()


if __name__ == '__main__':
    main()

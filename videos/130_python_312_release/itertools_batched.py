import itertools


def print_batches():
    data = [1, 2, 3, 4, 5, 6, 7, 8]
    for batch in itertools.batched(data, 3):
        print(batch)
    # (1, 2, 3)
    # (4, 5, 6)
    # (7, 8)

def main():
    print_batches()

if __name__ == '__main__':
    main()

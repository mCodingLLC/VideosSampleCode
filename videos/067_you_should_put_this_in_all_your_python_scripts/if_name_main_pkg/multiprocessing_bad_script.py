import multiprocessing as mp


def useful_function(x):
    return x * x


if __name__ == '__main__':
    print("processing in parallel")
    with mp.Pool() as p:
        results = p.map(useful_function, [1, 2, 3, 4])
        print(results)

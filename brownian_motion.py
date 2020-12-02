import matplotlib.pyplot as plt
import numpy as np


def quadratic_variation(B):
    return np.cumsum(np.power(np.diff(B, axis=0, prepend=0.), 2), axis=0)


def main():
    n = 10000
    d = 10
    T = 1.
    times = np.linspace(0., T, n)
    dt = times[1] - times[0]
    # Bt2 - Bt1 ~ Normal with mean 0 and variance t2-t1
    dB = np.sqrt(dt) * np.random.normal(size=(n - 1, d))
    B0 = np.zeros(shape=(1, d))
    B = np.concatenate((B0, np.cumsum(dB, axis=0)), axis=0)
    plt.plot(times, B)
    # plt.plot(times, quadratic_variation(B))
    plt.show()


if __name__ == '__main__':
    main()

import matplotlib.pyplot as plt
import numpy as np


def s(n):
    return n * (n - 1) // 2

def sum_range_examples():
    n = 5
    print(sum(range(n)))
    print(s(n))


def correct_s(n):
    return n * (n - 1) // 2


def plot_parabola():
    y = np.linspace(0., 2022, 2023)
    x = y * y

    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6)

    ax.plot(y, x)
    ax.set_xlabel("y")
    ax.set_ylabel("x")

    plt.show()
    plt.close()


def plot_circles():
    t = np.linspace(0., 2 * np.pi, 100)
    r = 10.
    sqrt_r = np.sqrt(r)

    fig: plt.Figure
    ax: plt.Axes
    fig, ax = plt.subplots()
    fig.set_size_inches(6, 6)

    x1, y1 = r * np.cos(t), r * np.sin(t)
    x2, y2 = sqrt_r * np.cos(t), sqrt_r * np.sin(t)
    x3, y3 = ((r - sqrt_r) / 2 * np.cos(t) + (sqrt_r + r) / 2,
              (r - sqrt_r) / 2 * np.sin(t))

    ax.hlines(0., 0., r, color="black")
    ax.vlines([0., sqrt_r, r], -r, 0,
              color="lightgray", linestyles="--")
    ax.set_aspect(1.)
    ax.set_xticks([0., sqrt_r, r])
    ax.set_xticklabels([0., r"$\sqrt{R}$", r"$R$"])

    ax.plot(x1, y1, label="water")
    ax.plot(x2, y2, label="your island")
    ax.plot(x3, y3, label="sharks")

    ax.set_yticks([])
    fig.legend()

    plt.show()
    plt.close()


def main():
    sum_range_examples()
    plot_parabola()
    plot_circles()


if __name__ == '__main__':
    main()

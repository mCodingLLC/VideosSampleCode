import timeit

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    N = 100000
    int_to_str = []
    test_nums = range(5000, N, 100)
    for n in test_nums:
        print(n)
        t = timeit.timeit("str(x)", f"x=10 ** {n}", globals=globals(), number=1)
        int_to_str.append((n, t))

    str_to_int = []
    for n in test_nums:
        print(n)
        t = timeit.timeit("int(s)", f"s='1'+ '0' * {n}", globals=globals(), number=1)
        str_to_int.append((n, t))

    int_to_str = pd.DataFrame.from_records(int_to_str, columns=["n", "t"])
    str_to_int = pd.DataFrame.from_records(str_to_int, columns=["n", "t"])

    linewidth = 3.0
    plt.figure(figsize=(16, 9))
    plt.title("str/int conversion times")
    plt.xlabel("$n$ digits")
    plt.ylabel("$t$ time")
    plt.plot(int_to_str["n"], int_to_str["t"], label="int to str", color="tab:blue", linewidth=linewidth)
    plt.plot(str_to_int["n"], str_to_int["t"], label="str to int", color="tab:orange", linewidth=linewidth)
    plt.legend()
    plt.show()

    plt.figure(figsize=(16, 9))
    plt.title("log-log str/int conversion times")
    plt.xlabel(r"$\log(n)$ digits")
    plt.ylabel(r"$\log(t)$ time")
    int_to_str.loc[:, "log_t"] = np.log(int_to_str["t"])
    int_to_str.loc[:, "log_n"] = np.log(int_to_str["n"])
    str_to_int.loc[:, "log_t"] = np.log(str_to_int["t"])
    str_to_int.loc[:, "log_n"] = np.log(str_to_int["n"])
    polyfit_log_int_to_str = np.poly1d(np.polyfit(int_to_str["log_n"], int_to_str["log_t"], deg=1))
    polyfit_log_str_to_int = np.poly1d(np.polyfit(str_to_int["log_n"], str_to_int["log_t"], deg=1))

    plt.plot(int_to_str["log_n"], int_to_str["log_t"], label="int to str", color="tab:blue", linewidth=linewidth)
    plt.plot(int_to_str["log_n"], polyfit_log_int_to_str(int_to_str["log_n"]), color="black", linestyle="dashed",
             label=f"$\\log t = {polyfit_log_int_to_str.c[0]:+.2f}\\,\\log n {polyfit_log_int_to_str.c[1]:+.2f}$")

    plt.plot(str_to_int["log_n"], str_to_int["log_t"], label="str to int", color="tab:orange", linewidth=linewidth)
    plt.plot(str_to_int["log_n"], polyfit_log_str_to_int(str_to_int["log_n"]), color="black", linestyle="dashed",
             label=f"$\\log t = {polyfit_log_str_to_int.c[0]:+.2f}\\,\\log n {polyfit_log_str_to_int.c[1]:+.2f}$")

    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()

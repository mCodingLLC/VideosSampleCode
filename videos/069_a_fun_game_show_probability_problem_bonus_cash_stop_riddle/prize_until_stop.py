import math
import random
import matplotlib.pyplot as plt
import itertools


def expected_winnings(amounts, stop_tok) -> float:
    return sum(x for x in amounts if x != stop_tok) / (amounts.count(stop_tok) + 1)


def print_all_permutations_and_winnings(amounts, stop_tok):
    s = 0
    for order in itertools.permutations(amounts):
        win = amount_won(order, stop_tok)
        print(f'{order}: {win}')
        s += win
    count = math.factorial(len(amounts))
    print(f'total: {s}')
    print(f'count: {count}')
    print(f'average: {s / count}')


def amount_won(order, stop_tok) -> float:
    first_stop_idx = order.index(stop_tok)
    return sum(order[:first_stop_idx])


def sim(amounts, stop_tok) -> float:
    order = random.sample(amounts, k=len(amounts))
    return amount_won(order, stop_tok)


def run_sim(amounts, stop_tok, trials):
    s = 0
    averages = []

    for trial_number in range(1, trials + 1):
        win = sim(amounts, stop_tok)
        s += win
        averages.append(s / trial_number)

    expected = expected_winnings(amounts, stop_tok)
    print(f'{averages[-1]=}')
    print('expected:', expected)
    plt.plot(averages)
    plt.axhline(expected, color="black", linestyle="dashed")
    plt.show()


def main():
    amounts = [10, 1000, 1000, 10000, "s"]
    stop_tok = "s"
    trials = 1000

    run_sim(amounts, stop_tok, trials)


if __name__ == '__main__':
    main()

from if_name_main_pkg.bad_script import *


def compute_val():
    l = [0, 1, 2, 3, 4, 5]

    sum = 0
    for n in range(10):
        sum += useful_function(l[(7 * i + 6) % len(l)])
    return sum


def main():
    val = compute_val()
    print(f'{val=}')


if __name__ == '__main__':
    main()

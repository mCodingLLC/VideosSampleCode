from if_name_main_pkg.bad_script import UsefulClass

import pickle


def main():
    with open('test.pickle', 'wb') as f:
        x = UsefulClass(0)
        pickle.dump(x, f)


if __name__ == '__main__':
    main()

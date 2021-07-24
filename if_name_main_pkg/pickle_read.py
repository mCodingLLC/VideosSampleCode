import pickle


def main():
    with open('test.pickle', 'rb') as f:
        x = pickle.load(f)
        print(f'{x!r}')


if __name__ == '__main__':
    main()

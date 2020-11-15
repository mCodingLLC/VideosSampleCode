import random

if __name__ == '__main__':
    while True:
        print(random.randbytes(80).decode(errors='ignore'), end='')

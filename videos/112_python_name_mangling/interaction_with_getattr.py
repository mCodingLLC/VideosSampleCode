class A:
    def __init__(self):
        self.__x = 0
        print(getattr(self, "__x"))
        setattr(self, "__x", 42)
        print(self.__x)


def main():
    a = A()


if __name__ == '__main__':
    main()

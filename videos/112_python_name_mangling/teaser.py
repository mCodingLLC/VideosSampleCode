class A:
    __count = 0

    def get_count(self):
        return self.__count

    def set_count(self, count):
        self.__count = count


def main():
    a = A()
    print(a.get_count())

    A.__count = 21
    print(a.get_count())
    print(A.__count)

    a.__count = 42
    print(a.get_count())

    print(a.__dict__)

    a.set_count(100)
    print(a.get_count())
    print(a.__dict__)


if __name__ == '__main__':
    main()

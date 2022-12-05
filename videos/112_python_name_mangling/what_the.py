def get_count(self):
    return self.__count


class A:
    __count = 0

    # def get_count(self):
    #     return self.__count

    get_count = get_count


def main():
    a = A()
    A.__count = 21
    print(a.get_count())


if __name__ == '__main__':
    main()

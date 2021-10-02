class VerboseMeta(type):

    def __new__(mcs, name, bases, namespace, print_f, **kwargs):
        print('VerboseMeta new', mcs, name, bases, namespace, print_f, kwargs)
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class A(metaclass=VerboseMeta, print_f=print):
    pass


def main():
    pass


if __name__ == '__main__':
    main()

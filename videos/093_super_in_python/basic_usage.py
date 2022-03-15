class Base:
    def f(self, x):
        print("Base.f", self, x)


class Derived(Base):
    def f(self, x):
        print("Derived.f", self, x)
        super().f(x)
        print("Derived.f finished")


def basic_example():
    d = Derived()
    d.f(42)


class LoggingDict(dict):
    def __setitem__(self, key, value):
        print(f'Setting {key}: {value}')
        super().__setitem__(key, value)

    def __getitem__(self, item):
        print(f'Getting {item}')
        return super().__getitem__(item)

    def __delitem__(self, key):
        print(f'Deleting {key}')
        super().__delitem__(key)


def logging_dict_example():
    print("LOGGING DICT EXAMPLE")
    d = LoggingDict()
    d[0] = "subscribe"
    x = d[0]
    del d[0]
    print()


def main():
    # basic_example()
    logging_dict_example()


if __name__ == '__main__':
    main()

def abstractmethod(f):
    f.__isabstract__ = True
    return f


def abstractmethods(cls):
    seen = set()
    abstract = []
    while isinstance(cls, ABCMeta):
        for key, val in vars(cls).items():
            if key in seen:
                continue
            seen.add(key)
            if getattr(val, '__isabstract__', False):
                abstract.append(key)
        # object is not ABCMeta so mro will have at least 2 entries
        cls = cls.__mro__[1]
    return abstract


class ABCMeta(type):
    def __call__(abccls, *args, **kwargs): # called when you A()
        print("call", abccls, args, kwargs)
        abstract = abstractmethods(abccls)
        if abstract:
            raise TypeError('no implementation for: ' + ', '.join(abstract))
        return super().__call__(*args, **kwargs)


class ABC(metaclass=ABCMeta):
    pass


class A(ABC):
    def __init__(self, *args, **kwargs):
        print("init", self, args, kwargs)

    @abstractmethod
    def f(self):
        pass

    @abstractmethod
    def g(self):
        pass


class B(A):
    def f(self):
        pass

    def g(self):
        pass


def main():
    # A()  # Error: abstract f,g
    b = B()
    print(f'{type(b)=}')
    print(f'{type(B)=}')


if __name__ == '__main__':
    main()

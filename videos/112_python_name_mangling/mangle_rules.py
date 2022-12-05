class A:
    def __init__(self, b):
        self.__x = 0  # -> _A__x
        self.__len__ = ...  # NOT MANGLED
        self.__ = ...  # NOT MANGLED
        __y = 0  # -> _A__y local
        import __abc  # imports _A__abc
        import __abc.a  # imports __abc.a

        b.__x = 0  # sets _A__x


class _:
    def __init__(self, b):
        self.__x = 0  # -> # NOT MANGLED
        self.__len__ = ...  # NOT MANGLED
        self.__ = ...  # NOT MANGLED
        __y = 0  # -> # NOT MANGLED
        import __abc  # # NOT MANGLED
        import __abc.a  # # NOT MANGLED

        b.__x = 0  # # NOT MANGLED


if __name__ == '__main__':
    main()

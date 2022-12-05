class A:
    __public_magic__ = "something"

    def __init__(self):
        self._dont_touch_me = "subscribe"
        self.__attr__ = "something"
        self._A__var = "manually mangled"

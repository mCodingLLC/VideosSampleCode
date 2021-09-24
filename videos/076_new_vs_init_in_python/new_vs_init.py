import codecs
import itertools
from abc import ABC, abstractmethod


class A:
    def __new__(cls, *args, **kwargs):
        print('new', cls, args, kwargs)
        return super().__new__(cls)

    def __init__(self, *args, **kwargs):
        print('init', self, args, kwargs)


def how_object_construction_works():
    x = A(1, 2, 3, x=4)

    # above is equivalent to below, but this can be customized using metaclasses

    x = A.__new__(A, 1, 2, 3, x=4)
    if isinstance(x, A):
        type(x).__init__(x, 1, 2, 3, x=4)
    print(x)


class UppercaseTuple(tuple):
    def __new__(cls, iterable):
        upper_iterable = (s.upper() for s in iterable)
        return super().__new__(cls, upper_iterable)

    # Error: tuples are immutable, even in init
    # def __init__(self, iterable):
    #     print(f'init {iterable}')
    #     for i, arg in enumerate(iterable):
    #         self[i] = arg.upper()


def inheriting_immutable_uppercase_tuple_example():
    print("UPPERCASE TUPLE EXAMPLE")
    print(UppercaseTuple(["hi", "there"]))


class Singleton:  # eg global config object, I discourage actually using this pattern
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


def singleton_example():
    print("SINGLETON EXAMPLE")
    x = Singleton()
    y = Singleton()
    print(f'{x is y=}')


class Client:
    _loaded = {}
    _db_file = "file.db"

    def __new__(cls, client_id):
        if (client := cls._loaded.get(client_id)) is not None:
            print(f'returning existing client {client_id} from cache')
            return client
        client = super().__new__(cls)
        cls._loaded[client_id] = client
        client._init_from_file(client_id, cls._db_file)
        return client

    def _init_from_file(self, client_id, file):
        # lookup client in file and read properties
        print(f'reading client {client_id} data from file, db, etc.')
        name = ...
        email = ...
        self.name = name
        self.email = email
        self.id = client_id


def cached_clients_example():
    print("CLIENT CACHE EXAMPLE")
    x = Client(0)
    y = Client(0)
    print(f'{x is y=}')
    z = Client(1)


class EncryptedFile:  # DO NOT USE ANY OF THESE FOR REAL ENCRYPTION
    _registry = {}  # 'rot13' -> ROT13Text

    def __init_subclass__(cls, prefix, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._registry[prefix] = cls

    def __new__(cls, path: str, key=None):
        prefix, sep, suffix = path.partition(':///')
        if sep:
            file = suffix
        else:
            file = prefix
            prefix = "file"
        subclass = cls._registry[prefix]
        obj = object.__new__(subclass)
        obj.file = file
        obj.key = key
        return obj

    def read(self) -> str:
        raise NotImplementedError


class Plaintext(EncryptedFile, prefix='file'):
    def read(self):
        with open(self.file, 'r') as f:
            return f.read()


class ROT13Text(EncryptedFile, prefix='rot13'):
    def read(self):
        with open(self.file, 'r') as f:
            text = f.read()
        return codecs.decode(text, 'rot_13')


class OneTimePadXorText(EncryptedFile, prefix='otp'):
    def __init__(self, path, key):
        if isinstance(self.key, str):
            self.key = self.key.encode()

    def xor_bytes_with_key(self, b: bytes) -> bytes:
        return bytes(b1 ^ b2 for b1, b2 in zip(b, itertools.cycle(self.key)))

    def read(self):
        with open(self.file, 'rb') as f:
            btext = f.read()
        text = self.xor_bytes_with_key(btext).decode()
        return text


def encrypted_file_example():
    print("ENCRYPTED FILE EXAMPLE")
    print(EncryptedFile('plaintext_hello.txt').read())
    print(EncryptedFile('rot13:///rot13_hello.txt').read())
    print(EncryptedFile('otp:///otp_hello.txt', key='1234').read())


class Drawable(ABC):

    @abstractmethod  # marks draw with __isabstractmethod__ = True
    def draw(self):
        return NotImplemented


def main():
    how_object_construction_works()
    inheriting_immutable_uppercase_tuple_example()
    singleton_example()
    cached_clients_example()
    encrypted_file_example()


if __name__ == '__main__':
    main()

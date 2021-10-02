import time


class LoadTimeMeta(type):
    base_time = time.perf_counter()

    def __new__(mcs, name, bases, namespace):
        print(mcs, name, bases, namespace)
        namespace['__class_load_time__'] = time.perf_counter() - LoadTimeMeta.base_time
        return super().__new__(mcs, name, bases, namespace)


class A(metaclass=LoadTimeMeta):
    pass

class B(A):
    pass

def main():
    print(f'{A.__class_load_time__=} after base time')
    print(f'{B.__class_load_time__=} after base time')
    print(f'{type(B)=}')


if __name__ == '__main__':
    main()

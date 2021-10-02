def _make_init(annotations):
    lines = [
        'def __init__(self, {}):'.format(
            ', '.join(f'{arg}: {annot.__qualname__}'
                      for arg, annot in annotations.items())),
    ]

    for arg, annot in annotations.items():
        lines += [
            f'   self.{arg} = {arg}',
        ]

    init_code = '\n'.join(lines)
    return init_code


class DataClassMeta(type):
    def __new__(mcs, name, bases, namespace, **kwargs):
        annotations = namespace.get('__annotations__')
        if annotations:
            init_code = _make_init(annotations)
            exec(init_code, globals(), namespace)
        return super().__new__(mcs, name, bases, namespace, **kwargs)


class DataClass(metaclass=DataClassMeta):
    pass


class MyFields(DataClass):
    x: int
    y: str


def main():
    print(MyFields.__annotations__)
    print(_make_init({'x': int, 'y': str}))
    # print(help(MyFields))
    m = MyFields(2, 3)


if __name__ == '__main__':
    main()

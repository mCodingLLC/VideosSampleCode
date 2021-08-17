import datetime

""" f-strings """


def equals_debugging():
    str_value = "other 🐶"
    num_value = 123
    print(f'the value is {str_value}')
    print(f'{num_value = }')
    print(f'{num_value % 2 = }')


def conversions():
    str_value = "other 🐶"
    print(f'{str_value!s}')
    print(f'{str_value!r}')


class MyClass:
    def __format__(self, format_spec) -> str:
        print(f'MyClass __format__ called with {format_spec=!r}')
        return "MyClass()"


def formatting():
    num_value = 123.456
    now = datetime.datetime.utcnow()
    print(f'{now=:%Y-%m-%d}')
    print(f'{num_value:.2f}')
    print(f'{MyClass():blah blah %%MYFORMAT%%}')

    nested_format = ".2f"
    print(f'{num_value:{nested_format}}')


def main():
    # equals_debugging()
    # conversions()
    formatting()


if __name__ == '__main__':
    main()

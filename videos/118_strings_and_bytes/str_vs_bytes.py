def converting_between_str_bytes():
    s = "abc"
    b = s.encode("utf-8")
    print(s)
    print(b)

    b = b"abc"
    s = b.decode("utf-8")
    print(s)
    print(b)


def str_bytes_syntax():
    s = "Hello from str"
    b = b"Hello from bytes"
    print(s)
    print(b)

    s = 'Hello from str'
    b = b'Hello from bytes'
    print(s)
    print(b)

    s = """Hello from str"""
    b = b'''Hello from bytes'''
    print(s)
    print(b)

    s = "Hello from str\n"
    b = b"Hello from bytes\n"
    print(s)
    print(b)

    s = r"Hello from str\n"
    b = rb"Hello from bytes\n"
    print(s)
    print(b)

    s = f"Hello from str in {__name__}"
    # b = fb"Hello from bytes in {__name__}" # Error
    print(s)


def str_bytes_functions():
    str_functions = set(dir(str))
    bytes_functions = set(dir(bytes))
    print("str and bytes common functions")
    for func in sorted(str_functions & bytes_functions):
        print(func)
    print()

    print("str but not bytes functions")
    for func in sorted(str_functions - bytes_functions):
        print(func)
    print()

    print("bytes but not str functions")
    for func in sorted(bytes_functions - str_functions):
        print(func)
    print()


def writing_to_a_file():
    with open("file.txt", "w") as fp:
        fp.write("some str")
        # fp.write(b"some bytes") # Error
        fp.write(b"some bytes".decode())  # OK

    with open("file.txt", "wb") as fp:
        # fp.write("some str") # Error
        fp.write("some str".encode())  # OK
        fp.write(b"some bytes")


def smiley():
    s = "😊"
    s = "\U0001F60A"
    # b = b"😊"
    b = s.encode("utf-8")
    print(b)
    print(f"{len(s)=}")
    print(f"{len(b)=}")
    print(list(b))
    print(int.from_bytes(b, byteorder="little"))
    print(int.from_bytes(b, byteorder="big"))
    print(b.decode("utf-8"))


def example_encode_decode_wrong_encoding():
    # on computer with utf-8 encoding
    s = "Hello, world! 😊"

    with open("data.txt", "w", encoding="utf-8") as fp:
        fp.write(s)

    # OK
    with open("data.txt", encoding="utf-8") as fp:
        print(fp.read())

    # Garbage on the end
    with open("data.txt", encoding="iso-8859-1") as fp:
        print(fp.read())

    # Error!
    # with open("data.txt", encoding="Windows-1251") as fp:
    #     print(fp.read())

    # Note: utf-8 is scheduled to become the default in Python 3.15
    # https://peps.python.org/pep-0686/

    # Note: in Python 3.10+ run with -X warn_default_encoding to get a warning
    # if you forget to specify encoding

    # Note: in Python 3.7+ run with -X utf8 to assume utf-8 if not specified


def main():
    # converting_between_str_bytes()
    # str_bytes_syntax()
    # str_bytes_functions()
    # smiley()
    example_encode_decode_wrong_encoding()


if __name__ == '__main__':
    main()

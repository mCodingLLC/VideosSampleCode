def do_something(options=None):
    if not options:
        options = {'option1': 1}
    print(options)


if __name__ == '__main__':
    x = (_ for _ in [])

    do_something(options={})

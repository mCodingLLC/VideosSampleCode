
def do_something(arg=None):
    arg = arg or []

if __name__ == '__main__':
    print(0 or [] or {})
    print(0 or 1 or 2)

    print(1 and 2 and 3)
    print(1 and 0 and [])
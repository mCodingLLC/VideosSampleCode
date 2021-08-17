from dataclasses import dataclass
import timeit

# Requires Python 3.10

def match_case_reserved_softkws():
    match = 6
    case = "case"

    match 6:
        case 6:
            print("6")
    print("no problem")

    # don't do this
    match case:
        case match:
            print(f'{match=} {case=}')

def underscore_is_a_wildcard():
    x = "case x binds x"
    match 0:
        case x:
            print("x bound")
    print(f'{x=}')

    _ = "case _ is a wildcard, not a var name"
    match 0:
        case _:
            print("wildcard")
    print(f'{_=}')

def name_binding_scope():
    match 1, 2:
        case 1, x:
            pass
    print(f'{x=}')

    x = 0
    match 0, 1, 2:
        case 0, x, 1:
            pass
        case 0, y, 2:
            pass

    print(f'{y=} is well-defied')
    print(f'{x=} is undefined/implementation dependent behavior')

def name_binding_already_bound():
    x = 0
    match 1:
        case 2:
            print('case 2')
        case x:
            print(f'You didnt match against 0, you just bound x!, {x=}')


def name_binding_dynamic():
    class dummy:
        x = sum(i**2 for i in range(5))

    y = sum(i**2 for i in range(5))
    match y:
        case dummy.x:
            print(f'{y=} {dummy.x=}')


def class_matching_getattr():
    class Person:
        __match_args__ = ("names",)
        def __init__(self, fullname):
            self.names = fullname.split(" ")

        @property
        def first_name(self):
            return self.names[0]

    p1 = Person(fullname="James Murphy")
    match p1:
        case Person(fullname="James Murphy"):
            print("wrong! not a constructor")
        case Person(names=["James", "Murphy"]):
            print("found me!")
        case Person(["James", "Murphy"]):
            print("same as previous due to match args!")
        case Person(first_name="James"):
            print("found me again!")


def timing_match():
    errno = 42
    match errno:
        case 0:
            pass
        case 1:
            pass
        case 42:
            pass
        case _:
            pass


def timing_match_old():
    errno = 42
    if errno == 0:
        pass
    elif errno == 1:
        pass
    elif errno == 42:
        pass
    else:
        pass

@dataclass
class Click:
    position: tuple[int, int]
    button: str

@dataclass
class KeyPress:
    key_name: str

@dataclass
class Quit:
    pass


def timing_match_by_class_old():
    event = "unknown"
    if isinstance(event, Click) and event.button == "left":
        x,y = event.position
    elif isinstance(event, Click):
        x,y = event.position
    elif isinstance(event, KeyPress) and event.key_name in ["Q","q"] \
            or isinstance(event, Quit):
        pass
    elif isinstance(event, KeyPress) and event.key_name == "up arrow":
        pass
    elif isinstance(event, KeyPress):
        pass
    else:
        pass

def timing_match_by_class():
    event = "unknown"
    match event:
        case Click(position=(x,y), button="left"):
            pass
        case Click(position=(x,y)):
            pass
        case KeyPress("Q"|"q") | Quit():
            pass
        case KeyPress(key_name="up arrow"):
            pass
        case KeyPress():
            pass #ignore other keystrokes
        case other_event:
            pass


def main():
    match_case_reserved_softkws()
    underscore_is_a_wildcard()
    name_binding_scope()
    name_binding_already_bound()
    name_binding_dynamic()
    class_matching_getattr()

if __name__ == '__main__':
    main()
    print(timeit.timeit(timing_match_old))
    print(timeit.timeit(timing_match))
    print(timeit.timeit(timing_match_by_class_old))
    print(timeit.timeit(timing_match_by_class))
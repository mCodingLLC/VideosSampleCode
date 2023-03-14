import collections
import dataclasses
import gzip
import io
import json
import math
import pathlib
import re
import typing
from html.parser import HTMLParser

import numpy as np


# 1
def manually_rounding_in_print():
    t = 1.23456
    print(f"Finished in {t}s")
    print(f"Finished in {round(t, 2)}s")
    print(f"Finished in {t:.2f}s")

# 2
def repeatedly_converting_to_from_numpy_arrays():
    nums = list(range(256 * 256 * 256))
    arr = np.array(nums)  # 1.01s

    m = max(nums)  # .16s
    m = np.max(arr)  # .01s
    m = arr.max()  # .01s
    m = max(arr)  # .73s

# 3
def manipulating_paths_as_strings():
    path = "path/to/data/my_data.json"
    zipped_file = path.removesuffix(".json") + ".zip"
    data_dir = "/".join(path.split("/")[-2])
    other_file = f"{data_dir}/other_file.txt"
    deeper_dir = f"{data_dir}/abc/def"

    path = pathlib.Path("path/to/data/my_data.json")
    zipped_file = path.with_suffix(".zip")
    data_dir = path.parent
    other_file = path.with_name("other_file.txt")
    deeper_dir = data_dir.joinpath("abc", "def")

    # also os.path but pathlib is preferred

# 4
def do_io_taking_path(path: str):
    with open(path, "w") as fp:
        fp.write("...")
        # do_io_taking_io(fp)


def do_io_taking_io(fp: typing.TextIO):
    fp.write("...")


def calls_do_io_with_gzip_io():
    with gzip.open("example.txt.gz", "wt") as fp:
        do_io_taking_io(fp)

    with gzip.open("example.txt.gz", "rt") as fp:
        assert fp.read() == "..."

# 5
def concatenating_strings_with_plus():
    s = ""
    for i in range(100):
        s += f"some string {i}"

    ss = io.StringIO()
    for i in range(100):
        ss.write(f"some string {i}")
    s = ss.getvalue()

    lines = []
    for i in range(100):
        lines.append(f"some string {i}")
    s = "\n".join(lines)

    return s

# 6
def using_eval_as_a_parser():
    data_str = '{"a":1, "b":2, "c":3}'
    data = eval(data_str)
    data = json.loads(data_str)
    with open("file_that_data_str_came_from.txt") as fp:
        data = json.load(fp)
    print(data)
    # pydantic...



# 7
strict = True


def storing_inputs_and_or_outputs_as_globals():
    for i in range(100):
        if strict:
            ...
        else:
            ...

    global ans
    ans = ...

# SELF PROMO

# 8
def thinking_and_or_return_bools():
    a = {"a": 1, "b": 2, "c": 3}
    b = [1, 2, 3]
    print(a or b)  # {"a": 1, "b": 2, "c": 3}
    print(a and b)  # [1, 2, 3]
    print({} or [])  # []
    print({} and [])  # {}

    # or: first true one or last false one
    # and: first false one or last true one

    cond = a or b
    if cond == True:
        print("cond is true")
    elif cond:
        print("cond is truthy")
    else:
        print("cond is falsey")

# 9
def single_letter_variables():
    for i in range(100):  # OK
        ...

    for idx in range(100):  # easier to ctrl+f for idx
        ...

    _ = "unused OK"

    x, y, z = (1, 2, 3)  # OK

    a0, r, t = 1.0, .01, 1.0
    a = a0 * math.exp(r * t)

    # Please use names
    p = "data.txt"
    with open(p) as f:
        for l in f:
            s = l.split()
            t, u = s[0], s[-1]
            ti, ui = int(t), int(u)
            d = ui - ti
            ...

    # with open(p) as fp:
    #     for line in fp:
    #         tokens = line.split()
    #         first_token, last_token = tokens[0], tokens[-1]
    #         first_int, last_int = int(first_token), int(last_token)
    #         diff = last_int - first_int
    #         ...

# 10
def using_div_and_mod_instead_of_divmod(x, p):
    q, r = x // p, x % p
    q, r = divmod(x, p)
    if r == 0:
        print(f"{p} divides {x} evenly into {q} parts")
    else:
        print(f"{p} divides {x} into {q} parts with a remainder of {r}")

# 11
class JavaLike:
    def __init__(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_x(self, x):
        # ...
        self._x = x

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, val):
        self._x = val


def not_knowing_about_properties():
    obj = JavaLike(0)

    obj.set_x(42)
    print(obj.get_x())

    obj.x = 42
    print(obj.x)

# 12
class Thingy:

    @property
    def val(self):
        # long computation
        ...
        return 42


def expensive_properties():
    thing = Thingy()

    val = thing.val  # if val is property, looks CHEAP

    val = thing.val()  # if val is function, looks maybe expensive


# 13
def inserting_or_deleting_while_iterating():
    # d = {chr(65+i): i for i in range(10)}
    # for key, val in d.items():
    #     if val % 2 == 0:
    #         del d[key]
    #         # d[key] = 42

    d = {chr(65 + i): i for i in range(10)}
    for key, val in list(d.items()):
        if val % 2 == 0:
            del d[key]
    print(d)

    d = {chr(65 + i): i for i in range(10)}
    to_delete = set()
    for key, val in d.items():
        if val % 2 == 0:
            to_delete.add(key)

    for key in to_delete:
        del d[key]
    print(d)


# 14
def using_filter_and_map_instead_of_comprehensions():
    xs = list(range(10))
    odds = filter(lambda x: x % 2 == 1, xs)
    squares = map(lambda x: x * x, xs)

    odds = (x for x in xs if x % 2 == 1)
    squares = (x * x for x in xs)

    def func(x):
        ...

    filtered = filter(func, xs)
    filtered = (x for x in xs if func(x))

    mapped = map(func, xs)
    mapped = (func(x) for x in xs)

    filtered = list(filter(func, xs))
    filtered = [x for x in xs if func(x)]

    mapped = list(map(func, xs))
    mapped = [func(x) for x in xs]


# 15
def defining_too_many_dunders():
    class Person:
        def __init__(self, name: str, friends: set):
            self.name = name
            self.friends = friends

        def __hash__(self):  # fine
            return hash(self.name)

        def __iadd__(self, other): # why?
            self.friends.add(other)
            other.friends.add(self)
            return self

        def add_friend(self, other):
            self.friends.add(other)
            other.friends.add(self)

    p1 = Person("James", set())
    p2 = Person("Other James", set())

    p1 += p2  # friends!
    p1.add_friend(p2)


# 16
def trying_to_parse_html_or_xml_using_regex():
    html = """
    <html>
    <body>
    <a href="https://mcoding.io">Great website</a>
    </body>
    </html>
    """

    links_regex = '<a href="(.*?)"'
    for match in re.finditer(links_regex, html):
        print(f"Found link: {match.group(1)}")

    class UrlParser(HTMLParser):
        def handle_starttag(self, tag: str, attrs):
            if tag != "a":
                return

            for attr, val in attrs:
                if attr == "href":
                    print(f"Found link: {val}")
                    break

    UrlParser().feed(html)
    # or use BeautifulSoup...


# 17
def not_knowing_about_raw_strings():
    some_path = "windows\\path\\to\\file.txt"
    some_path = r"c:\path\to\file.txt"

    some_regex = "\\d+\\.\\d*"
    some_regex = r"\d+\.\d*"

    val = 42
    interpolated = fr"\\ {val} //"
    print(interpolated)

    # gotcha = r"can't end in backslash \" # SyntaxError
    print(gotcha)

# 18
def thinking_super_means_parent():
    class Root:
        def f(self):
            print("Root.f")

    class A(Root):
        def f(self):
            print("A.f")
            super().f()

    class B(Root):
        def f(self):
            print("B.f")
            super().f()

    class C(A, B):
        def f(self):
            print("C.f")
            super().f()

    C().f()
    # C.f
    # A.f
    # B.f
    # Root.f

    print([cls.__name__ for cls in C.__mro__]) # C, A, B, Root, object

# 19
@dataclasses.dataclass
class Measurement:
    value: float
    timestamp: float
    location: tuple[float, float]
    error_estimate: tuple[float, float]


class Measurement(typing.NamedTuple):
    value: float
    timestamp: float
    location: tuple[float, float]
    error_estimate: tuple[float, float]


class Measurement(typing.TypedDict):
    value: float
    timestamp: float
    location: tuple[float, float]
    error_estimate: tuple[float, float]


def passing_structured_data_as_dict_or_tuple():
    # take some measurement
    measurement = 1.0001
    timestamp = ...
    location = ...
    error_estimate = ...

    data = {
        "measurement": measurement,
        "timestamp": timestamp,
        "location": location,
        "error_estimate": error_estimate,
    }

    data = (measurement, timestamp, location, error_estimate)

    return data

# 20
def using_namedtuple_instead_of_NamedTuple():
    Point = collections.namedtuple("Point", ["x", "y", "z"])
    p = Point(1, 2, 3)
    print(p.x + p.y + p.z)

    class Point(typing.NamedTuple):
        x: float
        y: float
        z: float

    p = Point(1, 2, 3)
    print(p.x + p.y + p.z)


# 21. import time side effects

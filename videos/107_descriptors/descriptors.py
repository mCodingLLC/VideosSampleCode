import dataclasses
import functools

import sqlalchemy.orm
from pydantic import BaseModel

DESCRIPTOR_KEYS = {"__get__", "__set__", "__delete__"}


def descriptor_keys(obj):
    return DESCRIPTOR_KEYS & set(dir(obj))


def print_obj_and_descriptor_keys(obj):
    print(obj)
    keys = descriptor_keys(obj)
    if keys:
        print(f"IS a descriptor, found: {keys}")
    else:
        print(f"IS NOT a descriptor, found: {keys}")


class Descriptor:
    def __get__(self, obj, objtype=None):
        ...

    def __set__(self, obj, value):
        ...

    def __delete__(self, obj):
        ...


class SomeClass:
    x = Descriptor()


def what_are_descriptors():
    obj = SomeClass()

    print(obj.x)
    print(SomeClass.x)

    obj.x = 42
    del obj.x


# 1. functions

class A:
    def f(self):
        pass


def functions():
    print_obj_and_descriptor_keys(A.__dict__["f"])
    a = A()
    print(a.f)
    print(A.f)


# 2. properties

class Rect:
    def __init__(self, w, h):
        self.width = w
        self.height = h

    @property
    def area(self):
        return self.width * self.height

    @functools.cached_property
    def expensive_val(self):
        return ...  # some long computation


class Student:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name


def properties():
    print_obj_and_descriptor_keys(Rect.__dict__["area"])
    rect = Rect(2, 4)
    print(rect.area)

    student = Student("James")
    print(student.name)


class Property:
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.fget(obj)


# 3. class methods and static methods

class Animal:
    @classmethod
    def create(cls):
        return cls()

    @staticmethod
    def something_static():
        ...


def static_and_class_methods():
    print_obj_and_descriptor_keys(Animal.__dict__["create"])
    animal = Animal.create()
    other = animal.create()  # weird but ok


class ClassMethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        if objtype is None:
            objtype = type(obj)
        return self.f.__get__(objtype, objtype)


class StaticMethod:
    def __init__(self, f):
        self.f = f

    def __get__(self, obj, objtype=None):
        return self.f


# 4. slots

class Vec3:
    __slots__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def slotted_variables():
    print_obj_and_descriptor_keys(Vec3.__dict__["x"])
    v = Vec3(0.0, 0.0, 0.0)
    v.x = 1.0  # ok
    # v.w = 1.0  # AttributeError


# 5. __dict__

class E:
    pass


def dunder_dict():
    print_obj_and_descriptor_keys(E.__dict__["__dict__"])


# 6. SQLAlchemy Models

Base = sqlalchemy.orm.declarative_base()


class User(Base):
    __tablename__ = "user_account"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String)


def sqlalchemy_models():
    print_obj_and_descriptor_keys(User.__dict__["id"])
    print(User.__dict__["id"].__class__)
    sqlalchemy.orm.attributes.InstrumentedAttribute



# 6.1 Counterexample: Pydantic models

class Client(BaseModel):
    id: int
    name: str


def not_pydantic_models():
    print_obj_and_descriptor_keys(Client.__fields__["id"])


# 7. Validators

class GreaterThan:
    def __init__(self, val):
        self.val = val

    def __set_name__(self, owner, name):
        self.name = f'_{name}'

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not value > self.val:
            raise ValueError(f"value must be greater than {self.val}, but got: {value}")
        setattr(obj, self.name, value)


@dataclasses.dataclass
class Item:
    name: str
    price: float = GreaterThan(0.0)


def field_validation():
    apple = Item("Apple", 1.50)
    # apple = Item("Apple", -1.50)  # ValueError

    print_obj_and_descriptor_keys(Item.__dict__["price"])


# 8. super view lookups

def super_lookups():
    class Package:
        def ship(self, address):
            print("taking my time...")

    class ExpressPackage(Package):
        def ship(self, address):
            print("on the way!")

    base_view = super(ExpressPackage)
    ExpressPackage.base_view = base_view

    ExpressPackage().ship(...)
    ExpressPackage().base_view.ship(...)
    print_obj_and_descriptor_keys(ExpressPackage.__dict__["base_view"])


# What about getattr?

class NoisyDescriptor:
    def __get__(self, obj, objtype=None):
        print("get")

    def __set__(self, obj, value):
        print("set")

    def __delete__(self, obj):
        print("delete")


class MyClass:
    x = NoisyDescriptor()  # calls __set_name__(MyClass, 'x') after class definition

    def __getattribute__(self, item):  # always called
        print("getattribute")
        return object.__getattribute__(self, item)  # implements descriptor logic

    def __getattr__(self, item):  # called if __getattribute__ raises AttributeError
        print("getattr")

    def __setattr__(self, key, value):  # always called
        print("setattr")
        object.__setattr__(self, key, value)  # implements descriptor logic

    def __delattr__(self, item):  # always called
        print("delattr")
        object.__delattr__(self, item)  # implements descriptor logic


def what_about_getattr():
    m = MyClass()

    print(m.x)  # calls Descriptor.__get__(m, MyClass)
    print(MyClass.x)  # calls Descriptor.__get__(None, MyClass)

    m.x = 42  # calls Descriptor.__set__(m, 42)
    del m.x  # call Descriptor.__delete__(m)


# Data vs non-data descriptors

class DataDesc:
    def __get__(self, obj, objtype=None):
        ...

    def __set__(self, obj, value):  # and/or __delete__
        ...


class NonDataDesc:
    def __get__(self, obj, objtype=None):
        ...


class Gotcha:
    x = DataDesc()
    y = NonDataDesc()


def gotchas_data_vs_nondata_descriptors():
    g = Gotcha()
    print(g.x, g.y)  # None None
    g.__dict__["x"] = 42
    g.__dict__["y"] = 42
    print(g.x, g.y)  # None 42


def main():
    pass
    # functions()
    # static_and_class_methods()
    # slotted_variables()
    # properties()
    # dunder_dict()
    # sqlalchemy_models()
    # not_pydantic_models()
    # field_validation()
    # super_lookups()
    # what_are_descriptors()
    # gotchas_data_vs_nondata_descriptors()


if __name__ == '__main__':
    main()

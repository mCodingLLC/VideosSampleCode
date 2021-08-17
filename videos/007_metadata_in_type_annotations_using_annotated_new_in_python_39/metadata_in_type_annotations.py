from typing import Annotated, TypeVar, get_args
import struct2

UnsignedShort = Annotated[int, struct2.ctype('H')]
SignedChar = Annotated[int, struct2.ctype('b')]

assert get_args(UnsignedShort) == (int, struct2.ctype('H'))


class Student(struct2.Packed):
    name: Annotated[str, struct2.ctype("<10s")]
    serialnum: UnsignedShort
    school: SignedChar


record: bytes = ...

student = Student.unpack(record)
# Student(name=b'raymond   ', serialnum=4658, school=264)

record = student.pack()



T = TypeVar('T')
Const = Annotated[T, my_annotations.CONST]


class C:
    def const_method(self,l: Const[list[int]]) -> int:
        ...

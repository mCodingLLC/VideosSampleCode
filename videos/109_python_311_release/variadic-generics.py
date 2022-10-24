from typing import TypeVar
from typing import TypeVarTuple
from typing import Generic
from typing import NewType
from typing import Literal as L

DType = TypeVar("DType")
Shape = TypeVarTuple("Shape")


class Array(Generic[DType, *Shape]):
    ...


Height = NewType("Height", int)
Width = NewType("Width", int)
Channels = NewType("Channels", int)


def find_edges(image: Array[float, Height, Width, Channels]):
    ...


my_image = Array[float, L[1080], L[1920], L[3]]()

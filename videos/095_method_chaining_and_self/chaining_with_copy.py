from dataclasses import dataclass

import numpy as np


def builtin_str_example():
    s = "Wow, I love mCoding videos, I just subscribed!\n"

    t = s.strip().upper().center(50)
    print(t)


@dataclass(slots=True, frozen=True)
class Vector:
    x: float
    y: float
    z: float

    def normalized(self):
        x, y, z = self.x, self.y, self.z
        norm = np.sqrt(x * x + y * y + z * z)
        return type(self)(x / norm, y / norm, z / norm)

    def reflected(self):
        return type(self)(-self.x, -self.y, -self.z)


def main():
    p = Vector(1., 2., 3.)
    q = p.reflected().normalized()
    print(p)
    print(q)


if __name__ == '__main__':
    main()

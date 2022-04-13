import numpy as np


class Player:
    def __init__(self, name, position, fatigue=0):
        self.name = name
        self.position = position
        self.fatigue = fatigue

    def draw(self):
        print(f"drawing {self.name} to screen at {self.position}")
        return self

    def move(self, delta):
        self.position += delta
        self.fatigue += 1
        return self

    def rest(self):
        self.fatigue = 0
        return self


def main():
    james = Player("James", np.array([0.0, 0.0]))
    UP = np.array([0.0, 1.0])
    RIGHT = np.array([1.0, 0.0])

    (
        james.move(UP)
            .move(RIGHT)
            .move(UP)
            .rest()
            .draw()
    )


if __name__ == "__main__":
    main()

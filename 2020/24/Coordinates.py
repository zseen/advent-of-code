from typing import Any


class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: Any):
        if not isinstance(other, Coordinates):
            return NotImplemented

        return self.x == other.x and self.y == other.y

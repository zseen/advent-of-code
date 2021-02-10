from typing import List


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class SeaMonster:
    def __init__(self):
        self.coordinates: List[Coordinate] = []
        self.length: int = 0
        self.bodyPartsCount = 0

    def setCoordinates(self, rawInput: List[str]) -> None:
        coordinates = [Coordinate(i, j - 1) for j in range(0, len(rawInput)) for i in range(0, len(rawInput[j])) if rawInput[j][i] == "#"]
        self.coordinates = coordinates
        self.bodyPartsCount = len(self.coordinates)
        self._setLength()

    def _setLength(self) -> None:
        self.length = max(self.coordinates, key=lambda coordinate: coordinate.x).x - min(self.coordinates, key=lambda coordinate: coordinate.x).x

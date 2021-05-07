from typing import List
from Coordinates import Coordinates


class SeaMonster:
    def __init__(self, coordinates: List[Coordinates]):
        self._coordinates: List[Coordinates] = coordinates

    def getCoordinates(self):
        if not self._coordinates:
            raise ValueError("Coordinates not set for sea monster.")

        return self._coordinates

    def getBodyPartsCount(self) -> int:
        return len(self._coordinates)

    def getLength(self) -> int:
        return max(self._coordinates, key=lambda coordinate: coordinate.x).x - min(self._coordinates, key=lambda coordinate: coordinate.x).x

from typing import List
from Coordinates import Coordinates

class SeaMonster:
    def __init__(self):
        self.coordinates: List[Coordinates] = []
        self.length: int = 0
        self.bodyPartsCount = 0

    def setCoordinates(self, coordinates: List[Coordinates]) -> None:
        if not coordinates:
            raise ValueError("Coordinates missing when setting coordinates for sea monster.")

        self.coordinates = coordinates
        self.bodyPartsCount = len(self.coordinates)
        self._setLength()

    def _setLength(self) -> None:
        if not self.coordinates:
            raise ValueError("Coordinates for the sea monster not found.")

        self.length = max(self.coordinates, key=lambda coordinate: coordinate.x).x - min(self.coordinates, key=lambda coordinate: coordinate.x).x

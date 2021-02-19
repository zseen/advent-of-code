from typing import List
from Coordinates import Coordinates

class SeaMonster:
    def __init__(self):
        self._coordinates: List[Coordinates] = []

    def setCoordinates(self, coordinates: List[Coordinates]) -> None:
        if not coordinates:
            raise ValueError("Coordinates missing when setting coordinates for sea monster.")

        self._coordinates = coordinates


    def getCoordinates(self):
        if not self._coordinates:
            raise ValueError("Coordinates not set for sea monster.")

        return self._coordinates
        

    def getBodyPartsCount(self) -> int:
        return len(self._coordinates)

    def getLength(self) -> int:
        if not self._coordinates:
            raise ValueError("Coordinates for the sea monster not found.")

        return max(self._coordinates, key=lambda coordinate: coordinate.x).x - min(self._coordinates, key=lambda coordinate: coordinate.x).x
        

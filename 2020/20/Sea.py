from typing import List
from Tile import Tile
from SeaMonster import SeaMonster


class Sea(Tile):
    def __init__(self, pixelRows: List[str], seaMonster: SeaMonster):
        self._pixelRows = pixelRows
        self._seaMonster = seaMonster

    def calculateWaterRoughness(self) -> int:
        allRoughnessCount = sum(1 for j in range(0, len(self._pixelRows)) for i in range(0, len(self._pixelRows[j])) if self._pixelRows[j][i] == "#")
        return allRoughnessCount - (self._getSeaMonsterCount() * self._seaMonster.getBodyPartsCount())

    def _getSeaMonsterCount(self) -> int:
        for _ in range(0, 2):
            for _ in range(0, 4):
                seaMonstersCount = self._countSeaMonstersInCurrentSeaAlignment()
                if seaMonstersCount > 0:
                    return seaMonstersCount
                self.rotateRight()
            self.flipSideways()

        raise ValueError("No sea monster found.")

    def _countSeaMonstersInCurrentSeaAlignment(self) -> int:
        seaMonsterCount = 0
        for j in range(1, len(self._pixelRows) - 1):
            for i in range(0, (len(self._pixelRows[j])) - self._seaMonster.getLength() - 1):
                if self._isSeaMonsterHere(i, j):
                    seaMonsterCount += 1
        return seaMonsterCount

    def _isSeaMonsterHere(self, seaCoordinateX: int, seaCoordinateY: int) -> bool:
        for seaMonsterCoordinate in self._seaMonster.getCoordinates():
            if self._pixelRows[seaCoordinateY + seaMonsterCoordinate.y][seaCoordinateX + seaMonsterCoordinate.x] != "#":
                return False
        return True

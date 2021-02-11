from typing import List

from Tile import Tile
from SeaMonster import SeaMonster


class Sea(Tile):
    def __init__(self, pixelRows: List[str], seaMonster: SeaMonster):
        self.pixelRows = pixelRows
        self._seaMonster = seaMonster

    def calculateWaterRoughness(self) -> int:
        allRoughnessCount = sum(1 for j in range(0, len(self.pixelRows)) for i in range(0, len(self.pixelRows[j])) if self.pixelRows[j][i] == "#")
        return allRoughnessCount - (self._getSeaMonsterCount() * self._seaMonster.bodyPartsCount)

    def _getSeaMonsterCount(self) -> int:
        for _ in range(0, 2):
            for _ in range(0, 4):
                seaMonstersCount = self._countSeaMonstersInCurrentSeaAlignment()
                if seaMonstersCount:
                    return seaMonstersCount
                self.rotateRight()
            self.flipSideways()

        raise ValueError("No sea monster found.")

    def _countSeaMonstersInCurrentSeaAlignment(self) -> int:
        return sum(1 for j in range(1, len(self.pixelRows) - 1) for i in range(0, (len(self.pixelRows[j]) - self._seaMonster.length - 1)) if
                   self._isSeaMonsterHere(i, j))

    def _isSeaMonsterHere(self, seaCoordinateX: int, seaCoordinateY: int) -> bool:
        for seaMonsterCoordinate in self._seaMonster.coordinates:
            if self.pixelRows[seaCoordinateY + seaMonsterCoordinate.y][seaCoordinateX + seaMonsterCoordinate.x] != "#":
                return False
        return True

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
        seaMonstersCount = self._checkForSeaMonsterInBoard()
        if seaMonstersCount:
            return seaMonstersCount

        self.flipSideways()
        seaMonstersCount = self._checkForSeaMonsterInBoard()
        if seaMonstersCount:
            return seaMonstersCount

        raise ValueError("Not a single sea monster...really?")

    def _checkForSeaMonsterInBoard(self) -> int:
        for _ in range(0, 4):
            seaMonsterCount = self._countSeaMonstersInCurrentSeaAlignment()
            if seaMonsterCount > 0:
                return seaMonsterCount
            self.rotateRight()

    def _countSeaMonstersInCurrentSeaAlignment(self) -> int:
        seaMonstersCount = 0

        for j in range(1, len(self.pixelRows) - 1):
            for i in range(0, (len(self.pixelRows[j]) - self._seaMonster.length - 1)):
                if self.pixelRows[j][i] == "#":
                    isSeaMonsterPossible = True
                    for seaMonsterCoordinate in self._seaMonster.coordinates:
                        if self.pixelRows[j + seaMonsterCoordinate.y][i + seaMonsterCoordinate.x] != "#":
                            isSeaMonsterPossible = False
                            break
                    if isSeaMonsterPossible:
                        seaMonstersCount += 1

        return seaMonstersCount

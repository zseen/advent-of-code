import math
from typing import List
from Tile import Tile
import PuzzleHelper as PH


class Puzzle:
    def __init__(self, _tiles: List[Tile]):
        self._tiles = _tiles
        self._corners: List[Tile] = []
        self._rowAndColumnSize = int(math.sqrt(len(self._tiles)))
        self._puzzleWithTilesPositioned = [[0 for _ in range(self._rowAndColumnSize)] for _ in range(self._rowAndColumnSize)]

    def getCornerTilesIdsProduct(self) -> int:
        return math.prod([int(corner.id) for corner in self._corners])

    def putPuzzleTogether(self) -> None:
        self._findCorners()
        self._puzzleTiles()

    def _findCorners(self) -> None:
        PH.findNeighboursForTiles(self._tiles)
        self._corners = [tile for tile in self._tiles if len(tile.neighbourTiles) == 2]

    def _puzzleTiles(self) -> None:
        PH.fillUpPuzzleFirstRow(self._corners, self._puzzleWithTilesPositioned)
        PH.fillUpPuzzleBody(self._puzzleWithTilesPositioned)













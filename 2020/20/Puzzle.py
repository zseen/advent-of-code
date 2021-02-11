import math
from typing import List
from Tile import Tile
import PuzzleHelper as PH

boardType = List[List[Tile]]


class Puzzle:
    def __init__(self, _tiles: List[Tile]):
        self._tiles = _tiles
        self._corners: List[Tile] = []
        self._rowAndColumnSize = int(math.sqrt(len(self._tiles)))
        self._board = [[0 for _ in range(self._rowAndColumnSize)] for _ in range(self._rowAndColumnSize)]

    def getCornerTilesIdsProduct(self) -> int:
        if not self._corners:
            raise ValueError("Corner tiles not determined.")

        return math.prod([int(corner.id) for corner in self._corners])

    def getPuzzleBoard(self) -> boardType:
        if not self._board:
            raise ValueError("Board not found, maybe the tiles are missing.")

        return self._board

    def putPuzzleTogether(self) -> None:
        if not self._tiles:
            raise ValueError("No tiles to build the puzzle from.")

        self._findCorners()
        self._puzzleTiles()

    def _findCorners(self) -> None:
        PH.findNeighboursForTiles(self._tiles)
        self._corners = [tile for tile in self._tiles if len(tile.neighbourTiles) == 2]

    def _puzzleTiles(self) -> None:
        PH.fillUpPuzzleFirstRow(self._corners, self._board)
        PH.fillUpPuzzleBody(self._board)

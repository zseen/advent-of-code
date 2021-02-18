import math
from typing import List
from Tile import Tile
import PuzzleHelper as PH

BoardType = PH.BoardType


class Puzzle:
    def __init__(self, _tiles: List[Tile]):
        self._tiles = _tiles
        self._corners: List[Tile] = []
        self._size = int(math.sqrt(len(self._tiles)))
        self._board : Optional[Tile] = [[None for _ in range(self._size)] for _ in range(self._size)]

    def getCornerTilesIdsProduct(self) -> int:
        if not self._corners:
            raise ValueError("Corner tiles not determined.")

        return math.prod([int(corner.id) for corner in self._corners])

    def getPuzzleBoard(self) -> BoardType:
        return self._board

    def assemble(self) -> None:
        if not self._tiles:
            raise ValueError("No tiles to build the puzzle from.")

        self._findCorners()
        self._arrangeTilesOnBoard()

    def _findCorners(self) -> None:
        PH.findNeighboursForTiles(self._tiles)
        self._corners = [tile for tile in self._tiles if len(tile.neighbourTiles) == 2]

    def _arrangeTilesOnBoard(self) -> None:
        PH.fillUpPuzzleFirstRow(self._corners, self._board)
        PH.fillUpPuzzleBody(self._board)

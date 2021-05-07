import math
from typing import List
from Tile import Tile
import PuzzleHelper as PH


class Puzzle:
    def __init__(self, tiles: List[Tile]):
        self._tiles = tiles
        self._corners: List[Tile] = []
        self._size = int(math.sqrt(len(self._tiles)))
        self._board: Optional[Tile] = [[None for _ in range(self._size)] for _ in range(self._size)]

    def getCornerTilesIdProduct(self) -> int:
        if not self._corners:
            raise ValueError("Corner tiles not determined.")

        return math.prod([int(corner.id) for corner in self._corners])

    def getPuzzleBoard(self) -> PH.BoardType:
        return self._board

    def assemble(self) -> None:
        if not self._tiles:
            raise ValueError("No tiles to build the puzzle from.")

        self._findCorners()
        self._alignTopLeftCornerIntoBoard()
        self._fillUpPuzzleFirstRow()
        self._fillUpPuzzleBody()

    def _findCorners(self) -> None:
        self._findNeighborsForTiles()
        self._corners = [tile for tile in self._tiles if len(tile.getNeighborTiles()) == 2]

    def _findNeighborsForTiles(self) -> None:
        if not self._tiles:
            raise ValueError("Empty list of tiles received.")

        for i in range(0, len(self._tiles)):
            for j in range(i + 1, len(self._tiles)):
                tile1 = self._tiles[i]
                tile2 = self._tiles[j]
                if PH.areTilesNeighbors(tile1, tile2):
                    tile1.addNeighborTile(tile2)
                    tile2.addNeighborTile(tile1)

    def _alignTopLeftCornerIntoBoard(self) -> None:
        assert self._board

        if not self._corners:
            raise ValueError("Corners missing.")

        topLeftCorner = self._corners[0]
        neighborsEdges = topLeftCorner.getAllEdgesFromAllNeighbors()
        for _ in range(0, 4):
            isRightEdgeAligning = topLeftCorner.getRightEdge() in neighborsEdges or topLeftCorner.getRightEdge()[::-1] in neighborsEdges
            isBottomEdgeAligning = topLeftCorner.getBottomEdge() in neighborsEdges or topLeftCorner.getBottomEdge()[::-1] in neighborsEdges
            if isRightEdgeAligning and isBottomEdgeAligning:
                self._board[0][0] = topLeftCorner
                return
            topLeftCorner.rotateRight()

    def _fillUpPuzzleFirstRow(self) -> None:
        if not self._board:
            raise ValueError("Puzzle board missing, so cannot be filled up.")

        currentTile = self._board[0][0]
        for columnIndex in range(1, len(self._board[0])):
            for neighbor in currentTile.getNeighborTiles():
                if PH.isHorizontalAlignmentPossible(currentTile, neighbor):
                    self._board[0][columnIndex] = neighbor
                    currentTile = neighbor

    def _fillUpPuzzleBody(self) -> None:
        for j in range(1, len(self._board)):
            for i in range(0, len(self._board[0])):
                self._populateField(i, j)

    def _populateField(self, columnIndex: int, rowIndex: int) -> None:
        fixedTile = self._board[rowIndex - 1][columnIndex]
        for neighbor in fixedTile.getNeighborTiles():
            if PH.isVerticalAlignmentPossible(fixedTile, neighbor):
                self._board[rowIndex][columnIndex] = neighbor

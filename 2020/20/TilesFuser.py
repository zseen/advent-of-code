from typing import List
from Tile import Tile
import PuzzleHelper as PH

class TilesFuser:
    def __init__(self):
        self._rowIndex = 0
        self._columnIndex = 0
        self._tileRowIndex = 0
        self._tileColumnIndex = 0
        self._tileSideLength = 0
        self._tilePixelRowLength = 0

    def createBoardWithTilePixelsFusedTogether(self, puzzleBoard: PH.BoardType) -> List[str]:
        if not puzzleBoard:
            raise ValueError("Puzzle board missing - cannot remove tile edges.")

        self._calculateTileEdgesLength(puzzleBoard)

        boardWithTrimmedEdgedTiles: List[str] = []
        while self._rowIndex < len(puzzleBoard) and self._columnIndex < len(puzzleBoard):
            while self._tileRowIndex < self._tileSideLength:
                self._addPixelRowsToBoard(boardWithTrimmedEdgedTiles, puzzleBoard)
            self._rowIndex += 1
            self._tileRowIndex = 0

        return boardWithTrimmedEdgedTiles

    def _calculateTileEdgesLength(self, puzzleBoard: PH.BoardType) -> None:
        if not puzzleBoard or not puzzleBoard[0][0]:
            raise ValueError("Top left corner of puzzle board is not a tile")

        self._tileSideLength = len(puzzleBoard[0][0].getRightEdge())
        self._tilePixelRowLength = len(puzzleBoard[0][0].getTopEdge())

    def _addPixelRowsToBoard(self, boardWithTrimmedEdgedTiles: List[str], puzzleBoard: PH.BoardType) -> None:
        pixelsIncurrentRow = self._collectPixelsFromAllTilesInRow(puzzleBoard)
        boardWithTrimmedEdgedTiles.append(pixelsIncurrentRow)
        self._tileRowIndex += 1
        self._columnIndex = 0

    def _collectPixelsFromAllTilesInRow(self, puzzleBoard: PH.BoardType) -> str:
        currentRow = ""

        while self._columnIndex < len(puzzleBoard[0]):
            currentTile = puzzleBoard[self._rowIndex][self._columnIndex]
            while self._tileColumnIndex < self._tilePixelRowLength:
                currentRow += currentTile.getPixelAtPosition(self._tileRowIndex, self._tileColumnIndex)
                self._tileColumnIndex += 1
            self._tileColumnIndex = 0
            self._columnIndex += 1

        return currentRow

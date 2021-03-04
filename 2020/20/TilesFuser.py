from typing import List
from Tile import Tile
import PuzzleHelper as PH


class TilesFuser:
    def __init__(self, tileEdgeLength):
        self._tileEdgeLength = tileEdgeLength
        self._rowIndex = 0
        self._columnIndex = 0
        self._tileRowIndex = 0
        self._tileColumnIndex = 0

    def createBoardWithTilePixelsFusedTogether(self, puzzleBoard: PH.BoardType) -> List[str]:
        if not puzzleBoard:
            raise ValueError("Puzzle board missing - cannot remove tile edges.")

        boardWithTrimmedEdgedTiles: List[str] = []
        while self._rowIndex < len(puzzleBoard) and self._columnIndex < len(puzzleBoard):
            while self._tileRowIndex < self._tileEdgeLength:
                self._addPixelRowsToBoard(boardWithTrimmedEdgedTiles, puzzleBoard)
            self._rowIndex += 1
            self._tileRowIndex = 0

        return boardWithTrimmedEdgedTiles

    def _addPixelRowsToBoard(self, boardWithTrimmedEdgedTiles: List[str], puzzleBoard: PH.BoardType) -> None:
        pixelsIncurrentRow = self._collectPixelsFromAllTilesInRow(puzzleBoard)
        boardWithTrimmedEdgedTiles.append(pixelsIncurrentRow)
        self._tileRowIndex += 1
        self._columnIndex = 0

    def _collectPixelsFromAllTilesInRow(self, puzzleBoard: PH.BoardType) -> str:
        currentRow = ""

        while self._columnIndex < len(puzzleBoard[0]):
            currentTile = puzzleBoard[self._rowIndex][self._columnIndex]
            while self._tileColumnIndex < self._tileEdgeLength:
                currentRow += currentTile.getPixelAtPosition(self._tileRowIndex, self._tileColumnIndex)
                self._tileColumnIndex += 1
            self._tileColumnIndex = 0
            self._columnIndex += 1

        return currentRow

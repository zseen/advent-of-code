from typing import List
from PuzzleHelper import BoardType
from Tile import Tile


class TileEdgesRemover:
    def __init__(self):
        self._rowIndex = 0
        self._columnIndex = 0
        self._tileRowIndex = 0
        self._tileColumnIndex = 0
        self._tileSideEdgeLength = 0
        self._tilePixelRowLength = 0

    def removeTileEdgesPixelsFromBoard(self, boardWithTilePixels: List[str]) -> List[str]:
        if not boardWithTilePixels:
            raise ValueError("Board with pixel rows not received.")

        boardWithTopBottomTileEdgesPixelsRemoved = self._removeTileTopAndBottomEdgesPixelRowsFromBoard(boardWithTilePixels)
        return self._removeTileSideEdgesPixelsFromBoard(boardWithTopBottomTileEdgesPixelsRemoved)

    def createBoardWithTilePixelsFusedTogetherInRows(self, puzzleBoard: BoardType) -> List[str]:
        if not puzzleBoard:
            raise ValueError("Puzze board missing - cannot remove tile edges.")

        self._calculateTileEdgesLength(puzzleBoard)

        boardWithTrimmedEdgedTiles = []
        while self._rowIndex < len(puzzleBoard) and self._columnIndex < len(puzzleBoard):
            while self._tileRowIndex < self._tileSideEdgeLength:
                self._addPixelRowsToBoard(boardWithTrimmedEdgedTiles, puzzleBoard)
            self._rowIndex += 1
            self._tileRowIndex = 0

        return boardWithTrimmedEdgedTiles

    def _calculateTileEdgesLength(self, puzzleBoard: BoardType) -> None:
        if not isinstance(puzzleBoard[0][0], Tile):
            raise ValueError("Top left corner of puzzle board is not a tile")

        self._tileSideEdgeLength = len(puzzleBoard[0][0].rightEdge)
        self._tilePixelRowLength = len(puzzleBoard[0][0].topEdge)

    def _addPixelRowsToBoard(self, boardWithTrimmedEdgedTiles: List[str], puzzleBoard: BoardType) -> None:
        pixelsIncurrentRow = self._collectPixelsFromAllTilesInRow(puzzleBoard)
        boardWithTrimmedEdgedTiles.append(pixelsIncurrentRow)
        self._tileRowIndex += 1
        self._columnIndex = 0

    def _collectPixelsFromAllTilesInRow(self, puzzleBoard: BoardType) -> str:
        currentRow = ""

        while self._columnIndex < len(puzzleBoard[0]):
            currentTile = puzzleBoard[self._rowIndex][self._columnIndex]
            while self._tileColumnIndex < self._tilePixelRowLength:
                currentRow += currentTile.getPixelAtPosition(self._tileRowIndex, self._tileColumnIndex)
                self._tileColumnIndex += 1
            self._tileColumnIndex = 0
            self._columnIndex += 1

        return currentRow

    def _removeTileTopAndBottomEdgesPixelRowsFromBoard(self, boardWithPixelRows: List[str]) -> List[str]:
        boardWithTopBottomTileEdgesPixelsRemoved = []

        if self._tileSideEdgeLength == 0:
            raise ValueError("Tile side edge is missing or miscalculated.")

        for _rowIndex in range(0, len(boardWithPixelRows)):
            if _rowIndex % self._tileSideEdgeLength != 0 and _rowIndex % self._tileSideEdgeLength != self._tileSideEdgeLength - 1:
                boardWithTopBottomTileEdgesPixelsRemoved.append(boardWithPixelRows[_rowIndex])
        return boardWithTopBottomTileEdgesPixelsRemoved

    def _removeTileSideEdgesPixelsFromBoard(self, boardWithPixelRows: List[str]) -> List[str]:
        tilesPixelsWithSideEdgesCutOff = []

        for pixelRow in boardWithPixelRows:
            tilePixelsWithoutSideEdgesInRowCombined = ""
            for pixelIndex in range(0, len(pixelRow), self._tilePixelRowLength):
                tilePixelsWithoutSideEdgesInRowCombined += pixelRow[pixelIndex + 1: pixelIndex + self._tilePixelRowLength - 1]
            tilesPixelsWithSideEdgesCutOff.append(tilePixelsWithoutSideEdgesInRowCombined)
        return tilesPixelsWithSideEdgesCutOff

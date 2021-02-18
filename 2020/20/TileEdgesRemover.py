from typing import List
from PuzzleHelper import BoardType
from Tile import Tile


class TileEdgesRemover:
    def __init__(self):
        self.rowIndex = 0
        self.columnIndex = 0
        self.tileRowIndex = 0
        self.tileColumnIndex = 0
        self.tileSideEdgeLength = 0
        self.tilePixelRowLength = 0

    def removeTileEdgesPixelsFromBoard(self, boardWithTilePixels: List[str]) -> List[str]:
        if not boardWithTilePixels:
            raise ValueError("Board with pixel rows not received.")

        boardWithTopBottomTileEdgesPixelsRemoved = self._removeTileTopAndBottomEdgesPixelRowsFromBoard(boardWithTilePixels)
        return self._removeTileSideEdgesPixelsFromBoard(boardWithTopBottomTileEdgesPixelsRemoved)

    def createBoardWithTilePixelsFusedTogetherInRows(self, puzzleBoard: BoardType) -> List[str]:
        if not puzzleBoard:
            raise ValueError("Puzze board missing - cannot remove tile edges.")

        self._calculateTileEsgesLength(puzzleBoard)

        boardWithTrimmedEdgedTiles = []
        while self.rowIndex < len(puzzleBoard) and self.columnIndex < len(puzzleBoard):
            while self.tileRowIndex < self.tileSideEdgeLength:
                self._addPixelRowsToBoard(boardWithTrimmedEdgedTiles, puzzleBoard)
            self.rowIndex += 1
            self.tileRowIndex = 0

        return boardWithTrimmedEdgedTiles

    def _calculateTileEsgesLength(self, puzzleBoard: BoardType) -> None:
        if not isinstance(puzzleBoard[0][0], Tile):
            raise ValueError("Top left corner of puzzle board is not a tile")

        self.tileSideEdgeLength = len(puzzleBoard[0][0].rightEdge)
        self.tilePixelRowLength = len(puzzleBoard[0][0].topEdge)

    def _addPixelRowsToBoard(self, boardWithTrimmedEdgedTiles: List[str], puzzleBoard: BoardType) -> None:
        pixelsIncurrentRow = self._collectPixelsFromAllTilesInRow(puzzleBoard)
        boardWithTrimmedEdgedTiles.append(pixelsIncurrentRow)
        self.tileRowIndex += 1
        self.columnIndex = 0

    def _collectPixelsFromAllTilesInRow(self, puzzleBoard: BoardType) -> str:
        currentRow = ""

        while self.columnIndex < len(puzzleBoard[0]):
            currentTile = puzzleBoard[self.rowIndex][self.columnIndex]
            while self.tileColumnIndex < len(currentTile.pixelRows[0]):
                currentRow += currentTile.pixelRows[self.tileRowIndex][self.tileColumnIndex]
                self.tileColumnIndex += 1
            self.tileColumnIndex = 0
            self.columnIndex += 1

        return currentRow

    def _removeTileTopAndBottomEdgesPixelRowsFromBoard(self, boardWithPixelRows: List[str]) -> List[str]:
        boardWithTopBottomTileEdgesPixelsRemoved = []

        if self.tileSideEdgeLength == 0:
            raise ValueError("Tile side edge is missing or miscalculated.")

        for rowIndex in range(0, len(boardWithPixelRows)):
            if rowIndex % self.tileSideEdgeLength != 0 and rowIndex % self.tileSideEdgeLength != self.tileSideEdgeLength - 1:
                boardWithTopBottomTileEdgesPixelsRemoved.append(boardWithPixelRows[rowIndex])
        return boardWithTopBottomTileEdgesPixelsRemoved

    def _removeTileSideEdgesPixelsFromBoard(self, boardWithPixelRows: List[str]) -> List[str]:
        tilesPixelsWithSideEdgesCutOff = []

        for pixelRow in boardWithPixelRows:
            tilePixelsWithoutSideEdgesInRowCombined = ""
            for pixelIndex in range(0, len(pixelRow), self.tilePixelRowLength):
                tilePixelsWithoutSideEdgesInRowCombined += pixelRow[pixelIndex + 1: pixelIndex + self.tilePixelRowLength - 1]
            tilesPixelsWithSideEdgesCutOff.append(tilePixelsWithoutSideEdgesInRowCombined)
        return tilesPixelsWithSideEdgesCutOff

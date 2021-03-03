from typing import List
from PuzzleHelper import BoardType
from Tile import Tile



class TileEdgesRemover:
    def __init__(self):
        self._tileSideLength = 0
        self._tilePixelRowLength = 0

    def removeTileEdgesPixelsFromBoard(self, boardWithTilePixels: List[str]) -> List[str]:
        if not boardWithTilePixels:
            raise ValueError("Board with pixel rows not received.")


        boardWithTopBottomTileEdgesPixelsRemoved = self._removeTileTopAndBottomEdgesPixelRowsFromBoard(boardWithTilePixels)
        return self._removeTileSideEdgesPixelsFromBoard(boardWithTopBottomTileEdgesPixelsRemoved)


    def _removeTileTopAndBottomEdgesPixelRowsFromBoard(self, boardWithPixelRows: List[str]) -> List[str]:
        boardWithTopBottomTileEdgesPixelsRemoved = []

        if self._tileSideLength == 0:
            raise ValueError("Tile side edge is missing or miscalculated.")

        for rowIndex in range(0, len(boardWithPixelRows)):
            if rowIndex % self._tileSideLength != 0 and rowIndex % self._tileSideLength != self._tileSideLength - 1:
                boardWithTopBottomTileEdgesPixelsRemoved.append(boardWithPixelRows[rowIndex])
        return boardWithTopBottomTileEdgesPixelsRemoved

    def _removeTileSideEdgesPixelsFromBoard(self, boardWithPixelRows: List[str]) -> List[str]:
        tilesPixelsWithSideEdgesCutOff = []

        for pixelRow in boardWithPixelRows:
            tilePixelsWithoutSideEdgesInRowCombined = ""
            for pixelIndex in range(0, len(pixelRow), self._tilePixelRowLength):
                tilePixelsWithoutSideEdgesInRowCombined += pixelRow[pixelIndex + 1: pixelIndex + self._tilePixelRowLength - 1]
            tilesPixelsWithSideEdgesCutOff.append(tilePixelsWithoutSideEdgesInRowCombined)
        return tilesPixelsWithSideEdgesCutOff

import math
from typing import List, Set, Tuple
from Tile import Tile

neighbourTilesPairsType = Set[Tuple[Tile, Tile]]
boardType = List[List[Tile]]


def findNeighboursForTiles(tiles: List[Tile]) -> None:
    if not tiles:
        raise ValueError("Empty list of tiles received.")

    neighbourTilesPairs: neighbourTilesPairsType = set()

    for i in range(0, len(tiles)):
        for j in range(i + 1, len(tiles)):
            tile1 = tiles[i]
            tile2 = tiles[j]
            assignPossibleNeighbourhood(tile1, tile2, neighbourTilesPairs)


def assignPossibleNeighbourhood(tile1: Tile, tile2: Tile, neighbourTilesPairs: neighbourTilesPairsType) -> None:
    if (tile1, tile2) in neighbourTilesPairs:
        return
    if areTilesNeighbours(tile1, tile2):
        tile1.neighbourTiles.add(tile2)
        tile2.neighbourTiles.add(tile1)
        neighbourTilesPairs.add((tile1, tile2))
        neighbourTilesPairs.add((tile2, tile1))


def areTilesNeighbours(tile1: Tile, tile2: Tile) -> bool:
    return any(edge for edge in tile1.edges if edge in tile2.edges or edge[::-1] in tile2.edges)


def fillUpPuzzleFirstRow(corners: List[Tile], puzzleBoard: boardType) -> None:
    if not puzzleBoard:
        raise ValueError("Problem with puzzle board to fill up.")

    topLeftCorner = findTopLeftCorner(corners)
    puzzleBoard[0][0] = topLeftCorner

    currentTile = topLeftCorner
    for columnIndex in range(1, len(puzzleBoard[0])):
        for neigbour in currentTile.neighbourTiles:
            if isHorizontalAlignmentPossible(neigbour, currentTile):
                puzzleBoard[0][columnIndex] = neigbour
                currentTile = neigbour


def findTopLeftCorner(corners: List[Tile]) -> Tile:
    for corner in corners:
        neighboursEdges = getAllEdgesFromAllNeighbours(corner)
        for _ in range(0, 4):
            if (corner.rightEdge in neighboursEdges or corner.rightEdge[::-1] in neighboursEdges) and (
                    corner.bottomEdge in neighboursEdges or corner.bottomEdge[::-1] in neighboursEdges):
                return corner
            corner.rotateRight()

    raise ValueError("Top left corner not found")


def getAllEdgesFromAllNeighbours(tile: Tile) -> List[str]:
    neighboursEdges = []
    for neighbour in tile.neighbourTiles:
        neighboursEdges.extend(neighbour.edges)
    return neighboursEdges


def fillUpPuzzleBody(puzzleBoard: boardType) -> None:
    for j in range(1, len(puzzleBoard)):
        for i in range(0, len(puzzleBoard[0])):
            populatePuzzleBoardBody(i, j, puzzleBoard)


def populatePuzzleBoardBody(columnIndex: int, rowIndex: int, puzzleBoard: boardType) -> None:
    currentTile = puzzleBoard[rowIndex - 1][columnIndex]
    for neigbour in currentTile.neighbourTiles:
        if isVerticalAlignmentPossible(neigbour, currentTile):
            puzzleBoard[rowIndex][columnIndex] = neigbour


def isHorizontalAlignmentPossible(neighbour: Tile, correctlyAlignedTile: Tile) -> bool:
    for _ in range(0, 2):
        for _ in range(0, 4):
            if neighbour.leftEdge == correctlyAlignedTile.rightEdge:
                return True
            neighbour.rotateRight()
        neighbour.flipSideways()


def isVerticalAlignmentPossible(neighbour: Tile, correctlyAlignedTile: Tile) -> bool:
    for _ in range(0, 2):
        for _ in range(0, 4):
            if neighbour.topEdge == correctlyAlignedTile.bottomEdge:
                return True
            neighbour.rotateRight()
        neighbour.flipSideways()


class TileEdgesRemover:
    def __init__(self):
        self.rowIndex = 0
        self.columnIndex = 0
        self.tileRowIndex = 1
        self.tileColumnIndex = 1

    def removeTileEdgesFromCompletedPuzzle(self, puzzleBoard: boardType) -> List[str]:
        if not puzzleBoard:
            raise ValueError("Problem with puzzle board to remove tile edges from.")

        boardWithTrimmedEdgedTiles = []
        maxRowIndex, maxColumnIndex = len(puzzleBoard), len(puzzleBoard)

        while self.rowIndex < maxRowIndex and self.columnIndex < maxColumnIndex:
            while self.tileRowIndex < len(puzzleBoard[0][0].pixelRows) - 1:
                self._addPixelRowsToBoard(boardWithTrimmedEdgedTiles, puzzleBoard)
            self.rowIndex += 1
            self.tileRowIndex = 1

        return boardWithTrimmedEdgedTiles

    def _addPixelRowsToBoard(self, boardWithTrimmedEdgedTiles: List[str], puzzleBoard: boardType):
        pixelsIncurrentRow = self._collectPixelsFromAllTilesInRow(puzzleBoard)
        boardWithTrimmedEdgedTiles.append(pixelsIncurrentRow)
        self.tileRowIndex += 1
        self.columnIndex = 0

    def _collectPixelsFromAllTilesInRow(self, puzzleBoard: boardType) -> str:
        currentRow = ""
        while self.columnIndex < len(puzzleBoard[0]):
            currentTile = puzzleBoard[self.rowIndex][self.columnIndex]
            while self.tileColumnIndex < len(currentTile.pixelRows[0]) - 1:
                currentRow += currentTile.pixelRows[self.tileRowIndex][self.tileColumnIndex]
                self.tileColumnIndex += 1
            self.tileColumnIndex = 1
            self.columnIndex += 1
        return currentRow

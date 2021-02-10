import math
from typing import List, Set, Tuple
from Tile import Tile


def findNeighboursForTiles(tiles) -> None:
    neighbourTilesPairs: Set[Tuple[Tile, Tile]] = set()

    for i in range(0, len(tiles)):
        for j in range(i + 1, len(tiles)):
            tile1 = tiles[i]
            tile2 = tiles[j]
            if (tile1, tile2) in neighbourTilesPairs:
                continue
            if areTilesNeighbours(tile1, tile2):
                tile1.neighbourTiles.add(tile2)
                tile2.neighbourTiles.add(tile1)
                neighbourTilesPairs.add((tile1, tile2))
                neighbourTilesPairs.add((tile2, tile1))


def areTilesNeighbours(tile1: Tile, tile2: Tile) -> bool:
    for edge in tile1.edges:
        if edge in tile2.edges or edge[::-1] in tile2.edges:
            return True
    return False


def fillUpPuzzleFirstRow(corners: List[Tile], puzzleBoard: List[List[Tile]]) -> None:
    topLeftCorner = findTopLeftCorner(corners)
    puzzleBoard[0][0] = topLeftCorner

    currentTile = topLeftCorner
    for columnIndex in range(1, len(puzzleBoard[0])):
        for neigbour in currentTile.neighbourTiles:
            if isHorizontalAlignmentPossible(neigbour, currentTile):
                puzzleBoard[0][columnIndex] = neigbour
                currentTile = neigbour


def findTopLeftCorner(corners: List[Tile]) -> Tile:
    rightNeighbourFound = False
    bottomNeighbourFound = False

    for corner in corners:
        neighboursEdges = []
        for neighbour in corner.neighbourTiles:
            neighboursEdges.extend(neighbour.edges)

        for _ in range(0, 4):
            if corner.rightEdge in neighboursEdges or corner.rightEdge[::-1] in neighboursEdges:
                rightNeighbourFound = True
            if corner.bottomEdge in neighboursEdges or corner.bottomEdge[::-1] in neighboursEdges:
                bottomNeighbourFound = True

            if rightNeighbourFound and bottomNeighbourFound:
                return corner

            rightNeighbourFound = False
            bottomNeighbourFound = False
            corner.rotateRight()

    raise ValueError("Top left corner not found")


def fillUpPuzzleBody(puzzleBoard: List[List[Tile]]) -> None:
    for j in range(1, len(puzzleBoard)):
        for i in range(0, len(puzzleBoard[0])):
            currentTile = puzzleBoard[j - 1][i]
            for neigbour in currentTile.neighbourTiles:
                if isVerticalAlignmentPossible(neigbour, currentTile):
                    puzzleBoard[j][i] = neigbour


def isHorizontalAlignmentPossible(neighbour: Tile, correctlyAlignedTile: Tile) -> bool:
    for _ in range(0, 4):
        if neighbour.leftEdge == correctlyAlignedTile.rightEdge:
            return True
        neighbour.rotateRight()

    neighbour.flipSideways()
    for _ in range(0, 4):
        if neighbour.leftEdge == correctlyAlignedTile.rightEdge:
            return True
        neighbour.rotateRight()

    neighbour.flipSideways()
    return False


def isVerticalAlignmentPossible(neighbour: Tile, correctlyAlignedTile: Tile):
    for _ in range(0, 4):
        if neighbour.topEdge == correctlyAlignedTile.bottomEdge:
            return True
        neighbour.rotateRight()

    neighbour.flipSideways()
    for _ in range(0, 4):
        if neighbour.topEdge == correctlyAlignedTile.bottomEdge:
            return True
        neighbour.rotateRight()

    neighbour.flipSideways()
    return False


def removeTileEdgesFromCompletedPuzzle(puzzleBoard):
    boardWithTrimmedEdgedTiles = []

    rowIndex, columnIndex = 0, 0
    maxRowIndex, maxColumnIndex = len(puzzleBoard), len(puzzleBoard)

    tileRowIndex = 1
    while rowIndex < maxRowIndex and columnIndex < maxColumnIndex:
        while tileRowIndex < len(puzzleBoard[0][0].pixelRows) - 1:
            currentRow = ""
            while columnIndex < len(puzzleBoard[0]):
                currentTile = puzzleBoard[rowIndex][columnIndex]
                for tileColumnIndex in range(1, len(currentTile.pixelRows[0]) - 1):
                    currentRow += currentTile.pixelRows[tileRowIndex][tileColumnIndex]
                columnIndex += 1
            boardWithTrimmedEdgedTiles.append(currentRow)
            tileRowIndex += 1
            columnIndex = 0
        rowIndex += 1
        tileRowIndex = 1

    return boardWithTrimmedEdgedTiles

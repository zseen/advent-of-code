import math
from typing import List, Set, Tuple
from Tile import Tile

neighbourTilesPairsType = Set[Tuple[Tile, Tile]]
BoardType = List[List[Tile]]


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


def fillUpPuzzleFirstRow(corners: List[Tile], puzzleBoard: BoardType) -> None:
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


def fillUpPuzzleBody(puzzleBoard: BoardType) -> None:
    for j in range(1, len(puzzleBoard)):
        for i in range(0, len(puzzleBoard[0])):
            populatePuzzleBoardBody(i, j, puzzleBoard)


def populatePuzzleBoardBody(columnIndex: int, rowIndex: int, puzzleBoard: BoardType) -> None:
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


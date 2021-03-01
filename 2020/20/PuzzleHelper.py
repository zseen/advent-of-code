import math
from typing import List, Set, Tuple
from Tile import Tile

BoardType = List[List[Tile]]


def areTilesNeighbors(tile1: Tile, tile2: Tile) -> bool:
    tile1Edges = tile1.getEdges()
    tile2Edges = tile2.getEdges()
    return any(edge for edge in tile1Edges if edge in tile2Edges) or any(edge for edge in tile1Edges if edge[::-1] in tile2Edges)


def findTopLeftCorner(corners: List[Tile]) -> Tile:
    corner = corners[0]
    neighborsEdges = getAllEdgesFromAllNeighbors(corner)
    for _ in range(0, 4):
        isRightEdgeAligning = corner.rightEdge in neighborsEdges or corner.rightEdge[::-1] in neighborsEdges
        isBottomEdgeAligning = corner.bottomEdge in neighborsEdges or corner.bottomEdge[::-1] in neighborsEdges
        if isRightEdgeAligning and isBottomEdgeAligning:
            return corner
        corner.rotateRight()

    raise ValueError("Top left corner not found")


def isHorizontalAlignmentPossible(correctlyAlignedTile: Tile, neighbor: Tile) -> bool:
    for _ in range(0, 2):
        for _ in range(0, 4):
            if neighbor.leftEdge == correctlyAlignedTile.rightEdge:
                return True
            neighbor.rotateRight()
        neighbor.flipSideways()


def isVerticalAlignmentPossible(correctlyAlignedTile: Tile, neighbor: Tile) -> bool:
    for _ in range(0, 2):
        for _ in range(0, 4):
            if neighbor.topEdge == correctlyAlignedTile.bottomEdge:
                return True
            neighbor.rotateRight()
        neighbor.flipSideways()

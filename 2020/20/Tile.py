from typing import List, Set


class Tile:
    def __init__(self, id: str, pixelRows: List[str]):
        self.id = id
        self._pixelRows = pixelRows
        self._topEdge: str = ""
        self._bottomEdge: str = ""
        self._leftEdge: str = ""
        self._rightEdge: str = ""
        self._neighborTiles: Set[Tile] = set()

    def addNeighborTile(self, neighborTile: 'Tile') -> None:
        self._neighborTiles.add(neighborTile)

    def flipSideways(self) -> None:
        self._pixelRows = [row[::-1] for row in self._pixelRows]

    def rotateRight(self) -> None:
        self._pixelRows = [self._buildEdge(i)[::-1] for i in range(0, len(self._pixelRows))]

    def getTopEdge(self):
        self._topEdge = self._pixelRows[0]
        return self._topEdge

    def getBottomEdge(self):
        self._bottomEdge = self._pixelRows[-1]
        return self._bottomEdge

    def getRightEdge(self):
        self._rightEdge = self._buildEdge(-1)
        return self._rightEdge

    def getLeftEdge(self):
        self._leftEdge = self._buildEdge(0)
        return self._leftEdge

    def getEdges(self) -> List[str]:
        if not self._pixelRows:
            raise ValueError("Problem with getting edges, no pixelRows found in tile.")

        return [self.getRightEdge(), self.getTopEdge(), self.getLeftEdge(), self.getBottomEdge()]

    def getNeighborTiles(self):
        return self._neighborTiles

    def getAllEdgesFromAllNeighbors(self) -> Set[str]:
        neighborsEdges = []
        for neighbor in self._neighborTiles:
            neighborsEdges.extend(neighbor.getEdges())
        return set(neighborsEdges)

    def getPixelAtPosition(self, tileRowIdex, tileColumnIndex) -> str:
        return self._pixelRows[tileRowIdex][tileColumnIndex]

    def getTileEdgeLength(self):
        assert len(self._topEdge) == len(self._rightEdge) == len(self._bottomEdge) == len(self._leftEdge)
        return len(self._topEdge)

    def _buildEdge(self, pixelPosition: int) -> str:
        return "".join([row[pixelPosition] for row in self._pixelRows])

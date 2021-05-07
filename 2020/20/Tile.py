from typing import List, Set


class Tile:
    def __init__(self, id: str, pixelRows: List[str]):
        assert pixelRows
        self.id = id
        self._pixelRows = pixelRows
        self._neighborTiles: Set[Tile] = set()

    def addNeighborTile(self, neighborTile: 'Tile') -> None:
        self._neighborTiles.add(neighborTile)

    def flipSideways(self) -> None:
        self._pixelRows = [row[::-1] for row in self._pixelRows]

    def rotateRight(self) -> None:
        self._pixelRows = [self._buildEdge(i)[::-1] for i in range(0, len(self._pixelRows))]

    def getTopEdge(self) -> str:
        return self._pixelRows[0]

    def getBottomEdge(self) -> str:
        return self._pixelRows[-1]

    def getRightEdge(self) -> str:
        return self._buildEdge(-1)

    def getLeftEdge(self) -> str:
        return self._buildEdge(0)

    def getEdges(self) -> List[str]:
        return [self.getRightEdge(), self.getTopEdge(), self.getLeftEdge(), self.getBottomEdge()]

    def getNeighborTiles(self) -> Set:
        return self._neighborTiles

    def getAllEdgesFromAllNeighbors(self) -> Set[str]:
        neighborsEdges = []
        for neighbor in self._neighborTiles:
            neighborsEdges.extend(neighbor.getEdges())
        return set(neighborsEdges)

    def getPixelAtPosition(self, tileRowIdex, tileColumnIndex) -> str:
        return self._pixelRows[tileRowIdex][tileColumnIndex]

    def getTileEdgeLength(self):
        assert len(self.getTopEdge()) == len(self.getBottomEdge()) == len(self.getLeftEdge()) == len(self.getRightEdge())
        return len(self.getTopEdge())

    def _buildEdge(self, pixelPosition: int) -> str:
        return "".join([row[pixelPosition] for row in self._pixelRows])

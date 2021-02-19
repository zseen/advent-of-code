from typing import List, Set


class Tile:
    def __init__(self, id: str, pixelRows: List[str]):
        self.id = id
        self._pixelRows = pixelRows
        self.topEdge: str = ""
        self.bottomEdge: str = ""
        self.leftEdge: str = ""
        self.rightEdge: str = ""
        self.neighborTiles: Set[Tile] = set()

    def flipSideways(self) -> None:
        self._pixelRows = [line[::-1] for line in self._pixelRows]
        self.setEdges()

    def rotateRight(self) -> None:
        self._pixelRows = [self._buildEdge(i)[::-1] for i in range(0, len(self._pixelRows))]
        self.setEdges()

    def setEdges(self) -> None:
        if not self._pixelRows:
            raise ValueError("Problem with setting edges, no pixelRows found in tile.")

        self.topEdge = self._pixelRows[0]
        self.bottomEdge = self._pixelRows[-1]
        self.rightEdge = self._buildEdge(-1)
        self.leftEdge = self._buildEdge(0)

    def getEdges(self) -> List[str]:
        return [self.topEdge, self.bottomEdge, self.rightEdge, self.leftEdge]

    def getAllEdgesFromAllNeighbors(self) -> Set[str]:
        neighborsEdges = []
        for neighbor in self.neighborTiles:
            neighborsEdges.extend(neighbor.getEdges())
        return set(neighborsEdges)

    def getPixelAtPosition(self, tileRowIdex, tileColumnIndex) -> str:
        return self._pixelRows[tileRowIdex][tileColumnIndex]

    def _buildEdge(self, pixelPosition: int) -> str:
        return "".join([row[pixelPosition] for row in self._pixelRows])


from typing import List

class Tile:
    def __init__(self, id: str, pixelRows: List[str]):
        self.id = id
        self.pixelRows = pixelRows
        self.topEdge = None
        self.bottomEdge = None
        self.leftEdge = None
        self.rightEdge = None
        self.neighbourTiles = set()

    def setEdges(self) -> None:
        if not self.pixelRows:
            raise ValueError("Problem with setting edges")

        self.topEdge = self.pixelRows[0]
        self.bottomEdge = self.pixelRows[-1]
        self.rightEdge = self._buildEdge(-1)
        self.leftEdge = self._buildEdge(0)

    def flipSideways(self) -> None:
        self.pixelRows = [line[::-1] for line in self.pixelRows]
        self.setEdges()

    def rotateRight(self) -> None:
        self.pixelRows = [self._buildEdge(i)[::-1] for i in range(0, len(self.pixelRows))]
        self.setEdges()

    def _buildEdge(self, pixelPosition: int) -> str:
        return "".join([row[pixelPosition] for row in self.pixelRows])
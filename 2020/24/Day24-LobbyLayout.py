import unittest
from typing import List, Set
from Direction import Direction
from Coordinates import Coordinates
import InputHandler

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

NUM_EXECUTION_REPETITION = 100


class PathsProcessor:
    def __init__(self, destinationPaths: List[List[Direction]]) -> None:
        self._destinationPaths = destinationPaths
        self._blackTilesCoordinates: Set[Coordinates] = set()
        self._currentCoordinates: Coordinates = None

    def getBlackTilesCount(self) -> int:
        return len(self._blackTilesCoordinates)

    def getBlackTilesCoordinates(self) -> Set[Coordinates]:
        return self._blackTilesCoordinates

    def processAllPaths(self) -> None:
        for destinationPath in self._destinationPaths:
            self._followDirections(destinationPath)

    def _followDirections(self, destinationPath: List[Direction]) -> None:
        self._currentCoordinates = Coordinates(0, 0)

        for direction in destinationPath:
            self._moveToTileInDirection(direction)

        self._processNewTileColor()

    def _moveToTileInDirection(self, direction: Direction) -> None:
        if direction == Direction.WEST:
            self._currentCoordinates = Coordinates(self._currentCoordinates.x - 2, self._currentCoordinates.y)
        elif direction == Direction.EAST:
            self._currentCoordinates = Coordinates(self._currentCoordinates.x + 2, self._currentCoordinates.y)
        elif direction == Direction.NORTHWEST:
            self._currentCoordinates = Coordinates(self._currentCoordinates.x - 1, self._currentCoordinates.y + 1)
        elif direction == Direction.SOUTHWEST:
            self._currentCoordinates = Coordinates(self._currentCoordinates.x - 1, self._currentCoordinates.y - 1)
        elif direction == Direction.NORTHEAST:
            self._currentCoordinates = Coordinates(self._currentCoordinates.x + 1, self._currentCoordinates.y + 1)
        elif direction == Direction.SOUTHEAST:
            self._currentCoordinates = Coordinates(self._currentCoordinates.x + 1, self._currentCoordinates.y - 1)
        else:
            raise ValueError("Unknown direction to follow.")

    def _processNewTileColor(self) -> None:
        if self._currentCoordinates in self._blackTilesCoordinates:
            self._blackTilesCoordinates.remove(self._currentCoordinates)
        else:
            self._blackTilesCoordinates.add(self._currentCoordinates)


class ExhibitionArranger:
    def __init__(self, initialBlackTilesCoordinates: Set[Coordinates]):
        self._blackTilesCoordinates: Set[Coordinates] = initialBlackTilesCoordinates

    def getBlackTilesCount(self) -> int:
        return len(self._blackTilesCoordinates)

    def executeIteration(self) -> None:
        tilesCoordinatesToVisit = self._findTilesCoordinatesToVisit()
        visitedTilesCoordinates: Set[Coordinates] = set()
        nextBlackTilesCoordinates: Set[Coordinates] = self._blackTilesCoordinates.copy()

        while len(tilesCoordinatesToVisit) > 0:
            currentTileCoordinates = tilesCoordinatesToVisit.pop()
            visitedTilesCoordinates.add(currentTileCoordinates)
            currentTileBlackNeighborsCount = self._countBlackNeighbors(currentTileCoordinates)
            self._processNewTileColor(currentTileCoordinates, currentTileBlackNeighborsCount, nextBlackTilesCoordinates)

        self._blackTilesCoordinates = nextBlackTilesCoordinates

    def _findTilesCoordinatesToVisit(self) -> Set[Coordinates]:
        tilesCoordinatesToVisit: Set[Coordinates] = set()
        for blackTileCoordinates in self._blackTilesCoordinates:
            tilesCoordinatesToVisit.add(blackTileCoordinates)
            neighborTilesCoordinates = self._getNeighborTilesCoordinates(blackTileCoordinates)
            tilesCoordinatesToVisit.update(neighborTilesCoordinates)
        return tilesCoordinatesToVisit

    def _getNeighborTilesCoordinates(self, currentTileCoordinates: Coordinates) -> Set[Coordinates]:
        neighborTilesCoordinates: Set[Coordinates] = set()

        neighborTilesCoordinates.add(self._retrieveNeighbor(currentTileCoordinates, xCoordinateOffset=-2, yCoordinateOffset=0))
        neighborTilesCoordinates.add(self._retrieveNeighbor(currentTileCoordinates, xCoordinateOffset=2, yCoordinateOffset=0))

        for xCoordinateOffset in range(-1, 2, 2):
            for yCoordinateOffset in range(-1, 2, 2):
                neighborTilesCoordinates.add(self._retrieveNeighbor(currentTileCoordinates, xCoordinateOffset, yCoordinateOffset))

        assert len(neighborTilesCoordinates) == 6
        return neighborTilesCoordinates

    def _retrieveNeighbor(self, currentTileCoordinates: Coordinates, xCoordinateOffset: int, yCoordinateOffset: int) -> Coordinates:
        return Coordinates(currentTileCoordinates.x + xCoordinateOffset, currentTileCoordinates.y + yCoordinateOffset)

    def _countBlackNeighbors(self, tileCoordinates: Coordinates) -> int:
        return sum([1 for neighborTileCoordinates in self._getNeighborTilesCoordinates(tileCoordinates) if
                    neighborTileCoordinates in self._blackTilesCoordinates])

    def _processNewTileColor(self, tileCoordinates: Coordinates, blackNeighborsCount: int, blackTilesCollection: Set[Coordinates]) -> None:
        if tileCoordinates not in blackTilesCollection:
            if blackNeighborsCount == 2:
                blackTilesCollection.add(tileCoordinates)
        else:
            if blackNeighborsCount > 2 or blackNeighborsCount == 0:
                blackTilesCollection.remove(tileCoordinates)


def getFinalBlackTilesCountInExhibition(destinationPaths: List[List[Direction]], iterationCount: int) -> int:
    pathsProcessor = PathsProcessor(destinationPaths)
    pathsProcessor.processAllPaths()
    exhibitionArranger = ExhibitionArranger(pathsProcessor.getBlackTilesCoordinates())
    for _ in range(iterationCount):
        exhibitionArranger.executeIteration()
    return exhibitionArranger.getBlackTilesCount()


def main():
    destinationPaths = InputHandler.getInput(INPUT_FILE)
    pathsProcessor = PathsProcessor(destinationPaths)
    pathsProcessor.processAllPaths()
    print(pathsProcessor.getBlackTilesCount())  # 373
    print(getFinalBlackTilesCountInExhibition(destinationPaths, NUM_EXECUTION_REPETITION))  # 3917


class PathsProcessorAndExhibitionArrangerTester(unittest.TestCase):
    def setUp(self) -> None:
        self.destinationPaths = InputHandler.getInput(TEST_INPUT_FILE)

    def test_getBlackTilesCount_pathsProcessor_correctCountReturned(self):
        pathsProcessor = PathsProcessor(self.destinationPaths)
        pathsProcessor.processAllPaths()
        self.assertEqual(10, pathsProcessor.getBlackTilesCount())

    def test_getBlackTilesCount_exhibition_correctCountReturned(self):
        self.assertEqual(2208, getFinalBlackTilesCountInExhibition(self.destinationPaths, NUM_EXECUTION_REPETITION))


if __name__ == '__main__':
    # main()
    unittest.main()

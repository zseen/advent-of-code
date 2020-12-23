from typing import List, Dict, Set, Tuple
from enum import Enum
import unittest

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

BOOT_PROCESS_CYCLE_COUNT = 6
RawCoordinateNumsCollection = List[Tuple[int, int]]


class CubeStatus(Enum):
    ACTIVE = "#"
    INACTIVE = "."


class Coordinates:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __key(self):
        return (self.x, self.y, self.z)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, Coordinates):
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.z == other.z


class ConwayCubesOperator:
    def __init__(self, activeCubesCoordinates: Set[Coordinates]):
        self._activeCubesCoordinates = activeCubesCoordinates

    def getActiveCubesNum(self) -> int:
        return len(self._activeCubesCoordinates)

    def getActiveCubesInNextRound(self) -> Set[Coordinates]:
        cubesToDelete: List[Coordinates] = []
        nextRoundActiveCubes: Set[Coordinates] = set(self._activeCubesCoordinates)
        for activeCube in self._activeCubesCoordinates:
            activeNeighborsCount = self._getActiveNeighborsCount(activeCube)
            if activeNeighborsCount != 2 and activeNeighborsCount != 3:
                cubesToDelete.append(activeCube)

        for inactiveCube in self._getNeighborsOfActiveCubes():
            activeNeighborsCount = self._getActiveNeighborsCount(inactiveCube)
            if activeNeighborsCount == 3:
                nextRoundActiveCubes.add(inactiveCube)

        for cube in cubesToDelete:
            nextRoundActiveCubes.remove(cube)

        self._activeCubesCoordinates = nextRoundActiveCubes
        return self._activeCubesCoordinates

    def _getActiveNeighborsCount(self, currentCube: Coordinates) -> int:
        activeNeighborsCount = sum(
            1 for cube in self._getNeighborCubes(currentCube) if cube in self._activeCubesCoordinates)
        return activeNeighborsCount - 1 if currentCube in self._activeCubesCoordinates else activeNeighborsCount

    def _getNeighborsOfActiveCubes(self) -> Set[Coordinates]:
        cubesInTheArea: Set[Coordinates] = set()

        for activeCube in self._activeCubesCoordinates:
            neighborCubes = self._getNeighborCubes(activeCube)
            for cube in neighborCubes:
                cubesInTheArea.add(cube)

        cubesInTheArea -= self._activeCubesCoordinates
        return cubesInTheArea

    def _getNeighborCubes(self, currentCube: Coordinates) -> Set[Coordinates]:
        nearbyCubes: Set[Coordinates] = set()
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                for zOffset in range(-1, 2):
                    nearbyCubes.add(
                        Coordinates(currentCube.x + xOffset, currentCube.y + yOffset, currentCube.z + zOffset))
        return nearbyCubes


class CoordinatesPartTwo(Coordinates):
    def __init__(self, x, y, z, w):
        super().__init__(x, y, z)
        self.w = w

    def __key(self):
        return (self.x, self.y, self.z, self.w)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, Coordinates):
            return NotImplemented

        return self.x == other.x and self.y == other.y and self.z == other.z and self.w == other.w


class ConwayCubesOperatorPartTwo(ConwayCubesOperator):
    def _getNeighborCubes(self, currentCube: Coordinates) -> Set[CoordinatesPartTwo]:
        nearbyCubes: Set[CoordinatesPartTwo] = set()
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                for zOffset in range(-1, 2):
                    for wOffset in range(-1, 2):
                        nearbyCubes.add(CoordinatesPartTwo(currentCube.x + xOffset, currentCube.y + yOffset,
                                                           currentCube.z + zOffset, currentCube.w + wOffset))
        return nearbyCubes


def createCoordinatesForPartOne(coordinateNumCollection: List[Tuple[int, int]]) -> Set[Coordinates]:
    activeCubes: Set[Coordinates] = set()
    for coordinateNum in coordinateNumCollection:
        activeCubes.add(Coordinates(coordinateNum[0], coordinateNum[1], 0))
    return activeCubes


def createCoordinatesForPartTwo(coordinateNumCollection: RawCoordinateNumsCollection) -> Set[CoordinatesPartTwo]:
    activeCubes: Set[CoordinatesPartTwo] = set()
    for coordinateNum in coordinateNumCollection:
        activeCubes.add(CoordinatesPartTwo(coordinateNum[0], coordinateNum[1], 0, 0))
    return activeCubes


def getInitialActiveCubesCoordinateNums(inputFile: str) -> RawCoordinateNumsCollection:
    coordinateNumsCollection: RawCoordinateNumsCollection = []

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for j in range(len(lines)):
            for i in range(len(lines[j].strip("\n"))):
                if lines[j][i] == CubeStatus.ACTIVE.value:
                    coordinateNumsCollection.append((i, j))

    return coordinateNumsCollection


def main():
    initialActiveCubesCoordinates: RawCoordinateNumsCollection = getInitialActiveCubesCoordinateNums(INPUT_FILE)

    initialActiveCubesPartOne: Set[Coordinates] = createCoordinatesForPartOne(initialActiveCubesCoordinates)
    cubeOp = ConwayCubesOperator(initialActiveCubesPartOne)

    for i in range(0, BOOT_PROCESS_CYCLE_COUNT):
        cubeOp.getActiveCubesInNextRound()
    print(cubeOp.getActiveCubesNum())  # 353

    initialActiveCubesPartTwo: Set[CoordinatesPartTwo] = createCoordinatesForPartTwo(initialActiveCubesCoordinates)
    cubeOp = ConwayCubesOperatorPartTwo(initialActiveCubesPartTwo)

    for i in range(0, BOOT_PROCESS_CYCLE_COUNT):
        cubeOp.getActiveCubesInNextRound()
    print(cubeOp.getActiveCubesNum())  # 2472


class ActiveCubesOperationTester(unittest.TestCase):
    def test_getActiveCubesInNextRound_threeDimensionCoordinates_correctActiveCubesNumReturned(self):
        initialActiveCubesCoordinates = getInitialActiveCubesCoordinateNums(TEST_INPUT_FILE)
        initialActiveCubesPartOne = createCoordinatesForPartOne(initialActiveCubesCoordinates)
        cubeOp = ConwayCubesOperator(initialActiveCubesPartOne)

        for i in range(0, BOOT_PROCESS_CYCLE_COUNT):
            cubeOp.getActiveCubesInNextRound()

        self.assertEqual(112, cubeOp.getActiveCubesNum())

    def test_getActiveCubesInNextRound_fourDimensionCoordinates_correctActiveCubesNumReturned(self):
        initialActiveCubesCoordinates = getInitialActiveCubesCoordinateNums(TEST_INPUT_FILE)
        initialActiveCubesPartOne = createCoordinatesForPartTwo(initialActiveCubesCoordinates)
        cubeOp = ConwayCubesOperatorPartTwo(initialActiveCubesPartOne)

        for i in range(0, BOOT_PROCESS_CYCLE_COUNT):
            cubeOp.getActiveCubesInNextRound()

        self.assertEqual(848, cubeOp.getActiveCubesNum())


if __name__ == '__main__':
    # main()
    unittest.main()

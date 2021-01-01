from typing import List, Dict, Set, Tuple
from enum import Enum
import unittest
from copy import deepcopy

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

BOOT_PROCESS_CYCLE_COUNT = 6


class CubeStatus(Enum):
    ACTIVE = "#"
    INACTIVE = "."


class FourDimensionalCoordinates:
    def __init__(self, x, y, z=0, w=0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __key(self):
        return (self.x, self.y, self.z, self.w)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, FourDimensionalCoordinates):
            return NotImplemented

        return self.__key() == other.__key()


class ConwayCubesHandler:
    def __init__(self, activeCubesCoordinates: Set[FourDimensionalCoordinates]):
        self._activeCubesCoordinates = activeCubesCoordinates

    def executeBootingCycles(self, numCycles: int) -> None:
        for _ in range(0, numCycles):
            self._executeIteration()

    def getActiveCubesNum(self) -> int:
        return len(self._activeCubesCoordinates)

    def _executeIteration(self) -> None:
        nextRoundActiveCubes: Set[FourDimensionalCoordinates] = deepcopy(self._activeCubesCoordinates)
        self._deleteNoLongerActiveCubes(nextRoundActiveCubes)
        self._addNewlyActivatedCubes(nextRoundActiveCubes)
        self._activeCubesCoordinates = nextRoundActiveCubes

    def _deleteNoLongerActiveCubes(self, nextRoundActiveCubes: Set[FourDimensionalCoordinates]) -> None:
        cubesToDelete: List[Coordinates] = []
        for activeCube in self._activeCubesCoordinates:
            activeNeighborsCount = self._getActiveNeighborsCount(activeCube)
            if activeNeighborsCount != 2 and activeNeighborsCount != 3:
                cubesToDelete.append(activeCube)

        for cube in cubesToDelete:
            nextRoundActiveCubes.remove(cube)

    def _addNewlyActivatedCubes(self, nextRoundActiveCubes: Set[FourDimensionalCoordinates]) -> None:
        for inactiveCube in self._getNeighborsOfActiveCubes():
            activeNeighborsCount = self._getActiveNeighborsCount(inactiveCube)
            if activeNeighborsCount == 3:
                nextRoundActiveCubes.add(inactiveCube)

    def _getActiveNeighborsCount(self, currentCube: FourDimensionalCoordinates) -> int:
        activeNeighborsCount = sum(
            1 for cube in self._getNeighborCubes(currentCube) if cube in self._activeCubesCoordinates)
        return activeNeighborsCount - 1 if currentCube in self._activeCubesCoordinates else activeNeighborsCount

    def _getNeighborsOfActiveCubes(self) -> Set[FourDimensionalCoordinates]:
        cubesInTheArea: Set[Coordinates] = set()

        for activeCube in self._activeCubesCoordinates:
            neighborCubes = self._getNeighborCubes(activeCube)
            cubesInTheArea.update(neighborCubes)

        cubesInTheArea -= self._activeCubesCoordinates
        return cubesInTheArea

    def _getNeighborCubes(self, currentCube: FourDimensionalCoordinates) -> Set[FourDimensionalCoordinates]:
        nearbyCubes: Set[FourDimensionalCoordinates] = set()
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                for zOffset in range(-1, 2):
                    nearbyCubes.add(
                        FourDimensionalCoordinates(currentCube.x + xOffset, currentCube.y + yOffset, currentCube.z + zOffset))
        return nearbyCubes


class ConwayCubesHandlerPartTwo(ConwayCubesHandler):
    def _getNeighborCubes(self, currentCube: FourDimensionalCoordinates) -> Set[FourDimensionalCoordinates]:
        nearbyCubes: Set[CoordinatesPartTwo] = set()
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                for zOffset in range(-1, 2):
                    for wOffset in range(-1, 2):
                        nearbyCubes.add(FourDimensionalCoordinates(currentCube.x + xOffset, currentCube.y + yOffset,
                                                                   currentCube.z + zOffset, currentCube.w + wOffset))
        return nearbyCubes


def getInitialActiveCubesCoordinateNums(inputFile: str) -> Set[FourDimensionalCoordinates]:
    fourDimensionalCoordinatesCollection: Set[FourDimensionalCoordinates] = set()

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for j in range(len(lines)):
            for i in range(len(lines[j].strip("\n"))):
                if lines[j][i] == CubeStatus.ACTIVE.value:
                    fourDimensionalCoordinatesCollection.add(FourDimensionalCoordinates(i, j))

    return fourDimensionalCoordinatesCollection


def main():
    initialActiveCubes: RawCoordinateNumsCollection = getInitialActiveCubesCoordinateNums(INPUT_FILE)

    cubeHandler = ConwayCubesHandler(initialActiveCubes)
    cubeHandler.executeBootingCycles(BOOT_PROCESS_CYCLE_COUNT)
    print(cubeHandler.getActiveCubesNum())  # 353

    cubeHandler = ConwayCubesHandlerPartTwo(initialActiveCubes)
    cubeHandler.executeBootingCycles(BOOT_PROCESS_CYCLE_COUNT)
    print(cubeHandler.getActiveCubesNum())  # 2472


class ActiveCubesOperationTester(unittest.TestCase):
    def test_getActiveCubesInNextRound_threeDimensionCoordinates_correctActiveCubesNumReturned(self):
        initialActiveCubesCoordinates = getInitialActiveCubesCoordinateNums(TEST_INPUT_FILE)
        cubeHandler = ConwayCubesHandler(initialActiveCubesCoordinates)
        cubeHandler.executeBootingCycles(BOOT_PROCESS_CYCLE_COUNT)

        self.assertEqual(112, cubeHandler.getActiveCubesNum())

    def test_getActiveCubesInNextRound_fourDimensionCoordinates_correctActiveCubesNumReturned(self):
        initialActiveCubesCoordinates = getInitialActiveCubesCoordinateNums(TEST_INPUT_FILE)
        cubeHandler = ConwayCubesHandlerPartTwo(initialActiveCubesCoordinates)
        cubeHandler.executeBootingCycles(BOOT_PROCESS_CYCLE_COUNT)

        self.assertEqual(848, cubeHandler.getActiveCubesNum())


if __name__ == '__main__':
    # main()
    unittest.main()

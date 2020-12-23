from typing import List, Dict, Set
from copy import deepcopy
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"


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
        self.activeCubesCoordinates = activeCubesCoordinates

    def getActiveCubesInNextRound(self):
        cubesToDelete = []
        nextRoundActiveCubes = set(self.activeCubesCoordinates)
        for activeCube in self.activeCubesCoordinates:
            activeNeighborsCount = self.getActiveNeighborsCount(activeCube)
            #print(activeNeighborsCount)
            if activeNeighborsCount != 2 and activeNeighborsCount != 3:
                cubesToDelete.append((activeCube))

        for passiveCube in self.getNeighborsOfActiveCubes():
            activeNeighborsCount = self.getActiveNeighborsCount(passiveCube) + 1
            if activeNeighborsCount == 3:
                nextRoundActiveCubes.add(passiveCube)


        for cube in cubesToDelete:
            nextRoundActiveCubes.remove(cube)

        self.activeCubesCoordinates = nextRoundActiveCubes

        return self.activeCubesCoordinates



    def getActiveNeighborsCount(self, currentActiveCube):
        activeNeighborsCount = 0
        # 1 0 0,  0 2 0,  1 2 0
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                for zOffset in range(-1, 2):
                    for item in self.activeCubesCoordinates:
                        if  Coordinates(currentActiveCube.x + xOffset, currentActiveCube.y + yOffset, currentActiveCube.z + zOffset) == item:
                            #if Coordinates(currentActiveCube.x + xOffset, currentActiveCube.y + yOffset, currentActiveCube.z + zOffset) in self.activeCubesCoordinates:
                            activeNeighborsCount += 1


        return activeNeighborsCount - 1


    def getNeighborsOfActiveCubes(self):
        cubesInTheArea: set = set()

        for activeCube in self.activeCubesCoordinates:
            for xOffset in range(-1, 2):
                for yOffset in range(-1, 2):
                    for zOffset in range(-1, 2):
                        cubesInTheArea.add(Coordinates(activeCube.x + xOffset, activeCube.y + yOffset, activeCube.z + zOffset))

        cubesInTheArea = cubesInTheArea - self.activeCubesCoordinates
        return cubesInTheArea


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
    def getActiveNeighborsCount(self, currentActiveCube):
        activeNeighborsCount = 0
        # 1 0 0,  0 2 0,  1 2 0
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                for zOffset in range(-1, 2):
                    for wOffset in range(-1, 2):
                        if CoordinatesPartTwo(currentActiveCube.x + xOffset, currentActiveCube.y + yOffset,
                                           currentActiveCube.z + zOffset, currentActiveCube.w + wOffset) in self.activeCubesCoordinates:
                                # if Coordinates(currentActiveCube.x + xOffset, currentActiveCube.y + yOffset, currentActiveCube.z + zOffset) in self.activeCubesCoordinates:
                            activeNeighborsCount += 1

        return activeNeighborsCount - 1

    def getNeighborsOfActiveCubes(self):
        cubesInTheArea: set = set()

        for activeCube in self.activeCubesCoordinates:
            for xOffset in range(-1, 2):
                for yOffset in range(-1, 2):
                    for zOffset in range(-1, 2):
                        for wOffset in range(-1, 2):
                            cubesInTheArea.add(
                                CoordinatesPartTwo(activeCube.x + xOffset, activeCube.y + yOffset, activeCube.z + zOffset, activeCube.w + wOffset))

        cubesInTheArea = cubesInTheArea - self.activeCubesCoordinates
        return cubesInTheArea


def getInitialActiveCubes(inputFile: str):
    activeCubesPartOne: Set[Coordinates] = set()
    activeCubesPartTwo: Set[CoordinatesPartTwo] = set()

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for j in range(len(lines)):
            for i in range(len(lines[j].strip("\n"))):
                if lines[j][i] == CubeStatus.ACTIVE.value:
                    activeCubesPartOne.add(Coordinates(i, j, 0))
                    activeCubesPartTwo.add(CoordinatesPartTwo(i, j, 0, 0))


    return activeCubesPartOne, activeCubesPartTwo


initialActiveCubes = getInitialActiveCubes(INPUT_FILE)
# cubeOp = ConwayCubesOperator(initialActiveCubes[0])
#
# for i in range(0, 6):
#     print(len(cubeOp.getActiveCubesInNextRound()))


cubeOp = ConwayCubesOperatorPartTwo(initialActiveCubes[1])
for i in range(0, 6):
    print(len(cubeOp.getActiveCubesInNextRound()))








from typing import List, Dict, Set

from enum import Enum

TEST_INPUT_FILE = "test_input.txt"


class CubeStatus(Enum):
    ACTIVE = "#"
    INACTIVE = "."


class Coordinates:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class ConwayCubesOperator:
    def __init__(self, activeCubesCoordinates: Set[Coordinates]):
        self.activeCubesCoordinates = activeCubesCoordinates

    def getActiveCubesInNextRound(self):
        cubesToDelete = []
        for activeCube in self.activeCubesCoordinates:
            activeNeighborsCount = self.getActiveNeighborsCount(activeCube)
            if activeNeighborsCount != 2 or activeNeighborsCount != 3:
                cubesToDelete.append(activeCube)

        for cube in cubesToDelete:
            self.activeCubesCoordinates.remove(cube)





    def getActiveNeighborsCount(self, currentActiveCube):
        activeNeighborsCount = 0

        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                for zOffset in range(-1, 2):
                    if currentActiveCube.x + xOffset == CubeStatus.ACTIVE.value:
                        activeNeighborsCount += 1
                    if currentActiveCube.y + yOffset == CubeStatus.ACTIVE.value:
                        activeNeighborsCount += 1
                    if currentActiveCube.z + zOffset == CubeStatus.ACTIVE.value:
                        activeNeighborsCount += 1

        return activeNeighborsCount - 1


    def getActiveCubesNeighbors(self):
        cubesInTheArea: set = set()

        for activeCube in self.activeCubesCoordinates:
            for xOffset in range(-1, 2):
                for yOffset in range(-1, 2):
                    for zOffset in range(-1, 2):
                        cubesInTheArea.add(Coordinates(activeCube.x + xOffset, activeCube.y, activeCube.z))
                        cubesInTheArea.add((Coordinates(activeCube.x, activeCube.y + yOffset, activeCube.z)))
                        cubesInTheArea.add((Coordinates(activeCube.x, activeCube.y, activeCube.z + zOffset)))
        cubesInTheArea = cubesInTheArea - self.activeCubesCoordinates
        return cubesInTheArea


def getInitialActiveCubes(inputFile: str):
    activeCubes: Set[Coordinates] = set()

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for j in range(len(lines)):
            for i in range(len(lines[j].strip("\n"))):
                if lines[j][i] == CubeStatus.ACTIVE.value:
                    activeCubes.add(Coordinates(j, i, 0))

    return activeCubes


initialActiveCubes = getInitialActiveCubes(TEST_INPUT_FILE)
cubeOp = ConwayCubesOperator(initialActiveCubes)

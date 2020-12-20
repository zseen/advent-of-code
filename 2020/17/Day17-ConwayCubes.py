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
        pass

    def getActiveNeighborsCount(self):
        for xOffset in range(-1, 2):
            for yOffset in range(-1, 2):
                for zOffset in range(-1, 2):




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


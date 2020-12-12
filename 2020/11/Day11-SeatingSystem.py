import unittest
from typing import List
from enum import Enum
from copy import deepcopy

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

TOLERANCE_TRESHOLD_PART_ONE = 4
TOLERANCE_TRESHOLD_PART_TWO = 5
VISIBILITY_RANGE_PART_ONE = 1
VISIBILITY_RANGE_PART_TWO = 1000 ** 3


class Occupancy(Enum):
    EMPTY = "L"
    OCCUPIED = "#"
    FLOOR = "."


class FerrySeatingOrganizer:
    def __init__(self, grid: [[str]], toleranceThreshold: int, visibilityRange: int):
        self.grid = grid
        self.prevGrid: List[str] = []
        self.toleranceThreshold = toleranceThreshold
        self.width: int = len(grid[0]) if self.grid else 0
        self.height: int = len(grid)
        self.visibilityRange = visibilityRange

    def getNextStateGrid(self):
        nextGrid = deepcopy(self.grid)

        for j in range(0, self.height):
            for i in range(0, self.width):
                nextGrid[j][i] = self._getNextStateOfSeatOccupancy(j, i)

        self.prevGrid = self.grid
        self.grid = nextGrid

    def _getNextStateOfSeatOccupancy(self, j: int, i: int):
        if self.grid[j][i] == Occupancy.FLOOR.value:
            return Occupancy.FLOOR.value

        occupiedSeatsCount = self.countOccupiedSeatsVisibleFromSeat(j, i)

        if self.grid[j][i] == Occupancy.OCCUPIED.value:
            if occupiedSeatsCount >= self.toleranceThreshold:
                return Occupancy.EMPTY.value
        elif self.grid[j][i] == Occupancy.EMPTY.value:
            if occupiedSeatsCount == 0:
                return Occupancy.OCCUPIED.value

        return self.grid[j][i]

    def countOccupiedSeatsVisibleFromSeat(self, j: int, i: int):
        occupiedSeatsCounter = 0

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in directions:
            occupiedSeatsCounter += 1 if self.isOccupiedSeatInDirection(j, i, direction[0], direction[1]) else 0

        return occupiedSeatsCounter

    def isOccupiedSeatInDirection(self, j: int, i: int, jDirection: int, iDirection: int):
        for _ in range(self.visibilityRange):
            j += jDirection
            i += iDirection
            if self.isCoordinateOutOfBounds(j, i):
                return False
            if self.grid[j][i] == Occupancy.EMPTY.value:
                return False
            if self.grid[j][i] == Occupancy.OCCUPIED.value:
                return True
        return False

    def isCoordinateOutOfBounds(self, j: int, i: int):
        jOutBounds = j >= self.height or j < 0
        iOutBounds = i >= self.width or i < 0
        return jOutBounds or iOutBounds

    def runUntilNoChangePossible(self):
        while self.prevGrid != self.grid:
            self.getNextStateGrid()

    def countOccupiedSeatsInGrid(self):
        occupiedSeatsCount = 0
        for j in range(0, self.height):
            for i in range(0, self.width):
                if self.grid[i][j] == Occupancy.OCCUPIED.value:
                    occupiedSeatsCount += 1
        return occupiedSeatsCount


def getInput(inputFile: str):
    ferrySeatingAreaGrid = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            ferrySeatingAreaGrid.append(list(line))

    return ferrySeatingAreaGrid


def main():
    ferrySeatingPlace = getInput(INPUT_FILE)

    ferrySeating = FerrySeatingOrganizer(ferrySeatingPlace, TOLERANCE_TRESHOLD_PART_ONE, VISIBILITY_RANGE_PART_ONE)
    ferrySeating.runUntilNoChangePossible()
    print(ferrySeating.countOccupiedSeatsInGrid())  # 2470

    ferrySeatingPart2 = FerrySeatingOrganizer(ferrySeatingPlace, TOLERANCE_TRESHOLD_PART_TWO, VISIBILITY_RANGE_PART_TWO)
    ferrySeatingPart2.runUntilNoChangePossible()
    print(ferrySeatingPart2.countOccupiedSeatsInGrid())  # 2259


class FerrySeatingOrganizerTester(unittest.TestCase):
    def test_getOccupiedSeatCount_occupancyDependsOnDirectNeighbours_correctCountReturned(self):
        ferrySeatingPlace = getInput(TEST_INPUT)
        ferrySeating = FerrySeatingOrganizer(ferrySeatingPlace, TOLERANCE_TRESHOLD_PART_ONE, VISIBILITY_RANGE_PART_ONE)
        ferrySeating.runUntilNoChangePossible()
        self.assertEqual(37, ferrySeating.countOccupiedSeatsInGrid())

    def test_getOccupiedSeatCount_occupancyDependsOnRecursiveNeighbours_correctCountReturned(self):
        ferrySeatingPlace = getInput(TEST_INPUT)
        ferrySeating = FerrySeatingOrganizer(ferrySeatingPlace, TOLERANCE_TRESHOLD_PART_TWO, VISIBILITY_RANGE_PART_TWO)
        ferrySeating.runUntilNoChangePossible()
        self.assertEqual(26, ferrySeating.countOccupiedSeatsInGrid())


if __name__ == '__main__':
    # main()
    unittest.main()

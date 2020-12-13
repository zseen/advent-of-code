import unittest
from typing import List
from enum import Enum
from copy import deepcopy
import sys

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

TOLERANCE_THRESHOLD_PART_ONE = 4
TOLERANCE_THRESHOLD_PART_TWO = 5
VISIBILITY_RANGE_PART_ONE = 1
VISIBILITY_RANGE_PART_TWO = sys.maxsize

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Occupancy(Enum):
    EMPTY = "L"
    OCCUPIED = "#"
    FLOOR = "."


class FerrySeatingOrganizer:
    def __init__(self, grid: List[List[str]], toleranceThreshold: int, visibilityRange: int):
        self.grid = grid
        self.width: int = len(grid[0]) if self.grid else 0
        self.height: int = len(grid)
        self.toleranceThreshold = toleranceThreshold
        self.visibilityRange = visibilityRange

    def runUntilNoChangePossible(self):
        prevGrid = None
        while prevGrid != self.grid:
            prevGrid = self.grid
            self.grid = self._getNextStateGrid()

    def countOccupiedSeatsInGrid(self):
        occupiedSeatsCount = 0
        for j in range(0, self.height):
            for i in range(0, self.width):
                if self.grid[i][j] == Occupancy.OCCUPIED.value:
                    occupiedSeatsCount += 1
        return occupiedSeatsCount

    def _getNextStateGrid(self):
        nextGrid = deepcopy(self.grid)

        for j in range(0, self.height):
            for i in range(0, self.width):
                nextGrid[j][i] = self._getNextStateOfSeatOccupancy(i, j)

        self.grid = nextGrid
        return self.grid

    def _getNextStateOfSeatOccupancy(self, i: int, j: int):
        if self.grid[j][i] == Occupancy.FLOOR.value:
            return Occupancy.FLOOR.value

        occupiedSeatsCount = self._countOccupiedSeatsVisibleFromSeat(i, j)

        if self.grid[j][i] == Occupancy.OCCUPIED.value:
            if occupiedSeatsCount >= self.toleranceThreshold:
                return Occupancy.EMPTY.value
        elif self.grid[j][i] == Occupancy.EMPTY.value:
            if occupiedSeatsCount == 0:
                return Occupancy.OCCUPIED.value

        return self.grid[j][i]

    def _countOccupiedSeatsVisibleFromSeat(self, i: int, j: int):
        occupiedSeatsCounter = 0

        for direction in DIRECTIONS:
            occupiedSeatsCounter += 1 if self._isOccupiedSeatInDirection(i, j, direction[1], direction[0]) else 0

        return occupiedSeatsCounter

    def _isOccupiedSeatInDirection(self, i: int, j: int, xDirection: int, yDirection: int):
        for _ in range(self.visibilityRange):
            i += xDirection
            j += yDirection
            if self._isCoordinateOutOfBounds(j, i):
                return False
            if self.grid[j][i] == Occupancy.EMPTY.value:
                return False
            if self.grid[j][i] == Occupancy.OCCUPIED.value:
                return True
        return False

    def _isCoordinateOutOfBounds(self, i: int, j: int):
        jOutBounds = j >= self.height or j < 0
        iOutBounds = i >= self.width or i < 0
        return jOutBounds or iOutBounds


def getInput(inputFile: str):
    ferrySeatingAreaGrid = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            ferrySeatingAreaGrid.append(list(line))

    return ferrySeatingAreaGrid


def main():
    initialFerrySeating = getInput(INPUT_FILE)

    ferrySeatingOrganizer = FerrySeatingOrganizer(initialFerrySeating, TOLERANCE_THRESHOLD_PART_ONE,
                                                  VISIBILITY_RANGE_PART_ONE)
    ferrySeatingOrganizer.runUntilNoChangePossible()
    print(ferrySeatingOrganizer.countOccupiedSeatsInGrid())  # 2470

    ferrySeatingOrganizerPart2 = FerrySeatingOrganizer(initialFerrySeating, TOLERANCE_THRESHOLD_PART_TWO,
                                                       VISIBILITY_RANGE_PART_TWO)
    ferrySeatingOrganizerPart2.runUntilNoChangePossible()
    print(ferrySeatingOrganizerPart2.countOccupiedSeatsInGrid())  # 2259


class FerrySeatingOrganizerTester(unittest.TestCase):
    def test_getOccupiedSeatCount_occupancyDependsOnDirectNeighbours_correctCountReturned(self):
        initialFerrySeating = getInput(TEST_INPUT)
        ferrySeatingOrganizer = FerrySeatingOrganizer(initialFerrySeating, TOLERANCE_THRESHOLD_PART_ONE,
                                                      VISIBILITY_RANGE_PART_ONE)
        ferrySeatingOrganizer.runUntilNoChangePossible()
        self.assertEqual(37, ferrySeatingOrganizer.countOccupiedSeatsInGrid())

    def test_getOccupiedSeatCount_occupancyDependsOnRecursiveNeighbours_correctCountReturned(self):
        initialFerrySeating = getInput(TEST_INPUT)
        ferrySeatingOrganizer = FerrySeatingOrganizer(initialFerrySeating, TOLERANCE_THRESHOLD_PART_TWO,
                                                      VISIBILITY_RANGE_PART_TWO)
        ferrySeatingOrganizer.runUntilNoChangePossible()
        self.assertEqual(26, ferrySeatingOrganizer.countOccupiedSeatsInGrid())


if __name__ == '__main__':
    # main()
    unittest.main()

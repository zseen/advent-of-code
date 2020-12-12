import unittest
from typing import List
from occupiedSeatCounterHelper import OccupiedSeatCounter
from occupancyEnum import Occupancy
from copy import deepcopy

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

TOLERANCE_TRESHOLD_PART_ONE = 4
TOLERANCE_TRESHOLD_PART_TWO = 5
INFINITY = 100000000000000000


class FerrySeatingOrganizer:
    def __init__(self, grid: [[str]], toleranceThreshold, visibilityRange):
        self.grid = grid
        self.prevGrid: List[str] = []
        self.occupiedSeatCounter: OccupiedSeatCounter = OccupiedSeatCounter(self.grid)
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
        self.occupiedSeatCounter.grid = self.grid

    def _getNextStateOfSeatOccupancy(self, j: int, i: int):
        if self.grid[j][i] == Occupancy.FLOOR.value:
            return Occupancy.FLOOR.value


        occupiedSeatsCount = self.occupiedSeatCounter.getOccupiedSeatsVisibleFromSeatCount(j, i, self.visibilityRange)

        if self.grid[j][i] == Occupancy.OCCUPIED.value:
            if occupiedSeatsCount >= self.toleranceThreshold:
                return Occupancy.EMPTY.value
        elif self.grid[j][i] == Occupancy.EMPTY.value:
            if occupiedSeatsCount == 0:
                return Occupancy.OCCUPIED.value

        return self.grid[j][i]


    def runUntilNoChangePossible(self):
        while self.prevGrid != self.grid:
            self.getNextStateGrid()

    def getOccupiedSeatCountInGrid(self):
        return self.occupiedSeatCounter.countOccupiedSeatsInGrid()





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

    ferrySeating = FerrySeatingOrganizer(ferrySeatingPlace, TOLERANCE_TRESHOLD_PART_ONE)
    while ferrySeating.prevGrid != ferrySeating.grid:
        ferrySeating.getNextStateGrid()

    print(ferrySeating.getOccupiedSeatCountInGrid())  # 2470

    ferrySeatingPart2 = FerrySeatingOrganizer(ferrySeatingPlace, TOLERANCE_TRESHOLD_PART_TWO)
    while ferrySeatingPart2.prevGrid != ferrySeatingPart2.grid:
        ferrySeatingPart2.getNextStateGrid()

    print(ferrySeatingPart2.getOccupiedSeatCountInGrid())  # 2259


class FerrySeatingOrganizerTester(unittest.TestCase):
    def test_getOccupiedSeatCount_occupancyDependsOnDirectNeighbours_correctCountReturned(self):
        ferrySeatingPlace = getInput(TEST_INPUT)
        ferrySeating = FerrySeatingOrganizer(ferrySeatingPlace, TOLERANCE_TRESHOLD_PART_ONE, 1)
        ferrySeating.runUntilNoChangePossible()
        self.assertEqual(37, ferrySeating.getOccupiedSeatCountInGrid())

    def test_getOccupiedSeatCount_occupancyDependsOnRecursiveNeighbours_correctCountReturned(self):
        ferrySeatingPlace = getInput(TEST_INPUT)
        ferrySeating = FerrySeatingOrganizer(ferrySeatingPlace, TOLERANCE_TRESHOLD_PART_TWO, INFINITY)
        ferrySeating.runUntilNoChangePossible()
        self.assertEqual(26, ferrySeating.getOccupiedSeatCountInGrid())


if __name__ == '__main__':
    # main()
    unittest.main()

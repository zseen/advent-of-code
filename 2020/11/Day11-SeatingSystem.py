import unittest
from typing import List
from occupiedSeatCounterHelper import OccupiedSeatCounter
from occupancyEnum import Occupancy

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

TOLERANCE_TRESHOLD_PART_ONE = 4
TOLERANCE_TRESHOLD_PART_TWO = 5


class FerrySeating:
    def __init__(self, grid):
        self.grid: List[str] = grid
        self.size: int = len(grid)
        self.prevGrid: List[str] = []
        self.occupiedSeatCounter: OccupiedSeatCounter = OccupiedSeatCounter(self.grid)

    def getNextStateGrid(self, toleranceTreshold: int):
        nextGrid = createEmptyGrid(self.size)

        for j in range(0, len(self.grid[0])):
            for i in range(0, len(self.grid)):
                nextGrid[j][i] = self._getNextStateOfSeatOccupancy(j, i, toleranceTreshold)

        self.prevGrid = self.grid
        self.grid = nextGrid
        self.occupiedSeatCounter.grid = self.grid

    def _getNextStateOfSeatOccupancy(self, j: int, i: int, toleranceTreshold: int):
        if self.grid[j][i] == Occupancy.FLOOR.value:
            return Occupancy.FLOOR.value

        if toleranceTreshold == TOLERANCE_TRESHOLD_PART_ONE:
            occupiedSeatsCount = self.occupiedSeatCounter.getOccupiedNeighbourSeatsCount(j, i)
        elif toleranceTreshold == TOLERANCE_TRESHOLD_PART_TWO:
            occupiedSeatsCount = self.occupiedSeatCounter.getOccupiedSeatsVisibleFromSeat(j, i)
        else:
            raise ValueError("Bad treshold received")

        if self.grid[j][i] == Occupancy.OCCUPIED.value:
            if occupiedSeatsCount >= toleranceTreshold:
                return Occupancy.EMPTY.value
        elif self.grid[j][i] == Occupancy.EMPTY.value:
            if occupiedSeatsCount == 0:
                return Occupancy.OCCUPIED.value

        return self.grid[j][i]

    def getOccupiedSeatCountInGrid(self):
        return self.occupiedSeatCounter.countOccupiedSeatsInGrid()


def printGrid(grid):
    for subArray in grid:
        for cell in subArray:
            print(cell, end="")
        print()
    print("-----")


def createEmptyGrid(size):
    emptyGrid = []
    for j in range(0, size):
        emptyGrid.append([])
        for i in range(0, size):
            emptyGrid[j].append([])
    return emptyGrid


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

    ferrySeating = FerrySeating(ferrySeatingPlace)
    while ferrySeating.prevGrid != ferrySeating.grid:
        ferrySeating.getNextStateGrid(TOLERANCE_TRESHOLD_PART_ONE)

    print(ferrySeating.getOccupiedSeatCountInGrid())  # 2470

    ferrySeatingPart2 = FerrySeating(ferrySeatingPlace)
    while ferrySeatingPart2.prevGrid != ferrySeatingPart2.grid:
        ferrySeatingPart2.getNextStateGrid(TOLERANCE_TRESHOLD_PART_TWO)

    print(ferrySeatingPart2.getOccupiedSeatCountInGrid())  # 2259


class FerrySeatingTester(unittest.TestCase):
    def test_getOccupiedSeatCount_occupancyDependsOnDirectNeighbours_correctCountReturned(self):
        ferrySeatingPlace = getInput(TEST_INPUT)
        ferrySeating = FerrySeating(ferrySeatingPlace)
        while ferrySeating.prevGrid != ferrySeating.grid:
            ferrySeating.getNextStateGrid(TOLERANCE_TRESHOLD_PART_ONE)
        self.assertEqual(37, ferrySeating.getOccupiedSeatCountInGrid())

    def test_getOccupiedSeatCount_occupancyDependsOnRecursiveNeighbours_correctCountReturned(self):
        ferrySeatingPlace = getInput(TEST_INPUT)
        ferrySeating = FerrySeating(ferrySeatingPlace)
        while ferrySeating.prevGrid != ferrySeating.grid:
            ferrySeating.getNextStateGrid(TOLERANCE_TRESHOLD_PART_TWO)
        self.assertEqual(26, ferrySeating.getOccupiedSeatCountInGrid())


if __name__ == '__main__':
    # main()
    unittest.main()

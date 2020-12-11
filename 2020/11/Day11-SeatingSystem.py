import unittest
from typing import List
from enum import Enum



INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

TOLERANCE_TRESHOLD_PART_ONE = 4
TOLERANCE_TRESHOLD_PART_TWO = 5


class Occupancy(Enum):
    EMPTY = "L"
    OCCUPIED = "#"

class Seat:
    def __init__(self, state):
        self.state = state

class FerrySeating:
    def __init__(self, grid, size):
        self.size = size
        self.grid = grid
        self.prevGrid = None


    def getNextStateGrid(self, toleranceTreshold):
        nextGrid = createEmptyGrid(self.size)
        self.prevGrid = self.grid

        for j in range(0, len(self.grid[0])):
            for i in range(0, len(self.grid)):
                nextGrid[j][i] = self.getNextStateOfCellInPosition(j, i, toleranceTreshold)

        self.grid = nextGrid

    def getNextStateOfCellInPosition(self, j, i, toleranceTreshold: int):
        if self.grid[j][i] == ".":
            return "."

        if toleranceTreshold == TOLERANCE_TRESHOLD_PART_ONE:
            occupiedCellNeighboursCount = self.getOccupiedCellNeighboursCount(j, i)
        elif toleranceTreshold == TOLERANCE_TRESHOLD_PART_TWO:
            occupiedCellNeighboursCount = self.getOccupiedCellFirstSeenFromPositionCount(j, i)
        else:
            raise ValueError("Bad treshold received")

        if self.grid[j][i] == Occupancy.OCCUPIED.value:
            if occupiedCellNeighboursCount >= toleranceTreshold:
                return Occupancy.EMPTY.value
        elif self.grid[j][i] == Occupancy.EMPTY.value:
             if occupiedCellNeighboursCount == 0:
               return Occupancy.OCCUPIED.value

        return self.prevGrid[j][i]

    def getOccupiedCellNeighboursCount(self, j, i):
        occupiedCellNeighboursCount = 0

        for verticalOffset in range(-1, 2):
            for horizontalOffset in range(-1, 2):
                if j + verticalOffset < len(self.grid[0]) and j + verticalOffset >= 0:
                    if i + horizontalOffset < len(self.grid[0]) and i + horizontalOffset >= 0:
                        if self.grid[j + verticalOffset][i + horizontalOffset] == Occupancy.OCCUPIED.value:
                            occupiedCellNeighboursCount += 1

        if self.grid[j][i] == Occupancy.OCCUPIED.value:
            occupiedCellNeighboursCount -= 1

        return occupiedCellNeighboursCount


    def getOccupiedCellFirstSeenFromPositionCount(self, j, i):
        currentCell = self.grid[j][i]
        occupiedCellCount = 0

        # north
        rowIndex = j - 1
        while rowIndex >= 0:
            if self.grid[rowIndex][i] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][i] == Occupancy.OCCUPIED.value:
                occupiedCellCount += 1
                break
            rowIndex -= 1

        # south
        rowIndex = j + 1
        while rowIndex < self.size:
            if self.grid[rowIndex][i] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][i] == Occupancy.OCCUPIED.value:
                occupiedCellCount += 1
                break
            rowIndex += 1

        # east
        columnIndex = i + 1
        while columnIndex < self.size:
            if self.grid[j][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[j][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedCellCount += 1
                break
            columnIndex += 1

        # west
        columnIndex = i - 1
        while columnIndex >= 0:
            if self.grid[j][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[j][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedCellCount += 1
                break
            columnIndex -= 1

        # northwest
        rowIndex = j - 1
        columnIndex = i - 1
        while rowIndex >= 0 and columnIndex >= 0 :
            if self.grid[rowIndex][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedCellCount += 1
                break
            rowIndex -= 1
            columnIndex -= 1

        # northeast
        rowIndex = j -1
        columnIndex = i + 1
        while rowIndex >= 0 and columnIndex < self.size:
            if self.grid[rowIndex][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedCellCount += 1
                break
            rowIndex -= 1
            columnIndex += 1

        # southwest
        rowIndex = j + 1
        columnIndex = i - 1
        while rowIndex < self.size and columnIndex >= 0:
            if self.grid[rowIndex][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedCellCount += 1
                break
            rowIndex += 1
            columnIndex -= 1

        # southeast
        rowIndex = j + 1
        columnIndex = i + 1
        while rowIndex < self.size and columnIndex < self.size:
            if self.grid[rowIndex][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedCellCount += 1
                break
            rowIndex += 1
            columnIndex += 1




        return occupiedCellCount


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


def getOccupiedSeatCountInGrid(grid):
    occupiedCount = 0
    for j in range(0, len(grid)):
        for i in range(0, len(grid[j])):
            if grid[i][j] == Occupancy.OCCUPIED.value:
                occupiedCount += 1
    return occupiedCount


def getInput(inputFile: str):
    ferrySeatingAreaGrid = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            ferrySeatingAreaGrid.append(list(line))

    return ferrySeatingAreaGrid, len(ferrySeatingAreaGrid)



# area = getInput(TEST_INPUT)
#
# secondFerrySeating = FerrySeating(area[0], area[1])
# #
# # for i in range(0, 5):
# #     secondFerrySeating.getNextStateGrid(TOLERANCE_TRESHOLD_PART_TWO)
#
#
#
# #printGrid(secondFerrySeating.grid)
#
# while secondFerrySeating.prevGrid != secondFerrySeating.grid:
#     secondFerrySeating.getNextStateGrid(TOLERANCE_TRESHOLD_PART_TWO)
#
# # printGrid(secondFerrySeating.grid)
#
# occ = getOccupiedSeatCountInGrid(secondFerrySeating.grid)
# print(occ)



mainRun = getInput(INPUT_FILE)
mainFerrySeating = FerrySeating(mainRun[0], mainRun[1])

while mainFerrySeating.prevGrid != mainFerrySeating.grid:
    mainFerrySeating.getNextStateGrid(TOLERANCE_TRESHOLD_PART_TWO)

occ = getOccupiedSeatCountInGrid(mainFerrySeating.grid)
print(occ)








# --------------- Part1 -------------------------------------
# gol = FerrySeating(area[0], area[1])
# for i in range(0, 5):
#     gol.getNextStateGrid(TOLERANCE_TRESHOLD_PART_ONE)
# testGridLast =["#.#L.L#.##",
# "#LLL#LL.L#",
# "L.#.L..#..",
# "#L##.##.L#",
# "#.#L.LL.LL",
# "#.#L#L#.##",
# "..L.L.....",
# "#L#L##L#L#",
# "#.LLLLLL.L",
# "#.#L#L#.##"]
#
# tl = []
# for row in testGridLast:
#     tl.append(list(row))
#
#
# print(gol.grid == tl)
#
#
# occ = getOccupiedSeatCountInGrid(gol.grid)
# print(occ)

# mainGrid = getInput(INPUT_FILE)
# ferrySeating = FerrySeating(mainGrid[0], mainGrid[1])
#
# while ferrySeating.grid != ferrySeating.prevGrid:
#     ferrySeating.getNextStateGrid(TOLERANCE_TRESHOLD_PART_ONE)

# print(getOccupiedSeatCountInGrid(ferrySeating.grid)) 2470



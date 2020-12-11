import unittest
from typing import List
from enum import Enum



INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"


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


    def getNextStateGrid(self):
        nextGrid = createEmptyGrid(self.size)
        self.prevGrid = self.grid

        for j in range(0, len(self.grid[0])):
            for i in range(0, len(self.grid)):
                nextGrid[j][i] = self.getNextStateOfCellInPosition(j, i)

        self.grid = nextGrid

    def getNextStateOfCellInPosition(self, j, i):
        if self.grid[j][i] == ".":
            return "."
        occupiedCellNeighboursCount = self.getOccupiedCellNeighboursCount(j, i)

        if self.grid[j][i] == Occupancy.OCCUPIED.value:
            if occupiedCellNeighboursCount >= 4:
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



area = getInput(TEST_INPUT)
gol = FerrySeating(area[0], area[1])


for i in range(0, 5):
    gol.getNextStateGrid()


testGridLast =["#.#L.L#.##",
"#LLL#LL.L#",
"L.#.L..#..",
"#L##.##.L#",
"#.#L.LL.LL",
"#.#L#L#.##",
"..L.L.....",
"#L#L##L#L#",
"#.LLLLLL.L",
"#.#L#L#.##"]

tl = []
for row in testGridLast:
    tl.append(list(row))


print(gol.grid == tl)


occ = getOccupiedSeatCountInGrid(gol.grid)
print(occ)

mainGrid = getInput(INPUT_FILE)
ferrySeating = FerrySeating(mainGrid[0], mainGrid[1])

while ferrySeating.grid != ferrySeating.prevGrid:
    ferrySeating.getNextStateGrid()

print(getOccupiedSeatCountInGrid(ferrySeating.grid))



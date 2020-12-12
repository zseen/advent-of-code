from occupancyEnum import Occupancy


class OccupiedSeatCounter:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)

    def getOccupiedNeighbourSeatsCount(self, j, i):
        northNeighbourRowIndex = None if j == 0 else j - 1
        southNeighbourRowIndex = None if j == self.size - 1 else j + 1
        westNeighbourColumnIndex = None if i == 0 else i - 1
        eastNeighbourColumnIndex = None if i == self.size - 1 else i + 1

        occupiedSeatsCount = 0

        if northNeighbourRowIndex is not None:
            if self.grid[northNeighbourRowIndex][i] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1
            if westNeighbourColumnIndex is not None:
                if self.grid[northNeighbourRowIndex][westNeighbourColumnIndex] == Occupancy.OCCUPIED.value:
                    occupiedSeatsCount += 1
            if eastNeighbourColumnIndex is not None:
                if self.grid[northNeighbourRowIndex][eastNeighbourColumnIndex] == Occupancy.OCCUPIED.value:
                    occupiedSeatsCount += 1
        if southNeighbourRowIndex is not None:
            if self.grid[southNeighbourRowIndex][i] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1
            if westNeighbourColumnIndex is not None:
                if self.grid[southNeighbourRowIndex][westNeighbourColumnIndex] == Occupancy.OCCUPIED.value:
                    occupiedSeatsCount += 1
            if eastNeighbourColumnIndex != None:
                if self.grid[southNeighbourRowIndex][eastNeighbourColumnIndex] == Occupancy.OCCUPIED.value:
                    occupiedSeatsCount += 1
        if westNeighbourColumnIndex is not None:
            if self.grid[j][westNeighbourColumnIndex] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1

        if eastNeighbourColumnIndex is not None:
            if self.grid[j][eastNeighbourColumnIndex] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1

        return occupiedSeatsCount

    def getOccupiedSeatsVisibleFromSeat(self, j, i):
        occupiedSeatsCount = 0

        # north
        rowIndex = j - 1
        while rowIndex >= 0:
            if self.grid[rowIndex][i] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][i] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1
                break
            rowIndex -= 1

        # south
        rowIndex = j + 1
        while rowIndex < self.size:
            if self.grid[rowIndex][i] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][i] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1
                break
            rowIndex += 1

        # east
        columnIndex = i + 1
        while columnIndex < self.size:
            if self.grid[j][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[j][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1
                break
            columnIndex += 1

        # west
        columnIndex = i - 1
        while columnIndex >= 0:
            if self.grid[j][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[j][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1
                break
            columnIndex -= 1

        # northwest
        rowIndex = j - 1
        columnIndex = i - 1
        while rowIndex >= 0 and columnIndex >= 0:
            if self.grid[rowIndex][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1
                break
            rowIndex -= 1
            columnIndex -= 1

        # northeast
        rowIndex = j - 1
        columnIndex = i + 1
        while rowIndex >= 0 and columnIndex < self.size:
            if self.grid[rowIndex][columnIndex] == Occupancy.EMPTY.value:
                break
            if self.grid[rowIndex][columnIndex] == Occupancy.OCCUPIED.value:
                occupiedSeatsCount += 1
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
                occupiedSeatsCount += 1
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
                occupiedSeatsCount += 1
                break
            rowIndex += 1
            columnIndex += 1

        return occupiedSeatsCount

    def countOccupiedSeatsInGrid(self):
        occupiedSeatsCount = 0
        for j in range(0, self.size):
            for i in range(0, self.size):
                if self.grid[i][j] == Occupancy.OCCUPIED.value:
                    occupiedSeatsCount += 1
        return occupiedSeatsCount

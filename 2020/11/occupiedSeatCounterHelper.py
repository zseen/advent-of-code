from occupancyEnum import Occupancy


class Coordinates:
    def __init__(self, x, y):
        self.x = x
        self.y = y





class OccupiedSeatCounter:
    def __init__(self, grid):
        self.grid = grid
        self.size = len(grid)
        self.heigtht = len(self.grid)
        self.width = len(self.grid[0]) if self.grid else 0


    def getOccupiedNeighbourSeatsCount(self, j, i):
        occupiedNeighboursCount = 0

        for verticalOffset in range(-1, 2):
            for horizontalOffset in range(-1, 2):
                if self.size > j + verticalOffset >= 0:
                    if self.size > i + horizontalOffset >= 0:
                        if self.grid[j + verticalOffset][i + horizontalOffset] == Occupancy.OCCUPIED.value:
                            occupiedNeighboursCount += 1

        if self.grid[j][i] == Occupancy.OCCUPIED.value:
            occupiedNeighboursCount -= 1

        return occupiedNeighboursCount





    def getOccupiedSeatsVisibleFromSeatCount(self, j, i, visibilityRange):
        oc = 0

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for direction in directions:
            oc += 1 if self.isOccInDir(j, i, direction[0], direction[1], visibilityRange) else 0

        return oc


    def isOccInDir(self, ystart, xstart, xdelta, ydelta, visibilityRange):
        for i in range(visibilityRange):
            xstart += xdelta
            ystart += ydelta
            if  self.isCoordinateOutOfBounds(ystart, xstart):
                return False

            if self.grid[ystart][xstart] == Occupancy.EMPTY.value:
                return False
            if self.grid[ystart][xstart] == Occupancy.OCCUPIED.value:
                return True
        return False


    def isCoordinateOutOfBounds(self, j, i):
        if j >= self.heigtht or j < 0:
            return True
        if i >= self.width or i < 0:
            return True
        return False






    def getOccupiedSeatsVisibleFromSeat2(self, j, i):
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

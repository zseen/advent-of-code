import unittest
from enum import Enum
from typing import List


INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

ROWS_NUM = 128
COLUMNS_NUM = 8


class Positions(Enum):
    FRONT_ROW = "F"
    BACK_ROW = "B"
    UPPER_COLUMN = "R"
    LOWER_COLUMN = "L"

class Seat:
    def __init__(self, seatDirections):
        self.seatDirections: str = seatDirections
        self.row = self.getRowNum()
        self.column = self.getColumnNum()
        self.seatID = self.getSeatID()

    def getRowNum(self):
        currentRowsNumUpperBound = ROWS_NUM - 1
        currentRowsNumLowerBound = 0
        if not self.seatDirections:
            raise ValueError("Seat directions is missing")

        seatDirectionForRow = self.seatDirections[:len(self.seatDirections) - 3]

        for char in seatDirectionForRow:
            middle = (currentRowsNumUpperBound + currentRowsNumLowerBound) // 2
            if char == Positions.FRONT_ROW.value:
                currentRowsNumUpperBound = middle
            elif char == Positions.BACK_ROW.value:
                currentRowsNumLowerBound = middle + 1

        if currentRowsNumLowerBound != currentRowsNumUpperBound:
            raise ValueError("Problem with searching for the row number")

        return currentRowsNumLowerBound

    def getColumnNum(self):
        currentColumnsNumUpperBound = COLUMNS_NUM - 1
        currentColumnsNumLowerBound = 0
        if not self.seatDirections:
            raise ValueError("Seat directions is missing")

        seatDirectionForColumn = self.seatDirections[len(self.seatDirections) - 3:]

        for char in seatDirectionForColumn:
            middle = (currentColumnsNumUpperBound + currentColumnsNumLowerBound) // 2
            if char == Positions.UPPER_COLUMN.value:
                currentColumnsNumLowerBound = middle + 1
            elif char == Positions.LOWER_COLUMN.value:
                currentColumnsNumUpperBound = middle

        if currentColumnsNumLowerBound != currentColumnsNumUpperBound:
            raise ValueError("Problem with searching for the column number")

        return currentColumnsNumLowerBound

    def getSeatID(self):
        if self.row is None:
            raise ValueError("Missing data for row")

        if self.column is None:
            print(self.seatDirections)
            raise ValueError("Missing data column")

        return  self.row * 8 + self.column


def getInput(inputFile):
    allSeatsDirections = []

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            allSeatsDirections.append(line)
    return allSeatsDirections

def getHighestSeatID(allSeats):
    currentMaxSeatID = 0
    for seat in allSeats:
        if seat.seatID > currentMaxSeatID:
            currentMaxSeatID = seat.seatID
    return currentMaxSeatID

def getAllSeats(allSeatsDirections: List):
    allSeats = []
    for seatDirection in allSeatsDirections:
        allSeats.append(Seat(seatDirection))
    return allSeats

def main():
    allSeatsDirections = getInput(INPUT_FILE)
    #FFFBBBFLLL
    print(getHighestSeatID(getAllSeats(allSeatsDirections)))
    # s = Seat("FFFBBBFLLL")
    # print(s.seatID)


if __name__ == '__main__':
    main()

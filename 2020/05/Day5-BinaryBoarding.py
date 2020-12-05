import unittest
from enum import Enum
from typing import List

INPUT_FILE = "input.txt"
SHORT_INPUT_FILE = "short_input.txt"

ROWS_NUM = 128
COLUMNS_NUM = 8


class Positions(Enum):
    FRONT_ROW = "F"
    BACK_ROW = "B"
    LEFT = "L"
    RIGHT = "R"


class Seat:
    def __init__(self, seatDirections):
        self.seatDirections: str = seatDirections
        self.row = self.calculateRowNum()
        self.column = self.calculateColumnNum()
        self.seatID = self.calculateSeatID()

    def calculateRowNum(self):
        currentRowsNumUpperBound = ROWS_NUM - 1
        currentRowsNumLowerBound = 0
        if not self.seatDirections:
            raise ValueError("Seat directions is missing")

        seatDirectionForRow = self.seatDirections[:len(self.seatDirections) - 3]

        # Positions ascend from FRONT_ROW to BACK_ROW
        for char in seatDirectionForRow:
            middle = (currentRowsNumUpperBound + currentRowsNumLowerBound) // 2
            if char == Positions.FRONT_ROW.value:
                currentRowsNumUpperBound = middle
            elif char == Positions.BACK_ROW.value:
                currentRowsNumLowerBound = middle + 1

        if currentRowsNumLowerBound != currentRowsNumUpperBound:
            raise ValueError("Problem with searching for the row number")

        return currentRowsNumLowerBound

    def calculateColumnNum(self):
        currentColumnsNumUpperBound = COLUMNS_NUM - 1
        currentColumnsNumLowerBound = 0
        if not self.seatDirections:
            raise ValueError("Seat directions is missing")

        seatDirectionForColumn = self.seatDirections[len(self.seatDirections) - 3:]

        # Positions ascend from LEFT to RIGHT
        for char in seatDirectionForColumn:
            middle = (currentColumnsNumUpperBound + currentColumnsNumLowerBound) // 2
            if char == Positions.LEFT.value:
                currentColumnsNumUpperBound = middle
            elif char == Positions.RIGHT.value:
                currentColumnsNumLowerBound = middle + 1

        if currentColumnsNumLowerBound != currentColumnsNumUpperBound:
            raise ValueError("Problem with searching for the column number")

        return currentColumnsNumLowerBound

    def calculateSeatID(self):
        if self.row is None:
            raise ValueError("Missing data for row")

        if self.column is None:
            raise ValueError("Missing data for column")

        return self.row * 8 + self.column


def getInput(inputFile):
    allSeatsDirections = []

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            allSeatsDirections.append(line)
    return allSeatsDirections


def getHighestSeatID(allSeatsIDS: List[int]):
    return max(allSeatsIDS)


def getAllSeats(allSeatsDirections: List):
    validSeats = [Seat(seatDirections) for seatDirections in allSeatsDirections if len(seatDirections) == 10]
    if len(validSeats) != len(allSeatsDirections):
        raise ValueError("Double check seat directions format!")
    return validSeats


def getAllSeatIDs(allseats: List):
    return [seat.seatID for seat in allseats]


def findMissingSeatID(allSeatIDs: List[int]):
    smallestSeatID = min(allSeatIDs)
    allSeatIDsSet = set(allSeatIDs)

    while True:
        if smallestSeatID + 1 not in allSeatIDsSet:
            return smallestSeatID + 1
        smallestSeatID += 1


def main():
    allSeatsDirections = getInput(INPUT_FILE)
    allSeats = getAllSeats(allSeatsDirections)
    print(getHighestSeatID(getAllSeatIDs(allSeats)))  # 980
    print(findMissingSeatID(getAllSeatIDs(allSeats)))  # 607


class SeatIDsTester(unittest.TestCase):
    def test_getHighestSeatID_shortInput_highestSeatIDReturned(self):
        allSeatsDirections = getInput(SHORT_INPUT_FILE)
        self.assertEqual(820, getHighestSeatID(getAllSeatIDs(getAllSeats(allSeatsDirections))))

    def test_getHighestSeatID_originalLongInput_highestSeatIDReturned(self):
        allSeatsDirections = getInput(INPUT_FILE)
        self.assertEqual(980, getHighestSeatID(getAllSeatIDs(getAllSeats(allSeatsDirections))))

    def test_findMissingSeatID_originalLongInput_missingSeatIDReturned(self):
        allSeatsDirections = getInput(INPUT_FILE)
        self.assertEqual(607, findMissingSeatID(getAllSeatIDs(getAllSeats(allSeatsDirections))))


if __name__ == '__main__':
    # main()
    unittest.main()

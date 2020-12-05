import unittest
from enum import Enum
from typing import List

INPUT_FILE = "input.txt"
SHORT_INPUT_FILE = "short_input.txt"

NUM_ROWS = 128
NUM_COLUMNS = 8


class RowPositions(Enum):
    FRONT_ROW = "F"
    BACK_ROW = "B"


class ColumnPositions(Enum):
    LEFT = "L"
    RIGHT = "R"


class Seat:
    def __init__(self, seatDirections):
        self.seatDirections: str = seatDirections
        self.row = self.calculateRowNum()
        self.column = self.calculateColumnNum()
        self.seatID = self.calculateSeatID()

    def calculateRowNum(self):
        rowInformation = self.seatDirections[:len(self.seatDirections) - 3]
        return self._findPosition(rowInformation, 0, NUM_ROWS - 1, RowPositions.FRONT_ROW, RowPositions.BACK_ROW)

    def calculateColumnNum(self):
        columnInformation = self.seatDirections[len(self.seatDirections) - 3:]

        return self._findPosition(columnInformation, 0, NUM_COLUMNS - 1, ColumnPositions.LEFT, ColumnPositions.RIGHT)

    def calculateSeatID(self):
        if self.row is None:
            raise ValueError("Missing data for row")

        if self.column is None:
            raise ValueError("Missing data for column")

        return self.row * 8 + self.column

    @staticmethod
    def _findPosition(directions, lowerBound, upperBound, validDirectionSmaller, validDirectionGreater):
        if not directions:
            raise ValueError("Seat directions is missing")

        for direction in directions:
            middle = (upperBound + lowerBound) // 2
            if direction == validDirectionSmaller.value:
                upperBound = middle
            elif direction == validDirectionGreater.value:
                lowerBound = middle + 1

        if lowerBound != upperBound:
            raise ValueError("Problem with searching for the seat location")

        return lowerBound


def getInput(inputFile):
    allSeatsDirections = []

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            allSeatsDirections.append(line)
    return allSeatsDirections


def getAllSeats(allSeatsDirections: List):
    validSeats = [Seat(seatDirections) for seatDirections in allSeatsDirections if len(seatDirections) == 10]
    if len(validSeats) != len(allSeatsDirections):
        raise ValueError("Double check seat directions format!")
    return validSeats


def getAllSeatIDs(allseats: List):
    return [seat.seatID for seat in allseats]


def findMissingSeatID(allSeatIDs: List[int]):
    possibleMissingSeatID = min(allSeatIDs) + 1
    allSeatIDsSet = set(allSeatIDs)

    while True:
        if possibleMissingSeatID not in allSeatIDsSet:
            return possibleMissingSeatID
        possibleMissingSeatID += 1


def main():
    allSeatsDirections = getInput(INPUT_FILE)
    allSeats = getAllSeats(allSeatsDirections)
    allSeatIDs = getAllSeatIDs(allSeats)
    print(max(allSeatIDs))  # 980
    print(findMissingSeatID(allSeatIDs))  # 607


class SeatIDsTester(unittest.TestCase):
    def test_getHighestSeatID_shortInput_highestSeatIDReturned(self):
        allSeatsDirections = getInput(SHORT_INPUT_FILE)
        self.assertEqual(820, max(getAllSeatIDs(getAllSeats(allSeatsDirections))))

    def test_getHighestSeatID_originalLongInput_highestSeatIDReturned(self):
        allSeatsDirections = getInput(INPUT_FILE)
        self.assertEqual(980, max(getAllSeatIDs(getAllSeats(allSeatsDirections))))

    def test_findMissingSeatID_originalLongInput_missingSeatIDReturned(self):
        allSeatsDirections = getInput(INPUT_FILE)
        self.assertEqual(607, findMissingSeatID(getAllSeatIDs(getAllSeats(allSeatsDirections))))


if __name__ == '__main__':
    # main()
    unittest.main()

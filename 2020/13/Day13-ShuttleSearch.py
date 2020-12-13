import unittest
from typing import List
import sys

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

class ShuttleBusOperation:
    def __init__(self, earliestTimestamp: int, busIDs: List ):
        self.earliestTimestamp = earliestTimestamp
        self.busIDs = busIDs

    def getEarliestSuitableBusID(self):
        busIDtoTimeDifference = dict()
        for busId in self.busIDs:
            currentDivisionResult = self.earliestTimestamp // busId
            if currentDivisionResult * busId == self.earliestTimestamp:
                return busId
            else:
                busIDtoTimeDifference[busId] = (currentDivisionResult + 1) * busId - self.earliestTimestamp

        minDifference = sys.maxsize
        busIdWithLeastTimeDifference = None
        for id, timeDifference in busIDtoTimeDifference.items():
            if timeDifference < minDifference:
                minDifference = timeDifference
                busIdWithLeastTimeDifference = id

        return busIdWithLeastTimeDifference * minDifference



def getNotes(inputFile: str):
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        if len(lines) > 1:
            busIDs = lines[1].strip("\n").split(",")
            validBusIDs = [int(busID) for busID in busIDs if busID.isnumeric()]
            return ShuttleBusOperation(int(lines[0].strip("\n")), validBusIDs)
        raise ValueError("Doublecheck the input format.")


sb = getNotes(INPUT_FILE)
print(sb.getEarliestSuitableBusID())
import unittest
from typing import List, Dict
import sys

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

class ShuttleBusFinder:
    def __init__(self, earliestTimestamp: int, busIDs: List[int]):
        self.earliestTimestamp = earliestTimestamp
        self.busIDs = busIDs

    def getEarliestSuitableBusID(self):
        busIDToWaitTime = dict()
        for busID in self.busIDs:
            currentDivisionResult = self.earliestTimestamp // busID
            if currentDivisionResult * busID == self.earliestTimestamp:
                return busID * 0 # The busID * waitTime should be returned, in this case the waitTime is 0
            else:
                busIDToWaitTime[busID] = (currentDivisionResult + 1) * busID - self.earliestTimestamp

        minWaitTime = sys.maxsize
        busIDWithLeastWaitTime = None
        for busID, waitTime in busIDToWaitTime.items():
            if waitTime < minWaitTime:
                minWaitTime = waitTime
                busIDWithLeastWaitTime = busID

        return busIDWithLeastWaitTime * minWaitTime

def getShuttleBusFinder(inputFile: str):
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        if len(lines) > 1:
            busIDs = lines[1].strip("\n").split(",")
            validBusIDs = [int(busID) for busID in busIDs if busID.isnumeric()]
            return ShuttleBusFinder(int(lines[0].strip("\n")), validBusIDs)
        raise ValueError("Doublecheck the input format.")


class EarliestTimestampFinder:
    def __init__(self, busIDToOffset: Dict[int, int], timestamps: List[int]):
        self.busIDToOffset = busIDToOffset
        self.timestamps = timestamps

    def getEarliestTimestampBusesArriveInOffsetOrder(self):
        if not self.timestamps:
            raise ValueError("No timestamps.")

        jump = self.timestamps[0]
        currentTimestamp = self.timestamps[0]

        for i in range(1, len(self.timestamps)):
            nextTimestamp = self.timestamps[i]
            while (currentTimestamp + self.busIDToOffset[nextTimestamp]) % nextTimestamp != 0:
                currentTimestamp += jump
            jump *= nextTimestamp

        return currentTimestamp

def getEarliestTimestampFinder(inputFile: str):
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        if len(lines) > 1:
            busIDs = lines[1].strip("\n").split(",")
            validBusIDs = [int(busID) for busID in busIDs if busID.isnumeric()]
            busIdToOffset = dict()
            busIdOffset = 0
            while busIdOffset != len(busIDs):
                if busIDs[busIdOffset].isnumeric():
                    busIdToOffset[int(busIDs[busIdOffset])] = busIdOffset
                busIdOffset += 1

            return EarliestTimestampFinder(busIdToOffset, validBusIDs)


        raise ValueError("Doublecheck the input format.")



def main():
    shuttleBusFinder = getShuttleBusFinder(INPUT_FILE)
    print(shuttleBusFinder.getEarliestSuitableBusID()) # 3035

    earliestTimestampFinder = getEarliestTimestampFinder(INPUT_FILE)
    print(earliestTimestampFinder.getEarliestTimestampBusesArriveInOffsetOrder()) #725169163285238

if __name__ == '__main__':
    main()
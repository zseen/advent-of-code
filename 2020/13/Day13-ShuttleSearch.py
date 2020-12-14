import unittest
from typing import List, Dict
import sys

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

class ShuttleBusFinder:
    def __init__(self, earliestTimestamp: int, busIDs: List[str]):
        self.earliestTimestamp = earliestTimestamp
        self.busIDs = [int(busID) for busID in busIDs if busID.isnumeric()]

    def getEarliestSuitableBusIDAndWaitTimeProduct(self):
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


class EarliestTimestampFinder:
    def __init__(self, busIDs: List[str]):
        self.busIDs = busIDs
        self.busIDToOffset: Dict[int, int] = self.getBusIDsToOffset()
        self.timestamps = [int(busID) for busID in busIDs if busID.isnumeric()]

    def getBusIDsToOffset(self):
        busIDsToOffset = dict()
        busIDOffset = 0
        while busIDOffset != len(self.busIDs):
            if self.busIDs[busIDOffset].isnumeric():
                busIDsToOffset[int(self.busIDs[busIDOffset])] = busIDOffset
            busIDOffset += 1
        return busIDsToOffset

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



def getTimestampAndBusIDs(inputFile: str):
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        if len(lines) > 1:
            return (int(lines[0].strip("\n")), lines[1].strip("\n").split(","))

        raise ValueError("Doublecheck the input format.")


def main():
    timestamp, busIDs = getTimestampAndBusIDs(INPUT_FILE)

    shuttleBusFinder = ShuttleBusFinder(timestamp, busIDs)
    print(shuttleBusFinder.getEarliestSuitableBusIDAndWaitTimeProduct()) # 3035

    earliestTimestampFinder = EarliestTimestampFinder(busIDs)
    print(earliestTimestampFinder.getEarliestTimestampBusesArriveInOffsetOrder()) #725169163285238

class ShuttleBusTimesTester(unittest.TestCase):
    def test_getEarliestSuitableBusIDAndWaitTimeProduct_noBusToArriveAtExactTimestamp_correctClosestBusAndWaitTimeProductReturned(self):
        timestamp, busIDs = getTimestampAndBusIDs(TEST_INPUT)
        shuttleBusFinder = ShuttleBusFinder(timestamp, busIDs)
        self.assertEqual(295, shuttleBusFinder.getEarliestSuitableBusIDAndWaitTimeProduct())

    def test_getEarliestTimestampBusesArriveInOffsetOrder_setTimestampInInputNotNeeded_correctTimestampReturned(self):
        timestamp, busIDs = getTimestampAndBusIDs(TEST_INPUT)
        earliestTimestampFinder = EarliestTimestampFinder(busIDs)
        self.assertEqual(1068781, earliestTimestampFinder.getEarliestTimestampBusesArriveInOffsetOrder())


if __name__ == '__main__':
    main()
    unittest.main()
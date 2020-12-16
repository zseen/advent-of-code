import unittest
from typing import List, Dict, Tuple
import sys

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"


def getEarliestSuitableBusIDAndWaitTimeProduct(earliestTimestamp: int, busIDs: List[int]) -> int:
    minWaitTime: int = sys.maxsize
    busIDWithLeastWaitTime: int = 0

    for busID in busIDs:
        currentWaitTime = getCurrentWaitTime(earliestTimestamp, busID)
        if currentWaitTime < minWaitTime:
            minWaitTime = currentWaitTime
            busIDWithLeastWaitTime = busID

    return busIDWithLeastWaitTime * minWaitTime


def getCurrentWaitTime(earliestTimestamp: int, busID: int) -> int:
    currentDivisionResult = earliestTimestamp // busID
    if currentDivisionResult * busID == earliestTimestamp:
        return 0

    return (currentDivisionResult + 1) * busID - earliestTimestamp



class EarliestTimestampFinder:
    def __init__(self, busIDToOffset: Dict[int, int]):
        self.busIDToOffset = busIDToOffset

    def getEarliestTimestampBusesArriveInOffsetOrder(self) -> int:
        timestamps: List[int] = list(self.busIDToOffset.keys())
        if not timestamps:
            raise ValueError("No timestamps.")

        jump = timestamps[0]
        currentTimestamp = timestamps[0]

        for i in range(1, len(timestamps)):
            nextTimestamp = timestamps[i]
            while (currentTimestamp + self.busIDToOffset[nextTimestamp]) % nextTimestamp != 0:
                currentTimestamp += jump
            jump *= nextTimestamp

        return currentTimestamp


def getBusIDsToOffset(busIDs: List[str]) -> Dict[int, int]:
    busIDsToOffset: Dict[int, int] = dict()
    for offset in range(0, len(busIDs)):
        if busIDs[offset].isnumeric():
            busIDsToOffset[int(busIDs[offset])] = offset
    return busIDsToOffset


def getValidBusIDs(busIDs) -> List[int]:
    return [int(busID) for busID in busIDs if busID.isnumeric()]


def getTimestampAndBusIDs(inputFile: str) -> Tuple[int, List[str]]:
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        if len(lines) > 1:
            return int(lines[0].strip("\n")), lines[1].strip("\n").split(",")

        raise ValueError("Double check the input format.")


def main():
    timestamp, busIDs = getTimestampAndBusIDs(INPUT_FILE)

    earliestBusAndWaitTimeProduct = getEarliestSuitableBusIDAndWaitTimeProduct(timestamp, getValidBusIDs(busIDs))
    print(earliestBusAndWaitTimeProduct)  # 3035

    earliestTimestampFinder = EarliestTimestampFinder(getBusIDsToOffset(busIDs))
    print(earliestTimestampFinder.getEarliestTimestampBusesArriveInOffsetOrder())  # 725169163285238


class ShuttleBusTimesTester(unittest.TestCase):
    def test_getEarliestSuitableBusIDAndWaitTimeProduct_noBusToArriveAtExactTimestamp_correctClosestBusAndWaitTimeProductReturned(
            self):
        timestamp, busIDs = getTimestampAndBusIDs(TEST_INPUT)
        self.assertEqual(295, getEarliestSuitableBusIDAndWaitTimeProduct(timestamp, getValidBusIDs(busIDs)))

    def test_getEarliestTimestampBusesArriveInOffsetOrder_setTimestampInInputNotNeeded_correctTimestampReturned(self):
        timestamp, busIDs = getTimestampAndBusIDs(TEST_INPUT)
        earliestTimestampFinder = EarliestTimestampFinder(getBusIDsToOffset(busIDs))
        self.assertEqual(1068781, earliestTimestampFinder.getEarliestTimestampBusesArriveInOffsetOrder())


if __name__ == '__main__':
    # main()
    unittest.main()

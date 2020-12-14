import unittest
from typing import List, Dict
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

class EarliestTimestampFinder:
    def __init__(self, busIDToOffset: Dict[int, int], timestamps):
        self.busIDToOffset = busIDToOffset
        self.timeStamps = timestamps



    def getEarliestTimestampBusesArriveAtOffsetPosition2(self):
        for num in range(100000000000000, 1000000000000000000000000000000000000):
            isNumPossible = True
            for offset, busID in self.offsetToBusID.items():
                if (num + offset) % busID != 0:
                    isNumPossible = False

            if isNumPossible:
                return num

    def getEarliestTimestampBusesArriveAtOffsetPosition(self):
        initialJump = self.timeStamps[0]
        initialStamp = self.timeStamps[0]


        for i in range(1, len(self.timeStamps)):
            nextTimestamp = self.timeStamps[i]
            while (initialStamp + self.busIDToOffset[nextTimestamp]) % nextTimestamp != 0:
                initialStamp += initialJump
            initialJump *= nextTimestamp

        return initialStamp














        # smallesttimestamp = self.timeStamps[0]
        # for i in range(1, len(self.timeStamps)):
        #     currTimestamp = self.timeStamps[i]
        #     while (smallesttimestamp + busIdToOffset[currTimestamp]) % currTimestamp != 0:
        #
        #
        #
        #
        # return smallesttimestamp




    def getMult(self, num, offset):
        a = []
        for i in range(1, 1000):
            a.append(i*num + offset)
        return a





def getAllBusIdsToOffsets(inputFile: str):
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
            return busIdToOffset, validBusIDs

        raise ValueError("Doublecheck the input format.")



def getNotesForPart1(inputFile: str):
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        if len(lines) > 1:
            busIDs = lines[1].strip("\n").split(",")
            validBusIDs = [int(busID) for busID in busIDs if busID.isnumeric()]
            return ShuttleBusOperation(int(lines[0].strip("\n")), validBusIDs)
        raise ValueError("Doublecheck the input format.")


#sb = getNotesForPart1(TEST_INPUT)
#print(sb.getEarliestSuitableBusID())

efInput = getAllBusIdsToOffsets(INPUT_FILE)
ef = EarliestTimestampFinder(efInput[0], efInput[1])
# ef.getOffsetToBusID()
# #print(ef.offsetToBusID)
print(ef.getEarliestTimestampBusesArriveAtOffsetPosition())


#
# mechanicInput2 = ["1789","37","47","1889"]
# mechanicDict = {0: 1789, 1: 37, 2:47, 3: 1889}
# mi = EarliestTimestampFinder(mechanicDict)
# mi.offsetToBusID = mechanicDict
#print(mi.getEarliestTimestampBusesArriveAtOffsetPosition())



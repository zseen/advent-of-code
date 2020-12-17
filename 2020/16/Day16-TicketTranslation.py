import unittest
from typing import List, Dict

TEST_INPUT = "test_input.txt"
NEARBY_TICKETS_INPUT = "nearbyTickets.txt"

def extractNumList(numList):
    lowestBound = numList[0]
    upperBound = numList[1]
    lowerBound = numList[2]
    uppestBound = numList[3]
    return [num for num in range(lowestBound, uppestBound + 1) if num <= upperBound or num >= lowerBound]

DEPARTURE_LOCATION = [num for num in range(45, 951) if num < 423 or num > 443]
DEPARTURE_STATION= extractNumList([36, 741, 752, 956])
DEPARTURE_PLATFORM = extractNumList([46, 788, 806, 967])
DEPARTURE_TRACK = extractNumList([46, 57, 70, 950])
DEPARTURE_DATE = extractNumList([35, 99, 108, 974])
DEPARTURE_TIME = extractNumList([42, 883, 903, 62])
ARRIVAL_LOCATION = extractNumList([47, 83, 95, 953])
ARRIVAL_STATION = extractNumList([31, 227, 240, 970])
ARRIVAL_PLATFORM = extractNumList([48, 840, 853, 964])
ARRIVAL_TRACK = extractNumList([49, 487, 499, 964])
CLASS = extractNumList([33, 363, 381, 959])
DURATION = extractNumList([35, 509, 522, 951])
PRICE = extractNumList([38, 590, 601, 950])
ROUTE = extractNumList([41, 266, 285, 962])
ROW = extractNumList([44, 402, 419, 962])
SEAT = extractNumList([41, 615, 634, 956])
TRAIN = extractNumList([47, 156, 178, 954])
TYPE =  extractNumList([44, 313, 338, 964])
WAGON = extractNumList([30, 110, 133, 970])
ZONE = extractNumList([38, 541, 550, 965])







class Train:
    def __init__(self):
        self.departureLocation = DEPARTURE_LOCATION
        self.departureStation = DEPARTURE_STATION
        self.departurePlatform = DEPARTURE_PLATFORM
        self.departureTrack = DEPARTURE_TRACK
        self.departureDate = DEPARTURE_DATE
        self.departureTime = DEPARTURE_TIME
        self.arrivalLocation = ARRIVAL_LOCATION
        self.arrivalStation = ARRIVAL_STATION
        self.arrivalPlatform = ARRIVAL_PLATFORM
        self.arrivalTrack = ARRIVAL_TRACK
        self.trainClass = CLASS
        self.duration = DURATION
        self.price = PRICE
        self.route = ROUTE
        self.row = ROW
        self.seat = SEAT
        self.train = TRAIN
        self.trainType = TYPE
        self.wagon = WAGON
        self.zone = ZONE
        self.allTrainDataCombined: set = self._flatten([self.departureLocation, self.departureStation, self.departurePlatform, self.departureTrack, self.departureDate, self.departureTime,
                                                                  self.arrivalLocation, self.arrivalStation, self.arrivalPlatform, self.arrivalTrack,
                                                                  self.trainClass, self.duration, self.price, self.route, self.row, self.seat, self.train, self.trainType, self.wagon, self.zone])

    def _flatten(self, arrayToFlatten):
        flattenedSet = set()

        for subArray in arrayToFlatten:

            for i in range(0, len(subArray)):
                flattenedSet.add(subArray[i])
        return flattenedSet


#

class MyTicket:
    def __init__(self):
        self.infoForPlace = [109,199,223,179,97,227,197,151,73,79,211,181,71,139,53,149,137,191,83,193]


class NearbyTickets:
    def __init__(self, allNearbyTicketsInfo: List[List[int]]):
        self.allNearbyTicketsInfo = allNearbyTicketsInfo

    def getValidTickets(self):
        return self.allNearbyTicketsInfo



def getInput(inputFile: str):
    nearbyTickets = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip()
            lineSplit = line.split(",")
            lineWithNums = [int(num) for num in lineSplit]
            nearbyTickets.append(lineWithNums)
    return nearbyTickets


class TestTrain:
    def __init__(self):
        self.trainClass = [1, 2, 3, 5, 6, 7]
        self.row = [6, 7, 8, 9, 10, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
        self.seat = [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 45, 46, 47, 48, 49, 50]

        # self.trainClass = extractNumList([0, 1, 4, 19])
        #
        # self.row = extractNumList([ 0, 5, 8, 19])
        # self.seat = extractNumList([0 ,13 , 16 ,19])
        self.allTrainDataCombined: set = self._flatten([self.trainClass, self.row, self.seat])

    def _flatten(self, arrayToFlatten):
        flattenedSet = set()
        for subArray in arrayToFlatten:
            for i in range(0, len(subArray)):
                flattenedSet.add(subArray[i])
        return flattenedSet

class TestMyTicket:
    def __init__(self):
        self.infoForPlace = [7, 1, 14]

class TestNearbyTickets:
    def __init__(self):
        self.allNearbyTicketsInfo = [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]]



def findInvalidTickets(train, nearbyTickets):
    invalidNumsSum = 0
    toDelete = []
    for ticketNearby in nearbyTickets.allNearbyTicketsInfo:
        for ticketInfo in ticketNearby:
            if ticketInfo not in train.allTrainDataCombined:
                invalidNumsSum += ticketInfo
                toDelete.append(ticketNearby)
    v = nearbyTickets.allNearbyTicketsInfo
    for item in toDelete:
        nearbyTickets.allNearbyTicketsInfo.remove(item)
    return invalidNumsSum



class PositionLocator(Train):

    def positionPossibilityChecker(self, validNearbyTickets):
        allTrainFields = [self.departureLocation, self.departureStation, self.departurePlatform, self.departureTrack, self.departureDate, self.departureTime,
                                                                  self.arrivalLocation, self.arrivalStation, self.arrivalPlatform, self.arrivalTrack,
                                                                  self.trainClass, self.duration, self.price, self.route, self.row, self.seat, self.train, self.trainType, self.wagon, self.zone]


        #allTrainFields = [self.trainClass, self.row, self.seat]
        positionToField = dict()


        for i in range(0, len(validNearbyTickets[0])):
            iCanBe = []
            for trainField in allTrainFields:
                if self.canThisIndexBeThisField(validNearbyTickets, i, trainField):
                    iCanBe.append(trainField)

            positionToField[i] = iCanBe



        #return positionToField
        #indexToTrainFeature = {0: "class", 1: "row", 2: "seat"}

        indexToTrainFeature = {0: "departureLocation", 1: "departureStation", 2: "departurePlatform",
                               3: "departureTrack", 4: "departureDate", 5: "departureTime",
                               6: "arrivalLocation", 7: "arrivalStation", 8: "arrivalPlatform", 9: "arrivalTrack",
                               10: "trainClass", 11: "duration", 12: "price", 13: "route", 14: "row", 15: "seat",
                               16: "train", 17: "trainType", 18: "wagon", 19: "zone"}

        foundFeatures = []


        while len(foundFeatures) != len(allTrainFields):
            currentFeatureFound = None
            for position in positionToField:
                if len(positionToField[position]) == 1:
                    print(position)

                    currentPosition = positionToField[position][0]
                    indexInAllTrainFields = self.lookupFieldIndexByArray(allTrainFields, currentPosition)
                    foundFeatures.append(indexToTrainFeature[indexInAllTrainFields])
                    currentFeatureFound = currentPosition
                    print(foundFeatures)

                for subArray in positionToField[position]:
                    if currentFeatureFound == subArray:
                        positionToField[position].remove(currentFeatureFound)

        return foundFeatures






    def canThisIndexBeThisField(self, nearbyTicketsMemberArrayOfArrays, index, field):
        for chunk in nearbyTicketsMemberArrayOfArrays:
            v = chunk[index]
            c = field
            z = nearbyTicketsMemberArrayOfArrays
            if chunk[index] not in field:
                return False
        return True


    def lookupFieldIndexByArray(self, allTranFields, foundArray):
        for i in range(len(allTranFields)):
            if foundArray == allTranFields[i]:
                return i








def main():
    # inputForNearbyTickets = getInput(NEARBY_TICKETS_INPUT)
    # train = Train()
    # myTicket = MyTicket()
    # nearbyTickets = NearbyTickets(inputForNearbyTickets)

    # train = TestTrain()
    # nearbyTickets = TestNearbyTickets()
    # invalidNumsSum = findInvalidTickets(train, nearbyTickets)
    # print(nearbyTickets.allNearbyTicketsInfo)
    # pl = PositionLocator()
    #x = pl.positionPossibilityChecker([[3,9,18],[15,1,5], [5,14,9], [11,12,13]])
    #print(x)

    inputForNearbyTickets = getInput(NEARBY_TICKETS_INPUT)
    train = Train()
    nearbyTickets = NearbyTickets(inputForNearbyTickets)
    #print(len(nearbyTickets.allNearbyTicketsInfo))
    x = findInvalidTickets(train, nearbyTickets)
    print(x)
    #print(len(nearbyTickets.allNearbyTicketsInfo))
    m = MyTicket()
    possLoc = PositionLocator()
    #print(nearbyTickets.getValidTickets())
    validTickets = nearbyTickets.getValidTickets()
    validTickets.append(m.infoForPlace)
    #print(validTickets)
    x = possLoc.positionPossibilityChecker(nearbyTickets.getValidTickets())
    print(x)






if __name__ == '__main__':
    main()
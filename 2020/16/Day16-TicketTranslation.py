import unittest
from typing import List, Dict

TEST_INPUT = "test_input.txt"
TEST_INPUT_SECOND_PART = "test_input_second_part.txt"
INPUT_FILE = "input.txt"

def extractNumList(numList):
    lowestBound = numList[0]
    upperBound = numList[1]
    lowerBound = numList[2]
    uppestBound = numList[3]
    return [num for num in range(lowestBound, uppestBound + 1) if num <= upperBound or num >= lowerBound]



def getInput(inputFile: str):
    trainPropertiesAndMyTicketAndTicketsNearby = [[]]
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            if line != "\n":
                trainPropertiesAndMyTicketAndTicketsNearby[-1].append(line.strip("\n"))
            else:
                trainPropertiesAndMyTicketAndTicketsNearby.append([])
    return trainPropertiesAndMyTicketAndTicketsNearby

def handleRawInput(rawTrainOwnTicketNearbyTickets: [[str]]):
    allTrainPropertiesToValues = []
    for trainProperty in rawTrainOwnTicketNearbyTickets[0]:
        trainProperty = trainProperty.split(": ")
        propertyDataFull: List[int] = extractNumList(parsingHelper(trainProperty[1]))
        propertyToValidDataRange = {trainProperty[0]: propertyDataFull}
        allTrainPropertiesToValues.append(propertyToValidDataRange)

    myTicket = parsingHelper(rawTrainOwnTicketNearbyTickets[1][1])

    nearbyTickets = [parsingHelper(ticket) for ticket in rawTrainOwnTicketNearbyTickets[2][1:]]
    nearbyTickets.append(myTicket)

    return allTrainPropertiesToValues, myTicket, nearbyTickets


def parsingHelper(dataRange: str):
    dataRange = dataRange.replace("or", ",").replace("-", ",")
    return [int(num) for num in dataRange.split(",")]

def sumInvalidValuesInTicketsNearby(trainProperties: List[Dict[str, List[int]]], nearbyTickets: List[List[int]]):
    invalidTicketsValues = 0
    for ticket in nearbyTickets:
        for ticketData in ticket:
            isTicketDataValid = False
            for trainProperty in trainProperties:
                for trainPropertyName, propertyData in trainProperty.items():
                    if ticketData in propertyData:
                        isTicketDataValid = True
                        break
            if not isTicketDataValid:
                invalidTicketsValues += ticketData

    return invalidTicketsValues

def removeInvalidTicketsFromNearbyTickets(trainProperties: List[Dict[str, List[int]]], nearbyTickets: List[List[int]]):
    ticketsToRemove = []
    for ticket in nearbyTickets:
        for ticketData in ticket:
            isTicketDataValid = False
            for trainProperty in trainProperties:
                for trainPropertyName, propertyData in trainProperty.items():
                    if ticketData in propertyData:
                        isTicketDataValid = True
                        break


            if not isTicketDataValid:
                ticketsToRemove.append(ticket)
                break
            continue

    for item in ticketsToRemove:
        nearbyTickets.remove(item)
    return nearbyTickets

def getPositionToPossibleTrainFields(trainProperties: List[Dict[str, List[int]]], validNearbyTickets: List[List[int]]):
    positionToPossibleFields = {}

    for position in range(0, len(validNearbyTickets[0])):
            possibleFieldsAtPosition = []
            for trainPropertyToData in trainProperties:
                for trainProperty, propertyData in trainPropertyToData.items():
                    if canThisIndexBeThisField(validNearbyTickets, position, propertyData):
                        possibleFieldsAtPosition.append(trainProperty)

            positionToPossibleFields[position] = possibleFieldsAtPosition
    return positionToPossibleFields

def canThisIndexBeThisField(nearbyTickets: List[List[int]], index: int, property: List[int]):
    for ticket in nearbyTickets:
        if ticket[index] not in property:
            return False
    return True


def getTrainFieldPositionInTicket(positionToPossibleFields: Dict[int, List[str]]):
    currentFeatureFound: str = ""
    locatedProperties: List[str] = [""] * len(positionToPossibleFields)
    allLocatedPropertiesSoFar: set[str] = set()

    for i in range(1, len(positionToPossibleFields) + 1):
        for position in positionToPossibleFields:
            if len(positionToPossibleFields[position]) == i:
                properties = positionToPossibleFields[position]
                for property in properties:
                    if property not in allLocatedPropertiesSoFar:
                        currentFeatureFound = property
                locatedProperties[position]=(currentFeatureFound)
                allLocatedPropertiesSoFar.add(currentFeatureFound)
                break
    return locatedProperties

def getDepartureIndexesInTrainPropertiesPositionsOnTicket(allProperties):
    return [i for i in range(len(allProperties)) if "departure" in allProperties[i]]


def multiplyDeparturePropertiesInMyTicket(allProperties: List[str], myTicket):
    indexesForDeparture = getDepartureIndexesInTrainPropertiesPositionsOnTicket(allProperties)

    product = 1
    for index in indexesForDeparture:
        product *= myTicket[index]
    return product


def main():
    rawInput = getInput(INPUT_FILE)
    train, myTicket, nearbyTickets = handleRawInput(rawInput)
    #print(nearbyTickets)
    #print(sumInvalidValuesInTicketsNearby(train, nearbyTickets))
    nearbyTicketsFiltered = removeInvalidTicketsFromNearbyTickets(train, nearbyTickets)
    #print(nearbyTicketsFiltered)
    x = getPositionToPossibleTrainFields(train, nearbyTicketsFiltered)

    v = getTrainFieldPositionInTicket(x)
    print(v)
    print(len(set(v)))
    print(getDepartureIndexesInTrainPropertiesPositionsOnTicket(v))
    c = multiplyDeparturePropertiesInMyTicket(v, myTicket)
    print(c)





if __name__ == '__main__':
    main()











#
# class Train:
#     def __init__(self):
#         self.departureLocation = DEPARTURE_LOCATION
#         self.departureStation = DEPARTURE_STATION
#         self.departurePlatform = DEPARTURE_PLATFORM
#         self.departureTrack = DEPARTURE_TRACK
#         self.departureDate = DEPARTURE_DATE
#         self.departureTime = DEPARTURE_TIME
#         self.arrivalLocation = ARRIVAL_LOCATION
#         self.arrivalStation = ARRIVAL_STATION
#         self.arrivalPlatform = ARRIVAL_PLATFORM
#         self.arrivalTrack = ARRIVAL_TRACK
#         self.trainClass = CLASS
#         self.duration = DURATION
#         self.price = PRICE
#         self.route = ROUTE
#         self.row = ROW
#         self.seat = SEAT
#         self.train = TRAIN
#         self.trainType = TYPE
#         self.wagon = WAGON
#         self.zone = ZONE
#         self.allTrainDataCombined: set = self._flatten([self.departureLocation, self.departureStation, self.departurePlatform, self.departureTrack, self.departureDate, self.departureTime,
#                                                                   self.arrivalLocation, self.arrivalStation, self.arrivalPlatform, self.arrivalTrack,
#                                                                   self.trainClass, self.duration, self.price, self.route, self.row, self.seat, self.train, self.trainType, self.wagon, self.zone])
#
#     def _flatten(self, arrayToFlatten):
#         flattenedSet = set()
#
#         for subArray in arrayToFlatten:
#
#             for i in range(0, len(subArray)):
#                 flattenedSet.add(subArray[i])
#         return flattenedSet
#
#
# #
#
# class MyTicket:
#     def __init__(self):
#         self.infoForPlace = [109,199,223,179,97,227,197,151,73,79,211,181,71,139,53,149,137,191,83,193]
#
#
# class NearbyTickets:
#     def __init__(self, allNearbyTicketsInfo: List[List[int]]):
#         self.allNearbyTicketsInfo = allNearbyTicketsInfo
#
#     def getValidTickets(self):
#         return self.allNearbyTicketsInfo
#
#
#
# def getInput(inputFile: str):
#     nearbyTickets = []
#     with open(inputFile, "r") as inputFile:
#         lines = inputFile.readlines()
#         for line in lines:
#             line = line.strip()
#             lineSplit = line.split(",")
#             lineWithNums = [int(num) for num in lineSplit]
#             nearbyTickets.append(lineWithNums)
#     return nearbyTickets
#
#
# # class TestTrain:
# #     def __init__(self, tclass, row, seat):
# #         self.trainClass = tclass #[1, 2, 3, 5, 6, 7]
# #         self.row = row #[6, 7, 8, 9, 10, 11, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44]
# #         self.seat = seat#[13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 45, 46, 47, 48, 49, 50]
# #
# #         # self.trainClass = extractNumList([0, 1, 4, 19])
# #         #
# #         # self.row = extractNumList([ 0, 5, 8, 19])
# #         # self.seat = extractNumList([0 ,13 , 16 ,19])
# #         self.allTrainDataCombined: set = self._flatten([self.trainClass, self.row, self.seat])
# #
# #     def _flatten(self, arrayToFlatten):
# #         flattenedSet = set()
# #         for subArray in arrayToFlatten:
# #             for i in range(0, len(subArray)):
# #                 flattenedSet.add(subArray[i])
# #         return flattenedSet
# #
# # class TestMyTicket:
# #     def __init__(self):
# #         self.infoForPlace = [7, 1, 14]
# #
# # class TestNearbyTickets:
# #     def __init__(self):
# #         self.allNearbyTicketsInfo = [[7, 3, 47], [40, 4, 50], [55, 2, 20], [38, 6, 12]]
#
#
#
# def findInvalidTickets(train, nearbyTickets):
#     invalidNumsSum = 0
#     toDelete = []
#     for ticketNearby in nearbyTickets.allNearbyTicketsInfo:
#         for ticketInfo in ticketNearby:
#             l = train.allTrainDataCombined
#             if ticketInfo not in train.allTrainDataCombined:
#                 invalidNumsSum += ticketInfo
#                 toDelete.append(ticketNearby)
#     v = nearbyTickets.allNearbyTicketsInfo
#     for item in toDelete:
#         nearbyTickets.allNearbyTicketsInfo.remove(item)
#     return invalidNumsSum
#
#
#
# class PositionLocator(Train):
#
#     def positionPossibilityChecker(self, validNearbyTickets):
#         allTrainFields = [self.departureLocation, self.departureStation, self.departurePlatform, self.departureTrack, self.departureDate, self.departureTime,
#                                                                   self.arrivalLocation, self.arrivalStation, self.arrivalPlatform, self.arrivalTrack,
#                                                                   self.trainClass, self.duration, self.price, self.route, self.row, self.seat, self.train, self.trainType, self.wagon, self.zone]
#
#
#         #allTrainFields = [self.trainClass, self.row, self.seat]
#         positionToField = dict()
#
#
#         for i in range(0, len(validNearbyTickets[0])):
#             iCanBe = []
#             for trainField in allTrainFields:
#                 if self.canThisIndexBeThisField(validNearbyTickets, i, trainField):
#                     iCanBe.append(trainField)
#
#             positionToField[i] = iCanBe
#
#
#         #print(len(positionToField.keys()))
#         for key, value in positionToField.items():
#             print(key, len(value))
#
#         #return positionToField
#         #indexToTrainFeature = {0: "class", 1: "row", 2: "seat"}
#
#         #indexToTrainFeature = {0: "trainClass", 1: "row", 2:"seat"}
#
#         indexToTrainFeature = {0: "departureLocation", 1: "departureStation", 2: "departurePlatform",
#                                3: "departureTrack", 4: "departureDate", 5: "departureTime",
#                                6: "arrivalLocation", 7: "arrivalStation", 8: "arrivalPlatform", 9: "arrivalTrack",
#                                10: "trainClass", 11: "duration", 12: "price", 13: "route", 14: "row", 15: "seat",
#                                16: "train", 17: "trainType", 18: "wagon", 19: "zone"}
#
#         foundFeatures = [""] * 20
#
#         allFoundFields = []
#         from copy import deepcopy
#
#
#
#         currentFeatureFound = None
#
#         for i in range(1, 21):
#             for position in sorted(positionToField, key=lambda k: len(positionToField[k])):
#                 if len(positionToField[position]) == i:
#                     fields = positionToField[position]
#                     for field in fields:
#                         if field not in allFoundFields:
#                             currentFeatureFound = field
#                     indexInAllTrainFields = self.lookupFieldIndexByArray(allTrainFields, currentFeatureFound)
#                     foundFeatures[position]=(indexToTrainFeature[indexInAllTrainFields])
#                     allFoundFields.append(currentFeatureFound)
#                     break
#         return foundFeatures
#
#
#
#
#
#
#     def canThisIndexBeThisField(self, nearbyTicketsMemberArrayOfArrays, index, field):
#         for chunk in nearbyTicketsMemberArrayOfArrays:
#             if chunk[index] not in field:
#                 return False
#         return True
#
#
#     def lookupFieldIndexByArray(self, allTranFields, foundArray):
#         for i in range(0, len(allTranFields)):
#             if foundArray == allTranFields[i]:
#                 return i
#
#
#
# def main():
#     # inputForNearbyTickets = getInput(NEARBY_TICKETS_INPUT)
#     # train = Train()
#     # myTicket = MyTicket()
#     # nearbyTickets = NearbyTickets(inputForNearbyTickets)
#
#     # train = TestTrain()
#     # nearbyTickets = TestNearbyTickets()
#     # invalidNumsSum = findInvalidTickets(train, nearbyTickets)
#     # print(nearbyTickets.allNearbyTicketsInfo)
#     # pl = PositionLocator()
#     #x = pl.positionPossibilityChecker([[3,9,18],[15,1,5], [5,14,9], [11,12,13]])
#     #print(x)
#
#     inputForNearbyTickets = getInput(NEARBY_TICKETS_INPUT)
#     train = Train()
#     m = MyTicket()
#     inputForNearbyTickets.append(m.infoForPlace)
#     nearbyTickets = NearbyTickets(inputForNearbyTickets)
#     x = findInvalidTickets(train, nearbyTickets) # DO NOT REMOVE
#     #m = MyTicket()
#     possLoc = PositionLocator()
#     validTickets = nearbyTickets.getValidTickets()
#     #validTickets.append(m.infoForPlace)
#     x = possLoc.positionPossibilityChecker(validTickets)
#     print(x)
#
#
#
#     indexToTrainFeature = {0: "departureLocation", 1: "departureStation", 2: "departurePlatform",
#                            3: "departureTrack", 4: "departureDate", 5: "departureTime",
#                            6: "arrivalLocation", 7: "arrivalStation", 8: "arrivalPlatform", 9: "arrivalTrack",
#                            10: "trainClass", 11: "duration", 12: "price", 13: "route", 14: "row", 15: "seat",
#                            16: "train", 17: "trainType", 18: "wagon", 19: "zone"}
#
#     #print(x[8])
#     #print(x[9])
#     #print(x[10])
#
#     # for item in x[10]:
#     #     if item not in x[8]:
#     #         print(item)
#     mt = m.infoForPlace
#     depLoc = mt[x.index("departureLocation")]
#     depStat = mt[x.index("departureStation")]
#     depPlat = mt[x.index("departurePlatform")]
#     depTrack = mt[x.index("departureTrack")]
#     depDate = mt[x.index("departureDate")]
#     depTime = mt[x.index("departureTime")]
#
#     print(depLoc * depStat * depPlat * depTrack * depDate * depTime) # 3777380346031 too high , 3429967441937
#     #
#     # loc = x.index("departureLocation")
#     # print(loc)
#     # stat = x.index("departureStation")
#     # print(stat)
#     # plat = x.index("departurePlatform")
#     # print(plat)
#     # track = x.index("departureTrack")
#     # print(track)
#     # date = x.index("departureDate")
#     # print(date)
#     # time = x.index("departureTime")
#     # print(time)
#
#     # class: 0 - 1 or 4 - 19
#     #
#     # departure
#     # row: 0 - 5 or 8 - 19
#     # departure
#     # seat: 0 - 13 or 16 - 19
#     #
#     # your
#     # ticket:
#     # 11, 12, 13
#     #
#     # nearby
#     # tickets:
#     # 3, 9, 18
#     # 15, 1, 5
#     # 5, 14, 9
#
#
#
#
#
#
#
#
# if __name__ == '__main__':
#     main()
import unittest
from typing import List, Dict

INPUT_FILE = "input.txt"
TEST_INPUT_FIRST_PART = "test_input.txt"
TEST_INPUT_SECOND_PART = "test_input_second_part.txt"
TRAIN_PROPERTIES_DEPARTURE_PREFIX = "departure"


def handleInput(inputFile: str):
    trainPropertiesAndMyTicketAndTicketsNearby = [[]]
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            if line != "\n":
                trainPropertiesAndMyTicketAndTicketsNearby[-1].append(line.strip("\n"))
            else:
                trainPropertiesAndMyTicketAndTicketsNearby.append([])
    return trainPropertiesAndMyTicketAndTicketsNearby


def parseInput(rawTrainOwnTicketNearbyTickets: List[List[str]]):
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


def extractNumList(numList):
    lowestBound = numList[0]
    upperBound = numList[1]
    lowerBound = numList[2]
    uppestBound = numList[3]
    return [num for num in range(lowestBound, uppestBound + 1) if num <= upperBound or num >= lowerBound]


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


def locateTrainPropertiesOnTickets(train, nearbyTickets):
    nearbyTicketsFiltered = removeInvalidTicketsFromNearbyTickets(train, nearbyTickets)
    positionToPossibleTrainProperty = getPositionToPossibleTrainProperties(train, nearbyTicketsFiltered)
    return getTrainPropertyPositionInTicket(positionToPossibleTrainProperty)


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

    for item in ticketsToRemove:
        nearbyTickets.remove(item)
    return nearbyTickets


def getPositionToPossibleTrainProperties(trainProperties: List[Dict[str, List[int]]],
                                         validNearbyTickets: List[List[int]]):
    positionToPossibleProperties: Dict[int, List[str]] = {}

    for position in range(0, len(validNearbyTickets[0])):
        possiblePropertiesAtPosition = []
        for trainPropertyToData in trainProperties:
            for trainProperty, propertyData in trainPropertyToData.items():
                if canPropertyBeAtPosition(validNearbyTickets, position, propertyData):
                    possiblePropertiesAtPosition.append(trainProperty)

        positionToPossibleProperties[position] = possiblePropertiesAtPosition
    return positionToPossibleProperties


def canPropertyBeAtPosition(nearbyTickets: List[List[int]], position: int, property: List[int]):
    for ticket in nearbyTickets:
        if ticket[position] not in property:
            return False
    return True


def getTrainPropertyPositionInTicket(positionToPossibleProperties: Dict[int, List[str]]):
    currentPropertyFound: str = ""
    locatedProperties: List[str] = [""] * len(positionToPossibleProperties)
    allLocatedPropertiesSoFar: set[str] = set()

    for i in range(1, len(positionToPossibleProperties) + 1):
        for position in positionToPossibleProperties:
            if len(positionToPossibleProperties[position]) == i:
                properties = positionToPossibleProperties[position]
                for property in properties:
                    if property not in allLocatedPropertiesSoFar:
                        currentPropertyFound = property
                locatedProperties[position] = currentPropertyFound
                allLocatedPropertiesSoFar.add(currentPropertyFound)
                break
    return locatedProperties


def multiplyDeparturePropertiesInMyTicket(allProperties: List[str], myTicket):
    indexesForDeparture = getDepartureIndexesInTrainPropertiesPositionsOnTicket(allProperties)
    product = 1
    for index in indexesForDeparture:
        product *= myTicket[index]
    return product


def getDepartureIndexesInTrainPropertiesPositionsOnTicket(allProperties):
    return [i for i in range(len(allProperties)) if TRAIN_PROPERTIES_DEPARTURE_PREFIX in allProperties[i]]


def main():
    rawInput = handleInput(INPUT_FILE)
    train, myTicket, nearbyTickets = parseInput(rawInput)
    invalidTicketValuesSum = sumInvalidValuesInTicketsNearby(train, nearbyTickets)
    print(invalidTicketValuesSum)  # 21071

    trainPropertiesPositionsOnTicket = locateTrainPropertiesOnTickets(train, nearbyTickets)
    departurePropertiesProductOnMyTicket = multiplyDeparturePropertiesInMyTicket(trainPropertiesPositionsOnTicket,
                                                                                 myTicket)
    print(departurePropertiesProductOnMyTicket)  # 3429967441937


class TrainPropertyLocatorTester(unittest.TestCase):
    def test_sumInvalidValuesInTicketsNearby_correctSumReturned(self):
        rawInput = handleInput(TEST_INPUT_FIRST_PART)
        train, myTicket, nearbyTickets = parseInput(rawInput)
        invalidTicketValuesSum = sumInvalidValuesInTicketsNearby(train, nearbyTickets)
        self.assertEqual(71, invalidTicketValuesSum)

    def test_locateTrainPropertiesOnTickets_correctProductReturned(self):
        rawInput = handleInput(TEST_INPUT_SECOND_PART)
        train, myTicket, nearbyTickets = parseInput(rawInput)
        trainPropertiesPositionsOnTicket = locateTrainPropertiesOnTickets(train, nearbyTickets)
        self.assertEqual(["row", "class", "seat"], trainPropertiesPositionsOnTicket)


if __name__ == '__main__':
    # main()
    unittest.main()

import unittest
from typing import List, Dict, Tuple

INPUT_FILE = "input.txt"
TEST_INPUT_FIRST_PART = "test_input.txt"
TEST_INPUT_SECOND_PART = "test_input_second_part.txt"
TRAIN_PROPERTIES_DEPARTURE_PREFIX = "departure"

TrainPropertiesToValuesType = List[Dict[str, List[int]]]
TicketType = List[int]
NearbyTicketsType = List[List[int]]


class TrainTicketPositionExtractor:
    def __init__(self, trainProperties: TrainPropertiesToValuesType, ownTicket: TicketType,
                 nearbyTickets: NearbyTicketsType):
        self.trainProperties = trainProperties
        self.ownTicket = ownTicket
        self.nearbyTickets = nearbyTickets

    def getSumOfNearbyInvalidTicketValues(self):
        sumOfNearbyInvalidTicketValues = 0
        for ticket in self.nearbyTickets:
            for ticketData in ticket:
                if not self.isTicketDataValid(ticketData):
                    sumOfNearbyInvalidTicketValues += ticketData
        return sumOfNearbyInvalidTicketValues

    def isTicketDataValid(self, ticketData: int) -> bool:
        for trainProperty in self.trainProperties:
            isTicketDataValid = any(
                ticketData in propertyData for trainPropertyName, propertyData in trainProperty.items())
            if isTicketDataValid:
                return True
        return False

    def findTrainPropertiesOnTickets(self) -> List[str]:
        self.removeInvalidTicketsFromNearbyTickets()
        positionToPossibleTrainProperty = self.getPositionToPossibleTrainProperties()
        return self.getTrainPropertyPositionInTicket(positionToPossibleTrainProperty)

    def removeInvalidTicketsFromNearbyTickets(self):
        ticketsToRemove = []
        for ticket in self.nearbyTickets:
            for ticketData in ticket:
                if not self.isTicketDataValid(ticketData):
                    ticketsToRemove.append(ticket)

        for item in ticketsToRemove:
            self.nearbyTickets.remove(item)

    def getPositionToPossibleTrainProperties(self) -> Dict[int, List[str]]:
        positionToPossibleProperties: Dict[int, List[str]] = {}

        for position in range(0, len(self.nearbyTickets[0])):
            positionToPossibleProperties[position] = self.getPossibleTrainPropertiesAtPosition(position)
        return positionToPossibleProperties

    def getPossibleTrainPropertiesAtPosition(self, position: int):
        possiblePropertiesAtPosition = []
        for trainPropertyToData in self.trainProperties:
            for trainProperty, propertyData in trainPropertyToData.items():
                if self.canPropertyBeAtPosition(position, propertyData):
                    possiblePropertiesAtPosition.append(trainProperty)
        return possiblePropertiesAtPosition

    def canPropertyBeAtPosition(self, position: int, validValues: List[int]) -> bool:
        for ticket in self.nearbyTickets:
            if ticket[position] not in validValues:
                return False
        return True

    def getTrainPropertyPositionInTicket(self, positionToPossibleProperties: Dict[int, List[str]]) -> List[str]:
        locatedProperties: List[str] = [""] * len(positionToPossibleProperties)

        for _ in range(1, len(positionToPossibleProperties) + 1):
            for position in positionToPossibleProperties:
                if len(positionToPossibleProperties[position]) == 1:
                    currentPropertyFound = positionToPossibleProperties[position][0]
                    locatedProperties[position] = currentPropertyFound
                    self.removePropertyFromAllPositionToPossibleProperties(positionToPossibleProperties,
                                                                           currentPropertyFound)

        return locatedProperties

    def removePropertyFromAllPositionToPossibleProperties(self, positionToPossibleProperties: Dict[int, List[str]],
                                                          currentPropertyFound: str) -> None:
        for position in positionToPossibleProperties:
            if currentPropertyFound in positionToPossibleProperties[position]:
                positionToPossibleProperties[position].remove(currentPropertyFound)

    def getProductOfDeparturePropertiesInMyTicket(self, allProperties: List[str]) -> int:
        indexesForDeparture = self.getDepartureIndexesOnTicket(allProperties)
        product = 1
        for index in indexesForDeparture:
            product *= self.ownTicket[index]
        return product

    def getDepartureIndexesOnTicket(self, allProperties) -> List[int]:
        return [i for i in range(len(allProperties)) if TRAIN_PROPERTIES_DEPARTURE_PREFIX in allProperties[i]]


def createTextSectionsFromInput(inputFile: str) -> List[List[str]]:
    with open(inputFile, "r") as inputFile:
        textToSplit = inputFile.read()
        categories = textToSplit.split("\n\n")
        textSections = [category.strip("\n").split("\n") for category in categories]
    return textSections


def parseInput(textSections: List[List[str]]) -> Tuple[
    TrainPropertiesToValuesType, TicketType, NearbyTicketsType]:
    allTrainPropertiesToValues = []
    for trainProperty in textSections[0]:
        trainProperty = trainProperty.split(": ")
        propertyDataFull: List[int] = extractNumList(createTicketValuesFromDataRangeString(trainProperty[1]))
        propertyToValidDataRange = {trainProperty[0]: propertyDataFull}
        allTrainPropertiesToValues.append(propertyToValidDataRange)

    myTicket = createTicketValuesFromDataRangeString(textSections[1][1])

    nearbyTickets = [createTicketValuesFromDataRangeString(ticket) for ticket in textSections[2][1:]]
    nearbyTickets.append(myTicket)

    return allTrainPropertiesToValues, myTicket, nearbyTickets


def extractNumList(numList) -> List[int]:
    if len(numList) != 4:
        raise ValueError("Double check the input format for train properties.")

    firstSectionLowerBound = numList[0]
    firstSectionUpperBound = numList[1]
    secondSectionLowerBound = numList[2]
    secondSectionUpperBound = numList[3]
    return [num for num in range(firstSectionLowerBound, secondSectionUpperBound + 1) if
            num <= firstSectionUpperBound or num >= secondSectionLowerBound]


def createTicketValuesFromDataRangeString(dataRange: str) -> List[int]:
    dataRange = dataRange.replace("or", ",").replace("-", ",")
    return [int(num) for num in dataRange.split(",")]


def main():
    rawInput = createTextSectionsFromInput(INPUT_FILE)
    train, myTicket, nearbyTickets = parseInput(rawInput)
    trainTicketPositionExtractor = TrainTicketPositionExtractor(train, myTicket, nearbyTickets)

    invalidTicketValuesSum = trainTicketPositionExtractor.getSumOfNearbyInvalidTicketValues()
    print(invalidTicketValuesSum)  # 21071

    trainPropertiesPositionsOnTicket = trainTicketPositionExtractor.findTrainPropertiesOnTickets()
    departurePropertiesProductOnMyTicket = trainTicketPositionExtractor.getProductOfDeparturePropertiesInMyTicket(
        trainPropertiesPositionsOnTicket)
    print(departurePropertiesProductOnMyTicket)  # 3429967441937


class TrainPropertyLocatorTester(unittest.TestCase):
    def test_getSumOfNearbyInvalidTicketValues_correctSumReturned(self):
        rawInput = createTextSectionsFromInput(TEST_INPUT_FIRST_PART)
        train, myTicket, nearbyTickets = parseInput(rawInput)
        trainTicketPositionExtractor = TrainTicketPositionExtractor(train, myTicket, nearbyTickets)
        invalidTicketValuesSum = trainTicketPositionExtractor.getSumOfNearbyInvalidTicketValues()
        self.assertEqual(71, invalidTicketValuesSum)

    def test_getProductOfDeparturePropertiesInMyTicket_correctProductReturned(self):
        rawInput = createTextSectionsFromInput(TEST_INPUT_SECOND_PART)
        train, myTicket, nearbyTickets = parseInput(rawInput)
        trainTicketPositionExtractor = TrainTicketPositionExtractor(train, myTicket, nearbyTickets)
        trainPropertiesPositionsOnTicket = trainTicketPositionExtractor.findTrainPropertiesOnTickets()
        departurePropertiesProductOnMyTicket = trainTicketPositionExtractor.getProductOfDeparturePropertiesInMyTicket(
            trainPropertiesPositionsOnTicket)
        self.assertEqual(1716, departurePropertiesProductOnMyTicket)


if __name__ == '__main__':
    # main()
    unittest.main()

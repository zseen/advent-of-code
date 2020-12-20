import unittest
from typing import List, Dict, Tuple

INPUT_FILE = "input.txt"
TEST_INPUT_FIRST_PART = "test_input.txt"
TEST_INPUT_SECOND_PART = "test_input_second_part.txt"
TRAIN_PROPERTIES_DEPARTURE_PREFIX = "departure"

TrainPropertiesToValuesFormat = List[Dict[str, List[int]]]
TicketFormat = List[int]
NearbyTicketsFormat = List[List[int]]


class TrainTicketPositionExtractor:
    def __init__(self, trainProperties: TrainPropertiesToValuesFormat, ownTicket: TicketFormat,
                 nearbyTickets: NearbyTicketsFormat):
        self.trainProperties = trainProperties
        self.ownTicket = ownTicket
        self.nearbyTickets = nearbyTickets

    def sumInvalidValuesInTicketsNearby(self):
        invalidTicketsValues = 0
        for ticket in self.nearbyTickets:
            for ticketData in ticket:
                if not self.isTicketDataValid(ticketData):
                    invalidTicketsValues += ticketData
        return invalidTicketsValues

    def isTicketDataValid(self, ticketData: int) -> bool:
        for trainProperty in self.trainProperties:
            isTicketDataValid = any(
                ticketData in propertyData for trainPropertyName, propertyData in trainProperty.items())
            if isTicketDataValid:
                return True
        return False

    def locateTrainPropertiesOnTickets(self) -> List[str]:
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
            possiblePropertiesAtPosition = []
            for trainPropertyToData in self.trainProperties:
                for trainProperty, propertyData in trainPropertyToData.items():
                    if self.canPropertyBeAtPosition(position, propertyData):
                        possiblePropertiesAtPosition.append(trainProperty)

            positionToPossibleProperties[position] = possiblePropertiesAtPosition
        return positionToPossibleProperties

    def canPropertyBeAtPosition(self, position: int, validValues: List[int]) -> bool:
        for ticket in self.nearbyTickets:
            if ticket[position] not in validValues:
                return False
        return True

    def getTrainPropertyPositionInTicket(self, positionToPossibleProperties: Dict[int, List[str]]) -> List[str]:
        locatedProperties: List[str] = [""] * len(positionToPossibleProperties)
        currentPropertyFound: str = ""

        for i in range(1, len(positionToPossibleProperties) + 1):
            for position in positionToPossibleProperties:
                if len(positionToPossibleProperties[position]) == 1:
                    currentPropertyFound = positionToPossibleProperties[position][0]
                    locatedProperties[position] = currentPropertyFound

                if currentPropertyFound in positionToPossibleProperties[position]:
                    positionToPossibleProperties[position].remove(currentPropertyFound)

        return locatedProperties

    def multiplyDeparturePropertiesInMyTicket(self, allProperties: List[str]) -> int:
        indexesForDeparture = self.getDepartureIndexesOnTicket(allProperties)
        product = 1
        for index in indexesForDeparture:
            product *= self.ownTicket[index]
        return product

    def getDepartureIndexesOnTicket(self, allProperties) -> List[int]:
        return [i for i in range(len(allProperties)) if TRAIN_PROPERTIES_DEPARTURE_PREFIX in allProperties[i]]


def handleInput(inputFile: str) -> List[List[str]]:
    textSections: List[List[str]] = [[]]
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            if line != "\n":
                textSections[-1].append(line.strip("\n"))
            else:
                textSections.append([])
    return textSections


def parseInput(textSections: List[List[str]]) -> Tuple[
    TrainPropertiesToValuesFormat, TicketFormat, NearbyTicketsFormat]:
    allTrainPropertiesToValues = []
    for trainProperty in textSections[0]:
        trainProperty = trainProperty.split(": ")
        propertyDataFull: List[int] = extractNumList(helpParsing(trainProperty[1]))
        propertyToValidDataRange = {trainProperty[0]: propertyDataFull}
        allTrainPropertiesToValues.append(propertyToValidDataRange)

    myTicket = helpParsing(textSections[1][1])

    nearbyTickets = [helpParsing(ticket) for ticket in textSections[2][1:]]
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


def helpParsing(dataRange: str) -> List[int]:
    dataRange = dataRange.replace("or", ",").replace("-", ",")
    return [int(num) for num in dataRange.split(",")]


def main():
    rawInput = handleInput(INPUT_FILE)
    train, myTicket, nearbyTickets = parseInput(rawInput)
    trainTicketPositionExtractor = TrainTicketPositionExtractor(train, myTicket, nearbyTickets)

    invalidTicketValuesSum = trainTicketPositionExtractor.sumInvalidValuesInTicketsNearby()
    print(invalidTicketValuesSum)  # 21071

    trainPropertiesPositionsOnTicket = trainTicketPositionExtractor.locateTrainPropertiesOnTickets()
    departurePropertiesProductOnMyTicket = trainTicketPositionExtractor.multiplyDeparturePropertiesInMyTicket(
        trainPropertiesPositionsOnTicket)
    print(departurePropertiesProductOnMyTicket)  # 3429967441937


class TrainPropertyLocatorTester(unittest.TestCase):
    def test_sumInvalidValuesInTicketsNearby_correctSumReturned(self):
        rawInput = handleInput(TEST_INPUT_FIRST_PART)
        train, myTicket, nearbyTickets = parseInput(rawInput)
        trainTicketPositionExtractor = TrainTicketPositionExtractor(train, myTicket, nearbyTickets)
        invalidTicketValuesSum = trainTicketPositionExtractor.sumInvalidValuesInTicketsNearby()
        self.assertEqual(71, invalidTicketValuesSum)

    def test_locateTrainPropertiesOnTickets_correctProductReturned(self):
        rawInput = handleInput(TEST_INPUT_SECOND_PART)
        train, myTicket, nearbyTickets = parseInput(rawInput)
        trainTicketPositionExtractor = TrainTicketPositionExtractor(train, myTicket, nearbyTickets)
        trainPropertiesPositionsOnTicket = trainTicketPositionExtractor.locateTrainPropertiesOnTickets()
        self.assertEqual(["row", "class", "seat"], trainPropertiesPositionsOnTicket)


if __name__ == '__main__':
    # main()
    unittest.main()

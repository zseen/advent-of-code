import unittest
from typing import List, Dict, Tuple

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"
TEST_INPUT_PART_TWO = "test_input_two.txt"


class MaskingHandler:
    def __init__(self, mask: str, shouldGetMaskedAddresses: bool):
        self.mask = mask
        self._addressesAndValuesWithMaskedValues: List[MemoryAddressToValue] = []
        self.shouldGetMaskedAddresses = shouldGetMaskedAddresses

    def addAddressAndValueWithMaskedValue(self, memoryAddress: int, value: int):
        maskedValue = self._createMaskedValue(value)
        if self.shouldGetMaskedAddresses:
            maskedAddressesFromAddress = self._getPossibleMaskedAddresses(memoryAddress)
            for maskedAddress in maskedAddressesFromAddress:
                memoryAddressToValueWithMaskedValue = MemoryAddressToValueWithMaskedValue(memoryAddress, value,
                                                                                          maskedAddress, maskedValue)
                self._addressesAndValuesWithMaskedValues.append(memoryAddressToValueWithMaskedValue)
        else:
            memoryAddressToValueWithMaskedValue = MemoryAddressToValueWithMaskedValue(memoryAddress, value,
                                                                                      -1, maskedValue)
            self._addressesAndValuesWithMaskedValues.append(memoryAddressToValueWithMaskedValue)

    def getAddressesAndValuesWithMaskedValues(self):
        return self._addressesAndValuesWithMaskedValues

    def _createMaskedValue(self, value) -> int:
        binaryValue: str = "{0:b}".format(value)
        paddedBinaryValue = binaryValue.rjust(36, "0")

        maskedBinaryString = ""
        for i in range(0, len(self.mask)):
            if self.mask[i] == "1":
                maskedBinaryString += "1"
            elif self.mask[i] == "0":
                maskedBinaryString += "0"
            else:
                maskedBinaryString += paddedBinaryValue[i]

        return int(maskedBinaryString, 2)

    def _getSmallestPossibleNumFromMaskedAddress(self, maskedBinaryAddress: str):
        smallestBinaryNumToGetWithFloatingMask: str = maskedBinaryAddress.replace('X', '0')
        return int(smallestBinaryNumToGetWithFloatingMask, 2)

    def _getPossibleMaskedAddresses(self, address):
        addressInBinary: str = ("{0:b}".format(address))
        addressInBinaryPadded = addressInBinary.rjust(36, "0")

        maskedBinaryAddress = ""
        xPositionsInMask = []
        for i in range(0, len(self.mask)):
            if self.mask[i] == "X":
                maskedBinaryAddress += "X"
                xPositionsInMask.append(35 - i)
            elif self.mask[i] == "1":
                maskedBinaryAddress += "1"
            else:
                maskedBinaryAddress += addressInBinaryPadded[i]

        numsToCombineAndAddToSmallestMaskedAddress = [2 ** xPosition for xPosition in xPositionsInMask]
        smallestPossibleNumFromMaskedAddress = self._getSmallestPossibleNumFromMaskedAddress(maskedBinaryAddress)
        allPossibleMaskedAddresses = self.getMaskedAddresses(smallestPossibleNumFromMaskedAddress,
                                                             numsToCombineAndAddToSmallestMaskedAddress)

        return allPossibleMaskedAddresses

    def getMaskedAddresses(self, smallestPossibleNumFromMaskedAddress: int, numsToCombineAndAddToSmallestPossibleNum):
        maskedAddresses = []

        def func(soFar, gen, res):
            if len(gen) == 0:
                res.append(soFar)
                maskedAddresses.append(int(soFar))
                return

            func(soFar + gen[0], gen[1:], res)
            func(soFar, gen[1:], res)

        func(smallestPossibleNumFromMaskedAddress, numsToCombineAndAddToSmallestPossibleNum, [])

        return maskedAddresses


class MaskingHandlersCollectionOperator:
    def __init__(self, allMasksToAddressesAndValues: Dict[str, List[Tuple[int, int]]], shouldMaskAddress: bool):
        self.allMasksToAddressesAndValues = allMasksToAddressesAndValues
        self.shouldMaskAddress = shouldMaskAddress
        self.allMaskingHandlers = self.getAllMaskingHandlers()
        self.allAddressesWithValuesAfterMasking = self.getAllAddressesAndValuesAfterMasking()

    def getAllMaskingHandlers(self):
        allMaskingHandlers: List[MaskingHandler] = []
        for mask, addressesAndValues in self.allMasksToAddressesAndValues.items():
            maskingHandler = MaskingHandler(mask, self.shouldMaskAddress)
            for addressAndValue in addressesAndValues:
                maskingHandler.addAddressAndValueWithMaskedValue(addressAndValue[0], addressAndValue[1])
            allMaskingHandlers.append(maskingHandler)
        return allMaskingHandlers

    def getAllAddressesAndValuesAfterMasking(self):
        allAddressesAndWaluesAfterMasking = []
        for maskingHandler in self.allMaskingHandlers:
            addressesWithValues = maskingHandler.getAddressesAndValuesWithMaskedValues()
            for addressWithValue in addressesWithValues:
                allAddressesAndWaluesAfterMasking.append(addressWithValue)
        return allAddressesAndWaluesAfterMasking

    def sumMaskedValuesInAllAddresses(self):
        addressesWithMaskedValueAlreadySummed = set()
        maskedValuesSum = 0

        for addressesAndValuesWithMaskedValues in self.allAddressesWithValuesAfterMasking[::-1]:
            currentMemoryAddress = addressesAndValuesWithMaskedValues.getMemoryAddress()
            if currentMemoryAddress not in addressesWithMaskedValueAlreadySummed:
                maskedValuesSum += addressesAndValuesWithMaskedValues.getMaskedValue()
            addressesWithMaskedValueAlreadySummed.add(currentMemoryAddress)
        return maskedValuesSum

    def sumAllUniqueMaskedAddresses(self):
        maskedAddressesAlreadyVisited = set()
        maskedAddressValueSum = 0
        for addressesWithValue in self.allAddressesWithValuesAfterMasking[::-1]:
            currentAddress = addressesWithValue.getMaskedAddress()
            if currentAddress not in maskedAddressesAlreadyVisited:
                maskedAddressValueSum += addressesWithValue.getValue()
            maskedAddressesAlreadyVisited.add(currentAddress)

        return maskedAddressValueSum


class MemoryAddressToValueWithMaskedValue:
    def __init__(self, memoryAddress: int, value: int, maskedAddress: int, maskedValue: int):
        self._memoryAddress = memoryAddress
        self._value = value
        self._maskedAddress = maskedAddress
        self._maskedValue = maskedValue

    def getMemoryAddress(self):
        return self._memoryAddress

    def getValue(self):
        return self._value

    def getMaskedAddress(self):
        return self._maskedAddress

    def getMaskedValue(self):
        return self._maskedValue


def getAllMasksToAddressesAndValues(inputFile: str):
    allMaskingData = {}
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" = ")
            if len(line) > 1:
                if line[0] == "mask":
                    mask = line[1].strip("\n")
                    allMaskingData[mask] = []
                else:
                    memoryAddressDigits = []
                    for char in line[0]:
                        if char.isdigit():
                            memoryAddressDigits.append(char)
                    memoryAddress = int("".join(memoryAddressDigits))
                    value = int(line[1].strip("\n"))
                    allMaskingData[mask].append((memoryAddress, value))

    return allMaskingData


allMasksToAddressesAndValues = getAllMasksToAddressesAndValues(TEST_INPUT)
firstPart = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues, False)
x = firstPart.sumMaskedValuesInAllAddresses()
print(x)  # 165

allMasksToAddressesAndValues = getAllMasksToAddressesAndValues(TEST_INPUT_PART_TWO)
secondPart = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues, True)
x = secondPart.sumAllUniqueMaskedAddresses()
print(x)  # 208

mainRunPartOne = getAllMasksToAddressesAndValues(INPUT_FILE)

c = MaskingHandlersCollectionOperator(mainRunPartOne, False)
print(c.sumMaskedValuesInAllAddresses())  # 7997531787333

v = MaskingHandlersCollectionOperator(mainRunPartOne, True)
print(v.sumAllUniqueMaskedAddresses())  # 3564822193820

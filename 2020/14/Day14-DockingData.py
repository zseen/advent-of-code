import unittest
from typing import List, Dict, Tuple

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"
TEST_INPUT_PART_TWO = "test_input_two.txt"


class MemoryAddressAndValue:
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


class MaskingHandler:
    def __init__(self, mask: str, shouldMaskAddress: bool):
        self.mask = mask
        self._addressesAndValuesAfterMasking: List[MemoryAddressAndValue] = []
        self.shouldMaskAddress = shouldMaskAddress

    def getAddressesAndValuesAfterMasking(self) -> List[MemoryAddressAndValue]:
        return self._addressesAndValuesAfterMasking

    def addAddressAndValueForMasking(self, memoryAddress: int, value: int) -> None:
        maskedValue: int = self._createMaskedValue(value)
        if self.shouldMaskAddress:
            maskedAddressesFromAddress = self._getPossibleMaskedAddresses(memoryAddress)
            for maskedAddress in maskedAddressesFromAddress:
                memoryAddressAndValueWithBothMasked = MemoryAddressAndValue(memoryAddress, value,
                                                                            maskedAddress, maskedValue)
                self._addressesAndValuesAfterMasking.append(memoryAddressAndValueWithBothMasked)
        else:
            memoryAddressAndValueWithMaskedValue = MemoryAddressAndValue(memoryAddress, value,
                                                                         -1, maskedValue)
            self._addressesAndValuesAfterMasking.append(memoryAddressAndValueWithMaskedValue)

    def _createMaskedValue(self, value: int) -> int:
        binaryValue: str = "{0:b}".format(value)
        paddedBinaryValue: str = binaryValue.rjust(36, "0")

        maskedBinaryString = ""
        for i in range(0, len(self.mask)):
            if self.mask[i] == "1" or self.mask[i] == "0":
                maskedBinaryString += self.mask[i]
            else:
                maskedBinaryString += paddedBinaryValue[i]

        return int(maskedBinaryString, 2)

    def _getPossibleMaskedAddresses(self, address):
        maskedBinaryAddress: str = self._createMaskedAddress(address)
        smallestPossibleNumFromMaskedAddress = self._getSmallestPossibleNumFromMaskedAddress(maskedBinaryAddress)
        numsToCombineAndAddToSmallestMaskedAddress = [2 ** xPosition for xPosition in self._getXPositionsInMask()]
        return self._getMaskedAddresses(smallestPossibleNumFromMaskedAddress,
                                        numsToCombineAndAddToSmallestMaskedAddress)

    def _createMaskedAddress(self, address: int) -> str:
        addressInBinary: str = ("{0:b}".format(address))
        addressInBinaryPadded = addressInBinary.rjust(36, "0")

        maskedBinaryAddress = ""
        for i in range(0, len(self.mask)):
            if self.mask[i] == "X" or self.mask[i] == "1":
                maskedBinaryAddress += self.mask[i]
            else:
                maskedBinaryAddress += addressInBinaryPadded[i]

        return maskedBinaryAddress

    def _getSmallestPossibleNumFromMaskedAddress(self, maskedBinaryAddress: str) -> int:
        return int(maskedBinaryAddress.replace('X', '0'), 2)

    def _getXPositionsInMask(self) -> List[int]:
        return [35 - i for i in range(0, len(self.mask)) if self.mask[i] == "X"]

    def _getMaskedAddresses(self, smallestPossibleNumFromMaskedAddress: int,
                            numsToCombineAndAddToSmallestPossibleNum: List[int]) -> List[int]:
        maskedAddresses = []

        def generatePossibleNums(sumSoFar: int, availableNums: List[int]):
            if len(availableNums) == 0:
                maskedAddresses.append(int(sumSoFar))
                return

            generatePossibleNums(sumSoFar + availableNums[0], availableNums[1:])
            generatePossibleNums(sumSoFar, availableNums[1:])

        generatePossibleNums(smallestPossibleNumFromMaskedAddress, numsToCombineAndAddToSmallestPossibleNum)
        return maskedAddresses


class MaskingHandlersCollectionOperator:
    def __init__(self, allMaskToAddressesAndValues: Dict[str, List[Tuple[int, int]]], shouldMaskAddress: bool):
        self.allMaskToAddressesAndValues = allMaskToAddressesAndValues
        self.shouldMaskAddress = shouldMaskAddress
        self.allMaskingHandlers = self._createAllMaskingHandlers()
        self.allAddressesWithValuesAfterMasking = self._getAllAddressesAndValuesAfterMasking()

    def sumMaskedValuesInAddresses(self) -> int:
        addressesWithMaskedValueAlreadySummed = set()
        maskedValuesSum = 0

        for addressesAndValuesWithMaskedValues in self.allAddressesWithValuesAfterMasking:
            currentMemoryAddress = addressesAndValuesWithMaskedValues.getMemoryAddress()
            if currentMemoryAddress not in addressesWithMaskedValueAlreadySummed:
                maskedValuesSum += addressesAndValuesWithMaskedValues.getMaskedValue()
            addressesWithMaskedValueAlreadySummed.add(currentMemoryAddress)

        return maskedValuesSum

    def sumValuesInMaskedAddresses(self) -> int:
        maskedAddressesWithAlreadySummedValues = set()
        maskedAddressValueSum = 0

        for addressesWithValue in self.allAddressesWithValuesAfterMasking:
            currentMaskedAddress = addressesWithValue.getMaskedAddress()
            if currentMaskedAddress not in maskedAddressesWithAlreadySummedValues:
                maskedAddressValueSum += addressesWithValue.getValue()
            maskedAddressesWithAlreadySummedValues.add(currentMaskedAddress)

        return maskedAddressValueSum

    def _createAllMaskingHandlers(self) -> List[MaskingHandler]:
        allMaskingHandlers: List[MaskingHandler] = []
        for mask, addressesAndValues in self.allMaskToAddressesAndValues.items():
            maskingHandler = MaskingHandler(mask, self.shouldMaskAddress)
            for addressAndValue in addressesAndValues:
                maskingHandler.addAddressAndValueForMasking(addressAndValue[0], addressAndValue[1])
            allMaskingHandlers.append(maskingHandler)
        return allMaskingHandlers

    def _getAllAddressesAndValuesAfterMasking(self) -> List[MemoryAddressAndValue]:
        allAddressesAndWaluesAfterMasking: List[MemoryAddressAndValue] = []
        for maskingHandler in self.allMaskingHandlers:
            addressesWithValues = maskingHandler.getAddressesAndValuesAfterMasking()
            for addressWithValue in addressesWithValues:
                allAddressesAndWaluesAfterMasking.append(addressWithValue)
        return allAddressesAndWaluesAfterMasking[::-1]


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
                    memoryAddressDigits = [char for char in line[0] if char.isdigit()]
                    memoryAddress = int("".join(memoryAddressDigits))
                    value = int(line[1].strip("\n"))
                    allMaskingData[mask].append((memoryAddress, value))

    return allMaskingData


def main():
    allMasksToAddressesAndValues: Dict[str, List[Tuple[int, int]]] = getAllMasksToAddressesAndValues(INPUT_FILE)

    maskingOperatorWithoutMaskingAddress = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                             shouldMaskAddress=False)
    print(maskingOperatorWithoutMaskingAddress.sumMaskedValuesInAddresses())  # 7997531787333

    maskingOperatorWithMaskingAddresses = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                            shouldMaskAddress=True)
    print(maskingOperatorWithMaskingAddresses.sumValuesInMaskedAddresses())  # 3564822193820


class MaskingOperationsTester(unittest.TestCase):
    def test_sumMaskedValuesInAddresses_addressesNotMasked_correctSumReturned(self):
        allMasksToAddressesAndValues: Dict[str, List[Tuple[int, int]]] = getAllMasksToAddressesAndValues(TEST_INPUT)
        maskingOperatorWithoutMaskingAddress = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                                 shouldMaskAddress=False)
        self.assertEqual(165, maskingOperatorWithoutMaskingAddress.sumMaskedValuesInAddresses())

    def test_sumValuesInMaskedAddresses_valuesNotMasked_correctSumReturned(self):
        allMasksToAddressesAndValues: Dict[str, List[Tuple[int, int]]] = getAllMasksToAddressesAndValues(
            TEST_INPUT_PART_TWO)
        maskingOperatorWithMaskingAddress = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                              shouldMaskAddress=True)
        self.assertEqual(208, maskingOperatorWithMaskingAddress.sumValuesInMaskedAddresses())


if __name__ == '__main__':
    # main()
    unittest.main()

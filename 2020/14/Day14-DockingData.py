import unittest
from typing import List, Dict, Tuple
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"
TEST_INPUT_PART_TWO = "test_input_two.txt"
MASK_LENGTH = 36


class MaskingType(Enum):
    ADDRESS = "address"
    VALUE = "valueMaskedMemoryItem"


class MemoryItem:
    def __init__(self, addressMaskedMemoryItem: int, valueMaskedMemoryItem: int):
        self.addressMaskedMemoryItem = addressMaskedMemoryItem
        self.valueMaskedMemoryItem = valueMaskedMemoryItem


class MaskingHandler:
    def __init__(self, mask: str, maskingType: MaskingType):
        self._mask = mask
        self._maskingType = maskingType

    def getMaskedAddressAndValue(self, addressAndValue: MemoryItem) -> List[MemoryItem]:
        return self.addAddressAndValueForMasking(addressAndValue)

    def addAddressAndValueForMasking(self, addressAndValue: MemoryItem) -> List[MemoryItem]:
        if self._maskingType == MaskingType.ADDRESS:
            maskedAddressesFromAddress = self._getAllMaskedAddresses(addressAndValue.addressMaskedMemoryItem)
            return [MemoryItem(maskedAddress, addressAndValue.valueMaskedMemoryItem) for maskedAddress in maskedAddressesFromAddress]
        else:
            maskedValue: int = self._createMaskedValue(addressAndValue.valueMaskedMemoryItem)
            return [MemoryItem(addressAndValue.addressMaskedMemoryItem, maskedValue)]


    def _createMaskedValue(self, valueMaskedMemoryItem: int) -> int:
        binaryValue: str = "{0:b}".format(valueMaskedMemoryItem)
        paddedBinaryValue: str = binaryValue.rjust(MASK_LENGTH, "0")

        maskedBinaryString = ""
        for i in range(0, len(self._mask)):
            maskedBinaryString += self.getNextMaskedChar(paddedBinaryValue, i, "1", "0")

        return int(maskedBinaryString, 2)

    def getNextMaskedChar(self, originalInput: str, charPosition: int, fistCharToCompareWith: str, secondCharToCompareWith: str) -> str:
        if self._mask[charPosition] == fistCharToCompareWith or self._mask[charPosition] == secondCharToCompareWith:
            return self._mask[charPosition]

        return originalInput[charPosition]


    def _getAllMaskedAddresses(self, address):
        maskedBinaryAddress: str = self._createMaskedAddress(address)
        smallestPossibleNumFromMaskedAddress = self._getSmallestPossibleNumFromMaskedAddress(maskedBinaryAddress)
        numsToCombineAndAddToSmallestMaskedAddress = [2 ** xPosition for xPosition in self._getXPositionsInMask()]
        return self._generateMaskedAddresses(smallestPossibleNumFromMaskedAddress,
                                             numsToCombineAndAddToSmallestMaskedAddress)

    def _createMaskedAddress(self, address: int) -> str:
        addressInBinary: str = ("{0:b}".format(address))
        addressInBinaryPadded = addressInBinary.rjust(MASK_LENGTH, "0")

        maskedBinaryAddress = ""
        for i in range(0, len(self._mask)):
            maskedBinaryAddress += self.getNextMaskedChar(addressInBinaryPadded, i, "X", "1")

        return maskedBinaryAddress

    def _getSmallestPossibleNumFromMaskedAddress(self, maskedBinaryAddress: str) -> int:
        return int(maskedBinaryAddress.replace('X', '0'), 2)

    def _getXPositionsInMask(self) -> List[int]:
        #return [i for i in range(MASK_LENGTH - 1, -1, -1) if self._mask[i] == "X"]
        return [(MASK_LENGTH - 1 - i) for i in range(0, MASK_LENGTH) if self._mask[i] == "X"]

    def _generateMaskedAddresses(self, smallestPossibleNumFromMaskedAddress: int,
                                 numsToCombineAndAddToSmallestPossibleNum: List[int]) -> List[int]:
        maskedAddresses = []
        self._generateMaskedAddressesRecursive(smallestPossibleNumFromMaskedAddress, numsToCombineAndAddToSmallestPossibleNum,
                                       maskedAddresses)
        return maskedAddresses

    def _generateMaskedAddressesRecursive(self, sumSoFar: int, availableNums: List[int], maskedAddresses: List[int]) -> None:
        if len(availableNums) == 0:
            maskedAddresses.append(int(sumSoFar))
            return

        self._generateMaskedAddressesRecursive(sumSoFar + availableNums[0], availableNums[1:], maskedAddresses)
        self._generateMaskedAddressesRecursive(sumSoFar, availableNums[1:], maskedAddresses)


class MaskingHandlersCollectionOperator:
    def __init__(self, _allMaskToAddressesAndValues: Dict[str, List[MemoryItem]], maskingType: MaskingType):
        self._allMaskToAddressesAndValues = _allMaskToAddressesAndValues
        self._maskingType = maskingType
        self._allAddressesWithValuesAfterMasking: Dict[int, int] = self.getAllMaskedItems()

    def sumValuesInAddresses(self) -> int:
        maskedValuesSum = 0
        for address, valueMaskedMemoryItem in self._allAddressesWithValuesAfterMasking.items():
            maskedValuesSum += valueMaskedMemoryItem

        return maskedValuesSum

    def getAllMaskedItems(self) -> Dict[int, int]:
        allAddressesAndValuesAfterMasking: Dict[int, int] = dict()
        for mask, addressesAndValues in self._allMaskToAddressesAndValues.items():
            maskingHandler = MaskingHandler(mask, self._maskingType)
            for addressAndValue in addressesAndValues:
                maskedAddressesAndValues = maskingHandler.getMaskedAddressAndValue(addressAndValue)
                for maskedAddressAndValue in maskedAddressesAndValues:
                    allAddressesAndValuesAfterMasking[maskedAddressAndValue.addressMaskedMemoryItem] = maskedAddressAndValue.valueMaskedMemoryItem
        return allAddressesAndValuesAfterMasking


def getAllMasksToAddressesAndValues(inputFile: str):
    allMaskingData: Dict[str, List[MemoryItem]] = {}
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" = ")
            if len(line) <= 1:
                raise ValueError("Double check input format.")
            
            if line[0] == "mask":
                mask = line[1].strip("\n")
                allMaskingData[mask] = []
            else:
                memoryAddressDigits = [char for char in line[0] if char.isdigit()]
                memoryAddress = int("".join(memoryAddressDigits))
                value = int(line[1].strip("\n"))
                allMaskingData[mask].append((MemoryItem(memoryAddress, value)))

    return allMaskingData


def main():
    allMasksToAddressesAndValues: Dict[str, List[MemoryItem]] = getAllMasksToAddressesAndValues(INPUT_FILE)

    maskingOperatorWithoutMaskingAddress = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                             MaskingType.VALUE)
    print(maskingOperatorWithoutMaskingAddress.sumValuesInAddresses())  # 7997531787333

    maskingOperatorWithMaskingAddresses = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                            MaskingType.ADDRESS)
    print(maskingOperatorWithMaskingAddresses.sumValuesInAddresses())  # 3564822193820


class MaskingOperationsTester(unittest.TestCase):
    def test_sumValuesInAddresses_addressesNotMasked_correctSumReturned(self):
        allMasksToAddressesAndValues: Dict[str, List[MemoryItem]] = getAllMasksToAddressesAndValues(TEST_INPUT)
        maskingOperatorWithoutMaskingAddress = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                                 MaskingType.VALUE)
        self.assertEqual(165, maskingOperatorWithoutMaskingAddress.sumValuesInAddresses())

    def test_sumValuesInAddresses_valuesNotMasked_correctSumReturned(self):
        allMasksToAddressesAndValues: Dict[str, List[MemoryItem]] = getAllMasksToAddressesAndValues(
            TEST_INPUT_PART_TWO)
        maskingOperatorWithMaskingAddress = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                              MaskingType.ADDRESS)
        self.assertEqual(208, maskingOperatorWithMaskingAddress.sumValuesInAddresses())


if __name__ == '__main__':
    main()
    unittest.main()

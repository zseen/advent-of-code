import unittest
from typing import List, Dict, Tuple
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"
TEST_INPUT_PART_TWO = "test_input_two.txt"
MASK_LENGTH = 36


class MaskingType(Enum):
    ADDRESS = "memoryAddress"
    VALUE = "valueMaskedMemoryItem"


class MemoryItem:
    def __init__(self, memoryAddressMaskedMemoryItem: int, valueMaskedMemoryItem: int):
        self.memoryAddressMaskedMemoryItem = memoryAddressMaskedMemoryItem
        self.valueMaskedMemoryItem = valueMaskedMemoryItem


class MaskingHandler:
    def __init__(self, mask: str, maskingType: MaskingType):
        self._mask = mask
        self._maskingType = maskingType

    def getMaskedMemoryItems(self, memoryAddressAndValue: MemoryItem) -> List[MemoryItem]:
        return self.addMemoryAddressAndValueForMasking(memoryAddressAndValue)

    def addMemoryAddressAndValueForMasking(self, memoryAddressAndValue: MemoryItem) -> List[MemoryItem]:
        if self._maskingType == MaskingType.ADDRESS:
            maskedMemoryAddressesFromMemoryAddress = self._getAllMaskedMemoryAddresses(
                memoryAddressAndValue.memoryAddressMaskedMemoryItem)
            return [MemoryItem(maskedMemoryAddress, memoryAddressAndValue.valueMaskedMemoryItem) for maskedMemoryAddress
                    in maskedMemoryAddressesFromMemoryAddress]
        else:
            maskedValue: int = self._createMaskedValue(memoryAddressAndValue.valueMaskedMemoryItem)
            return [MemoryItem(memoryAddressAndValue.memoryAddressMaskedMemoryItem, maskedValue)]

    def _createMaskedValue(self, valueMaskedMemoryItem: int) -> int:
        binaryValue: str = "{0:b}".format(valueMaskedMemoryItem)
        paddedBinaryValue: str = binaryValue.rjust(MASK_LENGTH, "0")

        maskedBinaryString = ""
        for i in range(0, MASK_LENGTH):
            maskedBinaryString += self.getNextMaskedChar(paddedBinaryValue, i, "1", "0")

        return int(maskedBinaryString, 2)

    def getNextMaskedChar(self, maskedMemoryItemPadded: str, charPosition: int, fistCharToCompareWith: str,
                          secondCharToCompareWith: str) -> str:
        if self._mask[charPosition] == fistCharToCompareWith or self._mask[charPosition] == secondCharToCompareWith:
            return self._mask[charPosition]

        return maskedMemoryItemPadded[charPosition]

    def _getAllMaskedMemoryAddresses(self, memoryAddress: int) -> List[int]:
        maskedBinaryMemoryAddress: str = self._createMaskedMemoryAddress(memoryAddress)
        smallestPossibleNumFromMaskedMemoryAddress = self._getSmallestPossibleNumFromMaskedMemoryAddress(
            maskedBinaryMemoryAddress)
        numsToCombineAndAddToSmallestMaskedMemoryAddress = [2 ** xPosition for xPosition in self._getXPositionsInMask()]
        return self._generateMaskedMemoryAddresses(smallestPossibleNumFromMaskedMemoryAddress,
                                                   numsToCombineAndAddToSmallestMaskedMemoryAddress)

    def _createMaskedMemoryAddress(self, memoryAddress: int) -> str:
        memoryAddressInBinary: str = ("{0:b}".format(memoryAddress))
        memoryAddressInBinaryPadded = memoryAddressInBinary.rjust(MASK_LENGTH, "0")

        maskedBinaryMemoryAddress = ""
        for i in range(0, MASK_LENGTH):
            maskedBinaryMemoryAddress += self.getNextMaskedChar(memoryAddressInBinaryPadded, i, "X", "1")

        return maskedBinaryMemoryAddress

    def _getSmallestPossibleNumFromMaskedMemoryAddress(self, maskedBinaryMemoryAddress: str) -> int:
        return int(maskedBinaryMemoryAddress.replace('X', '0'), 2)

    def _getXPositionsInMask(self) -> List[int]:
        # return [i for i in range(MASK_LENGTH - 1, -1, -1) if self._mask[i] == "X"]
        return [(MASK_LENGTH - 1 - i) for i in range(0, MASK_LENGTH) if self._mask[i] == "X"]

    def _generateMaskedMemoryAddresses(self, smallestPossibleNumFromMaskedMemoryAddress: int,
                                       numsToCombineAndAddToSmallestPossibleNum: List[int]) -> List[int]:
        maskedMemoryAddresses = []
        self._generateMaskedMemoryAddressesRecursive(smallestPossibleNumFromMaskedMemoryAddress,
                                                     numsToCombineAndAddToSmallestPossibleNum,
                                                     maskedMemoryAddresses)
        return maskedMemoryAddresses

    def _generateMaskedMemoryAddressesRecursive(self, sumSoFar: int, availableNums: List[int],
                                                maskedMemoryAddresses: List[int]) -> None:
        if len(availableNums) == 0:
            maskedMemoryAddresses.append(int(sumSoFar))
            return

        self._generateMaskedMemoryAddressesRecursive(sumSoFar + availableNums[0], availableNums[1:],
                                                     maskedMemoryAddresses)
        self._generateMaskedMemoryAddressesRecursive(sumSoFar, availableNums[1:], maskedMemoryAddresses)


class MaskingHandlersCollectionOperator:
    def __init__(self, allMemoryItems: Dict[str, List[MemoryItem]], maskingType: MaskingType):
        self._allMemoryItems = allMemoryItems
        self._maskingType = maskingType
        self._allMaskedMemoryItems: Dict[int, int] = self.getAllMaskedItems()

    def sumValuesInMemoryAddresses(self) -> int:
        maskedValuesSum = 0
        for memoryAddress, valueMaskedMemoryItem in self._allMaskedMemoryItems.items():
            maskedValuesSum += valueMaskedMemoryItem

        return maskedValuesSum

    def getAllMaskedItems(self) -> Dict[int, int]:
        allMaskedMemoryItems: Dict[int, int] = dict()
        for mask, memoryItems in self._allMemoryItems.items():
            maskingHandler = MaskingHandler(mask, self._maskingType)
            for memoryItem in memoryItems:
                maskedMemoryItems = maskingHandler.getMaskedMemoryItems(memoryItem)
                for maskedMemoryItem in maskedMemoryItems:
                    allMaskedMemoryItems[
                        maskedMemoryItem.memoryAddressMaskedMemoryItem] = maskedMemoryItem.valueMaskedMemoryItem
        return allMaskedMemoryItems


def getAllMasksToMemoryItems(inputFile: str):
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
    allMasksToMemoryItems: Dict[str, List[MemoryItem]] = getAllMasksToMemoryItems(INPUT_FILE)

    maskingOperatorWithoutMaskingMemoryAddress = MaskingHandlersCollectionOperator(allMasksToMemoryItems,
                                                                                   MaskingType.VALUE)
    print(maskingOperatorWithoutMaskingMemoryAddress.sumValuesInMemoryAddresses())  # 7997531787333

    maskingOperatorWithMaskingMemoryAddresses = MaskingHandlersCollectionOperator(allMasksToMemoryItems,
                                                                                  MaskingType.ADDRESS)
    print(maskingOperatorWithMaskingMemoryAddresses.sumValuesInMemoryAddresses())  # 3564822193820


class MaskingOperationsTester(unittest.TestCase):
    def test_sumValuesInMemoryAddresses_memoryAddressesNotMasked_correctSumReturned(self):
        allMasksToMemoryItems: Dict[str, List[MemoryItem]] = getAllMasksToMemoryItems(TEST_INPUT)
        maskingOperatorWithoutMaskingMemoryAddress = MaskingHandlersCollectionOperator(allMasksToMemoryItems,
                                                                                       MaskingType.VALUE)
        self.assertEqual(165, maskingOperatorWithoutMaskingMemoryAddress.sumValuesInMemoryAddresses())

    def test_sumValuesInMemoryAddresses_valuesNotMasked_correctSumReturned(self):
        allMasksToMemoryItems: Dict[str, List[MemoryItem]] = getAllMasksToMemoryItems(
            TEST_INPUT_PART_TWO)
        maskingOperatorWithMaskingMemoryAddress = MaskingHandlersCollectionOperator(allMasksToMemoryItems,
                                                                                    MaskingType.ADDRESS)
        self.assertEqual(208, maskingOperatorWithMaskingMemoryAddress.sumValuesInMemoryAddresses())


if __name__ == '__main__':
    # main()
    unittest.main()

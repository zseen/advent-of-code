import unittest
from typing import List, Dict, Tuple
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"
TEST_INPUT_PART_TWO = "test_input_two.txt"
MASK_LENGTH = 36


class MaskingType(Enum):
    MEMORY_ADDRESS = "memoryAddress"
    VALUE = "value"


class MemoryItem:
    def __init__(self, memoryAddress: int, value: int):
        self.memoryAddress = memoryAddress
        self.value = value


class MaskingHandler:
    def __init__(self, mask: str, maskingType: MaskingType):
        self._mask = mask
        self._maskingType = maskingType

    def getMaskedMemoryItems(self, memoryItem: MemoryItem) -> List[MemoryItem]:
        if self._maskingType == MaskingType.MEMORY_ADDRESS:
            maskedMemoryAddresses = self._getAllMaskedMemoryAddresses(memoryItem.memoryAddress)
            return [MemoryItem(maskedMemoryAddress, memoryItem.value) for maskedMemoryAddress in maskedMemoryAddresses]
        else:
            maskedValue: int = self._createMaskedValue(memoryItem.value)
            return [MemoryItem(memoryItem.memoryAddress, maskedValue)]

    def _createMaskedValue(self, value: int) -> int:
        binaryValue: str = "{0:b}".format(value)
        paddedBinaryValue: str = binaryValue.rjust(MASK_LENGTH, "0")

        maskedBinaryString = ""
        for i in range(0, MASK_LENGTH):
            maskedBinaryString += self.getNextMaskedChar(paddedBinaryValue, i, ["1", "0"])

        return int(maskedBinaryString, 2)

    def getNextMaskedChar(self, maskedMemoryItemPadded: str, charPosition: int, charsToCompareWith: List[str]) -> str:
        if self._mask[charPosition] in charsToCompareWith:
            return self._mask[charPosition]

        return maskedMemoryItemPadded[charPosition]

    def _getAllMaskedMemoryAddresses(self, memoryAddress: int) -> List[int]:
        maskedBinaryMemoryAddress: str = self._createMaskedMemoryAddress(memoryAddress)
        smallestPossibleNum = self._getSmallestPossibleNumFromMaskedMemoryAddress(
            maskedBinaryMemoryAddress)
        numsToCombineAndAddToSmallestMaskedMemoryAddress = [2 ** xPosition for xPosition in self._getXPositionsInMask()]
        return self._generateMaskedMemoryAddresses(smallestPossibleNum, numsToCombineAndAddToSmallestMaskedMemoryAddress)

    def _createMaskedMemoryAddress(self, memoryAddress: int) -> str:
        memoryAddressInBinary: str = ("{0:b}".format(memoryAddress))
        memoryAddressInBinaryPadded = memoryAddressInBinary.rjust(MASK_LENGTH, "0")

        maskedBinaryMemoryAddress = ""
        for i in range(0, MASK_LENGTH):
            maskedBinaryMemoryAddress += self.getNextMaskedChar(memoryAddressInBinaryPadded, i, ["X", "1"])

        return maskedBinaryMemoryAddress

    def _getSmallestPossibleNumFromMaskedMemoryAddress(self, maskedBinaryMemoryAddress: str) -> int:
        return int(maskedBinaryMemoryAddress.replace('X', '0'), 2)

    def _getXPositionsInMask(self) -> List[int]:
        return [(MASK_LENGTH - 1 - i) for i in range(0, MASK_LENGTH) if self._mask[i] == "X"]

    def _generateMaskedMemoryAddresses(self, smallestPossibleNumFromMaskedMemoryAddress: int, numsToCombineAndAddToSmallestPossibleNum: List[int]) -> \
    List[int]:
        maskedMemoryAddresses = []
        self._generateMaskedMemoryAddressesRecursive(smallestPossibleNumFromMaskedMemoryAddress, numsToCombineAndAddToSmallestPossibleNum,
                                                     maskedMemoryAddresses)
        return maskedMemoryAddresses

    def _generateMaskedMemoryAddressesRecursive(self, sumSoFar: int, availableNums: List[int], maskedMemoryAddresses: List[int]) -> None:
        if len(availableNums) == 0:
            maskedMemoryAddresses.append(int(sumSoFar))
            return

        self._generateMaskedMemoryAddressesRecursive(sumSoFar + availableNums[0], availableNums[1:], maskedMemoryAddresses)
        self._generateMaskedMemoryAddressesRecursive(sumSoFar, availableNums[1:], maskedMemoryAddresses)


class MaskingInstructionExecutor:
    def __init__(self, allMemoryItems: Dict[str, List[MemoryItem]], maskingType: MaskingType):
        self._allMemoryItems = allMemoryItems
        self._maskingType = maskingType
        self._memory: Dict[int, int] = {}

    def sumValuesInMemoryAddresses(self) -> int:
        maskedValuesSum = 0
        for memoryAddress, value in self._memory.items():
            maskedValuesSum += value

        return maskedValuesSum

    def populateMemory(self) -> None:
        for mask, memoryItems in self._allMemoryItems.items():
            maskingHandler = MaskingHandler(mask, self._maskingType)
            self._writeAllMaskedItemsToMemory(
                memoryItems, maskingHandler)

    def _writeAllMaskedItemsToMemory(self, memoryItems: List[MemoryItem], maskingHandler: MaskingHandler) -> None:
        for memoryItem in memoryItems:
            maskedMemoryItems = maskingHandler.getMaskedMemoryItems(memoryItem)
            self._writeMaskedMemoryItemsToMemory(maskedMemoryItems)

    def _writeMaskedMemoryItemsToMemory(self, maskedMemoryItems) -> None:
        for maskedMemoryItem in maskedMemoryItems:
            self._memory[maskedMemoryItem.memoryAddress] = maskedMemoryItem.value


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

    maskingOperatorWithoutMaskingMemoryAddress = MaskingInstructionExecutor(allMasksToMemoryItems, MaskingType.VALUE)
    maskingOperatorWithoutMaskingMemoryAddress.populateMemory()
    print(maskingOperatorWithoutMaskingMemoryAddress.sumValuesInMemoryAddresses())  # 7997531787333

    maskingOperatorWithMaskingMemoryAddresses = MaskingInstructionExecutor(allMasksToMemoryItems, MaskingType.MEMORY_ADDRESS)
    maskingOperatorWithoutMaskingMemoryAddress.populateMemory()
    print(maskingOperatorWithMaskingMemoryAddresses.sumValuesInMemoryAddresses())  # 3564822193820


class MaskingOperationsTester(unittest.TestCase):
    def test_sumValuesInMemoryAddresses_memoryAddressesNotMasked_correctSumReturned(self):
        allMasksToMemoryItems: Dict[str, List[MemoryItem]] = getAllMasksToMemoryItems(TEST_INPUT)
        maskingOperatorWithoutMaskingMemoryAddress = MaskingInstructionExecutor(allMasksToMemoryItems, MaskingType.VALUE)
        maskingOperatorWithoutMaskingMemoryAddress.populateMemory()
        self.assertEqual(165, maskingOperatorWithoutMaskingMemoryAddress.sumValuesInMemoryAddresses())

    def test_sumValuesInMemoryAddresses_valuesNotMasked_correctSumReturned(self):
        allMasksToMemoryItems: Dict[str, List[MemoryItem]] = getAllMasksToMemoryItems(TEST_INPUT_PART_TWO)
        maskingOperatorWithMaskingMemoryAddress = MaskingInstructionExecutor(allMasksToMemoryItems, MaskingType.MEMORY_ADDRESS)
        maskingOperatorWithMaskingMemoryAddress.populateMemory()
        self.assertEqual(208, maskingOperatorWithMaskingMemoryAddress.sumValuesInMemoryAddresses())


if __name__ == '__main__':
    # main()
    unittest.main()

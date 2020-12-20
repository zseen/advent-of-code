import unittest
from typing import List, Dict, Tuple
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"
TEST_INPUT_PART_TWO = "test_input_two.txt"
MASK_LENGTH = 36

RawAddressAndValue = Tuple[int, int]
AllRawAddressesAndValues = List[RawAddressAndValue]


class MaskingType(Enum):
    ADDRESS = "address"
    VALUE = "value"


class MemoryAddressAndValue:
    def __init__(self, memoryAddress: int, value: int):
        self.memoryAddress = memoryAddress
        self.value = value


class MaskingHandler:
    def __init__(self, mask: str, itemToMask: MaskingType):
        self.mask = mask
        self._addressesAndValuesAfterMasking: List[MemoryAddressAndValue] = []
        self.itemToMask = itemToMask

    def getMaskedAddressAndValue(self, addressAndValue) -> List[MemoryAddressAndValue]:
        self.addAddressAndValueForMasking(addressAndValue)
        return self._addressesAndValuesAfterMasking

    def addAddressAndValueForMasking(self, addressAndValue: RawAddressAndValue) -> None:
        if self.itemToMask == MaskingType.ADDRESS:
            maskedAddressesFromAddress = self._getAllMaskedAddresses(addressAndValue[0])
            for maskedAddress in maskedAddressesFromAddress:
                maskedMemoryAddressAndValue = MemoryAddressAndValue(maskedAddress, addressAndValue[1])
                self._addressesAndValuesAfterMasking.append(maskedMemoryAddressAndValue)
        else:
            maskedValue: int = self._createMaskedValue(addressAndValue[1])
            memoryAddressAndMaskedValue = MemoryAddressAndValue(addressAndValue[0], maskedValue)
            self._addressesAndValuesAfterMasking.append(memoryAddressAndMaskedValue)

    def _createMaskedValue(self, value: int) -> int:
        binaryValue: str = "{0:b}".format(value)
        paddedBinaryValue: str = binaryValue.rjust(MASK_LENGTH, "0")

        maskedBinaryString = ""
        for i in range(0, len(self.mask)):
            if self.mask[i] == "1" or self.mask[i] == "0":
                maskedBinaryString += self.mask[i]
            else:
                maskedBinaryString += paddedBinaryValue[i]

        return int(maskedBinaryString, 2)

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
        for i in range(0, len(self.mask)):
            if self.mask[i] == "X" or self.mask[i] == "1":
                maskedBinaryAddress += self.mask[i]
            else:
                maskedBinaryAddress += addressInBinaryPadded[i]

        return maskedBinaryAddress

    def _getSmallestPossibleNumFromMaskedAddress(self, maskedBinaryAddress: str) -> int:
        return int(maskedBinaryAddress.replace('X', '0'), 2)

    def _getXPositionsInMask(self) -> List[int]:
        return [(MASK_LENGTH - 1 - i) for i in range(0, len(self.mask)) if self.mask[i] == "X"]

    def _generateMaskedAddresses(self, smallestPossibleNumFromMaskedAddress: int,
                                 numsToCombineAndAddToSmallestPossibleNum: List[int]) -> List[int]:
        maskedAddresses = []
        self.generatePossibleAddresses(smallestPossibleNumFromMaskedAddress, numsToCombineAndAddToSmallestPossibleNum,
                                       maskedAddresses)
        return maskedAddresses

    def generatePossibleAddresses(self, sumSoFar: int, availableNums: List[int], maskedAddresses: List[int]) -> List[
        int]:
        if len(availableNums) == 0:
            maskedAddresses.append(int(sumSoFar))
            return maskedAddresses

        self.generatePossibleAddresses(sumSoFar + availableNums[0], availableNums[1:], maskedAddresses)
        self.generatePossibleAddresses(sumSoFar, availableNums[1:], maskedAddresses)


class MaskingHandlersCollectionOperator:
    def __init__(self, allMaskToAddressesAndValues: Dict[str, AllRawAddressesAndValues], itemToMask: MaskingType):
        self.allMaskToAddressesAndValues = allMaskToAddressesAndValues
        self.itemToMask = itemToMask
        self.allAddressesWithValuesAfterMasking: Dict[int, int] = self.getAllMaskedItems()

    def sumValuesInAddresses(self) -> int:
        maskedValuesSum = 0
        for address, value in self.allAddressesWithValuesAfterMasking.items():
            maskedValuesSum += value

        return maskedValuesSum

    def getAllMaskedItems(self) -> Dict[int, int]:
        allAddressesAndValuesAfterMasking: Dict[int, int] = dict()
        for mask, addressesAndValues in self.allMaskToAddressesAndValues.items():
            maskingHandler = MaskingHandler(mask, self.itemToMask)
            for addressAndValue in addressesAndValues:
                maskedAddressesAndValues = maskingHandler.getMaskedAddressAndValue(addressAndValue)
                for maskedAddressAndValue in maskedAddressesAndValues:
                    allAddressesAndValuesAfterMasking[maskedAddressAndValue.memoryAddress] = maskedAddressAndValue.value
        return allAddressesAndValuesAfterMasking


def getAllMasksToAddressesAndValues(inputFile: str):
    allMaskingData: Dict[str, AllRawAddressesAndValues] = {}
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
                                                                             MaskingType.VALUE)
    print(maskingOperatorWithoutMaskingAddress.sumValuesInAddresses())  # 7997531787333

    maskingOperatorWithMaskingAddresses = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                            MaskingType.ADDRESS)
    print(maskingOperatorWithMaskingAddresses.sumValuesInAddresses())  # 3564822193820


class MaskingOperationsTester(unittest.TestCase):
    def test_sumValuesInAddresses_addressesNotMasked_correctSumReturned(self):
        allMasksToAddressesAndValues: Dict[str, AllRawAddressesAndValues] = getAllMasksToAddressesAndValues(TEST_INPUT)
        maskingOperatorWithoutMaskingAddress = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                                 MaskingType.VALUE)
        self.assertEqual(165, maskingOperatorWithoutMaskingAddress.sumValuesInAddresses())

    def test_sumValuesInAddresses_valuesNotMasked_correctSumReturned(self):
        allMasksToAddressesAndValues: Dict[str, AllRawAddressesAndValues] = getAllMasksToAddressesAndValues(
            TEST_INPUT_PART_TWO)
        maskingOperatorWithMaskingAddress = MaskingHandlersCollectionOperator(allMasksToAddressesAndValues,
                                                                              MaskingType.ADDRESS)
        self.assertEqual(208, maskingOperatorWithMaskingAddress.sumValuesInAddresses())


if __name__ == '__main__':
    # main()
    unittest.main()

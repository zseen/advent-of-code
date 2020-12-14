import unittest
from typing import List, Dict

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"







class MaskingHandler:
    def __init__(self, mask: str):
        self.mask = mask
        self._addressesAndValuesWithMaskedValues: List[MemoryAddressToValue] = []

    def addAddressAndValueWithMaskedValue(self, memoryAddress: str, normalValue: int):
        maskedValue = self._createMaskedValue(normalValue)
        memoryAddressToValueWithMaskedValue = MemoryAddressToValueWithMaskedValue(memoryAddress, normalValue, maskedValue)
        self._addressesAndValuesWithMaskedValues.append(memoryAddressToValueWithMaskedValue)

    def getAddressesAndValuesWithMaskedValues(self):
        return self._addressesAndValuesWithMaskedValues

    def _createMaskedValue(self, value):
        binaryValue: str = ("{0:b}".format(value))
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



class AllMaskingHandlers:
    def __init__(self, allMasksToAddressesAndValues: List[MaskingHandler]):
        self.allMasksToAddressesAndValues = allMasksToAddressesAndValues

    def getAllAddressesToValuesWithMaskedValues(self):
        allAddressesToValuesWithMaskedValues = []
        for maskingHandler in self.allMasksToAddressesAndValues:
            allAddressesToValuesWithMaskedValues.append(maskingHandler.getAddressesAndValuesWithMaskedValues())
        return allAddressesToValuesWithMaskedValues

    def sumMaskedValuesInAllAddresses(self):
        allAddressesToValuesWithMaskedValues = self.getAllAddressesToValuesWithMaskedValues()
        addressesWithMaskedValueAlreadySummed = set()
        maskedValuesSum = 0

        for addressesAndValuesWithMaskedValues in allAddressesToValuesWithMaskedValues[::-1]:
            for addressToValueAndMaskedValue in addressesAndValuesWithMaskedValues:
                currentMemoryAddress = addressToValueAndMaskedValue.getMemoryAddress()
                if currentMemoryAddress not in addressesWithMaskedValueAlreadySummed:
                    maskedValuesSum += addressToValueAndMaskedValue.getMaskedValue()
                addressesWithMaskedValueAlreadySummed.add(currentMemoryAddress)
        return maskedValuesSum





class MemoryAddressToValueWithMaskedValue:
    def __init__(self, memoryAddress: str, value: int, maskedValue: int):
        self.memoryAddress = memoryAddress
        self.value = value
        self.maskedValue = maskedValue

    def getMemoryAddress(self):
        return self.memoryAddress

    def getMaskedValue(self):
        return self.maskedValue








def getAllMasksToAddresses(inputFile: str):
    allMasksToAddresses = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" = ")
            if line[0] == "mask":
                maskingValue = line[1].strip("\n")
                maskingHandler = MaskingHandler(maskingValue)
                allMasksToAddresses.append(maskingHandler)
            else:
                maskingHandler.addAddressAndValueWithMaskedValue(line[0], int(line[1].strip("\n")))

    return allMasksToAddresses


x = getAllMasksToAddresses(INPUT_FILE)
#print(x)

allMaskingHandlers = AllMaskingHandlers(x)
allSums = allMaskingHandlers.sumMaskedValuesInAllAddresses()
# v = []
# for maskingHandler in x:
#     #allSums += maskingHandler.getMaskedValuesSumInAddress()
#     print(maskingHandler.mask)
#     for c in maskingHandler.addressesAndValues:
#         print(c.memoryAddress, c.value)
#     print("--------------------------------")

print(allSums) # 9175676038603 is too high

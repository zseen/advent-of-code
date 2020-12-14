import unittest
from typing import List, Dict

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"







class MaskingHandler:
    def __init__(self, mask: str):
        self.mask = mask
        self.addressesAndValues: List[MemoryAddressToValue] = []

    def addAddressAndValue(self, memoryAddress: str, normalValue: int):
        self.addressesAndValues.append(MemoryAddressToValue(memoryAddress, normalValue))

    def getAddressesAndValuesWithMaskedValues(self):
        self.putMaskOnValues()
        return self.addressesAndValues

    def putMaskOnValues(self):
        for addressAndValue in self.addressesAndValues:
            addressAndValue.putMaskOnValue(self.mask)

    # def getMaskedValuesSumInAddress(self):
    #     self.putMaskOnValues()
    #     addressAlreadyAssignedTo = set()
    #     maskedValuesSum = 0
    #     for addressToValue in self.addressesAndValues[::-1]:
    #         if not addressToValue.memoryAddress in addressAlreadyAssignedTo:
    #             maskedValuesSum += addressToValue.maskedValue
    #         addressAlreadyAssignedTo.add(addressToValue.memoryAddress)
    #
    #     return maskedValuesSum

class AllMaskingHandlers:
    def __init__(self, allMasksToAddressesAndValues: List[MaskingHandler]):
        self.allMasksToAddressesAndValues = allMasksToAddressesAndValues
        self.allAddressesToValuesWithMaskedValues = []

    def getAllAddressesToValuesWithMaskedValues(self):
        for maskingHandler in self.allMasksToAddressesAndValues:
            self.allAddressesToValuesWithMaskedValues.append(maskingHandler.getAddressesAndValuesWithMaskedValues())

    def sumMaskedValuesInAllAddresses(self):
        self.getAllAddressesToValuesWithMaskedValues()
        addressesAlreadyAssignedTo = set()
        maskedValuesSum = 0

        for addressAndValuesWithMaskedValues in self.allAddressesToValuesWithMaskedValues[::-1]:
            print(addressAndValuesWithMaskedValues)
            for memoryAddressToValueAndMaskedValue in addressAndValuesWithMaskedValues:
                if memoryAddressToValueAndMaskedValue.memoryAddress not in addressesAlreadyAssignedTo:
                    maskedValuesSum += memoryAddressToValueAndMaskedValue.maskedValue
                addressesAlreadyAssignedTo.add(memoryAddressToValueAndMaskedValue.memoryAddress)
        return maskedValuesSum





class MemoryAddressToValue:
    def __init__(self, memoryAddress: str, value: int):
        self.memoryAddress = memoryAddress
        self.value = value
        self.maskedValue: int  = -1

    def putMaskOnValue(self, mask):
        binaryValue: str = ("{0:b}".format(self.value))
        paddedBinaryValue = binaryValue.rjust(36, "0")

        maskedBinaryString = ""
        for i in range(0, len(mask)):
            if mask[i] == "1":
                maskedBinaryString += "1"
            elif mask[i] == "0":
                maskedBinaryString += "0"
            else:
                maskedBinaryString += paddedBinaryValue[i]

        maskedBinaryStringInDecimal = int(maskedBinaryString, 2)
        self.maskedValue = maskedBinaryStringInDecimal









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
                maskingHandler.addAddressAndValue(line[0], int(line[1].strip("\n")))

    return allMasksToAddresses


x = getAllMasksToAddresses(INPUT_FILE)
print(x)

allMaskingHandlers = AllMaskingHandlers(x)
allSums = allMaskingHandlers.sumMaskedValuesInAllAddresses()
v = []
for maskingHandler in x:
    #allSums += maskingHandler.getMaskedValuesSumInAddress()
    print(maskingHandler.mask)
    for c in maskingHandler.addressesAndValues:
        print(c.memoryAddress, c.value)
    print("--------------------------------")

print(allSums) # 9175676038603 is too high

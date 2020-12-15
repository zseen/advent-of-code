import unittest
from typing import List, Dict

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"
TEST_INPUT_PART_TWO = "test_input_two.txt"






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
# -------------------------------------------------------------------------------------------------------------------------


def getInput(inputFile: str):
    allMasksToAddresses = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" = ")
            if line[0] == "mask":
                maskingValue = line[1].strip("\n")
                memoryAddressMasker = MemoryAddressMasker(maskingValue)
                allMasksToAddresses.append(memoryAddressMasker)
            else:
                numPartOfMemoryAddress = []
                for char in line[0]:
                    if char.isdigit():
                        numPartOfMemoryAddress.append(char)
                memoryAddress = int("".join(numPartOfMemoryAddress))
                val = int(line[1].strip("\n"))
                memoryAddressMasker.addMemoryAddressWithMaskedAddressAndValue(memoryAddress)

    return allMasksToAddresses


class MemoryAddressMasker:
    def __init__(self, mask: str):
        self.mask = mask
        self.memoryAddressesAndValuesWithMaskedMemoryAddresses = []

    def addMemoryAddressWithMaskedAddressAndValue(self, address: int):
        maskedAddressesFromAddress = self.getPossibleMaskedAddresses(address)
        for maskedAddress in maskedAddressesFromAddress:
            self.memoryAddressesAndValuesWithMaskedMemoryAddresses.append(MemoryAddressAndMaskedAddress(maskedAddress, maskedAddress))

    def getPossibleMaskedAddresses(self, address):
        binaryValue: str = ("{0:b}".format(address))
        paddedBinaryValue = binaryValue.rjust(36, "0")

        maskedBinaryAddress = ""
        xPositions = []
        for i in range(0, len(self.mask)):
            if self.mask[i] == "X":
                maskedBinaryAddress += "X"
                xPositions.append(35 - i)
            elif self.mask[i] == "1":
                maskedBinaryAddress += "1"
            else:
                maskedBinaryAddress += paddedBinaryValue[i]

        positionToValueOfTwoPowered: Dict[int, int] = dict()
        for i in range(0, 36):
            positionToValueOfTwoPowered[i] = 2 ** i

        smallestToGet = ""
        for i in range(0, len(maskedBinaryAddress)):
            if maskedBinaryAddress[i] == "X":
                smallestToGet += "0"
            else:
                smallestToGet += maskedBinaryAddress[i]


        smallestToGetNum = int(smallestToGet, 2)

        numsToCombineAndAddToSmallestMaskedAddress = []

        for xpos in xPositions[::-1]:
            numsToCombineAndAddToSmallestMaskedAddress.append(positionToValueOfTwoPowered[xpos])

        allPossibleMaskedAddresses = []
        def func(soFar, gen, res):
            #print(soFar)
            if len(gen) == 0:
                res.append(soFar)
                allPossibleMaskedAddresses.append(soFar)
                return

            func(soFar + gen[0], gen[1:], res)
            func(soFar, gen[1:], res)


        func(smallestToGetNum, numsToCombineAndAddToSmallestMaskedAddress, [])

        return allPossibleMaskedAddresses








# x = MemoryAddressMasker("000000000000000000000000000000X1001X")
# m = x.getPossibleMaskedAddresses(42)
# print(m)
#
# z = MemoryAddressMasker("00000000000000000000000000000000X0XX")
# c = z.getPossibleMaskedAddresses(26)
# print(c)


class AllMemoryAddressesToModifiedAddresses:
    def __init__(self, allMemoryAddressMaskers: List[MemoryAddressMasker]):
        self.memoryAddressesToModifiedAddresses = allMemoryAddressMaskers

    def getAllMemoryAddressesToMaskedAddresses(self):
        return self.memoryAddressesToModifiedAddresses


class MemoryAddressAndMaskedAddress:
    def __init__(self, memoryAddress: int, maskedAddress: str):
        self.memoryAddress = memoryAddress
        self.maskedAddress: str = maskedAddress





testPartTwoInput = getInput(TEST_INPUT_PART_TWO)
#for x in testPartTwoInput:
    #print(x)
    #print(x.mask)
    #print(x.memoryAddressesAndValuesWithMaskedMemoryAddresses)
    #for c in x.memoryAddressesAndValuesWithMaskedMemoryAddresses:
        #print(c.memoryAddress)

allMemoryAddressesToModifiedAddresses = AllMemoryAddressesToModifiedAddresses(testPartTwoInput)
x = allMemoryAddressesToModifiedAddresses.getAllMemoryAddressesToMaskedAddresses()
for data in x:
    print(data.memoryAddressesAndValuesWithMaskedMemoryAddresses)
    for c in data.memoryAddressesAndValuesWithMaskedMemoryAddresses:
        print(c.memoryAddress, c.maskedAddress)


#### TODO:
# only sum unique addressed masked addresses in AllMemoryAddressesToModifiedAddresses






#x = getAllMasksToAddresses(INPUT_FILE)
#print(x)

# allMaskingHandlers = AllMaskingHandlers(x)
# allSums = allMaskingHandlers.sumMaskedValuesInAllAddresses()
# v = []
# for maskingHandler in x:
#     #allSums += maskingHandler.getMaskedValuesSumInAddress()
#     print(maskingHandler.mask)
#     for c in maskingHandler.addressesAndValues:
#         print(c.memoryAddress, c.value)
#     print("--------------------------------")

#print(allSums) # 9175676038603 is too high

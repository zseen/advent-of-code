import unittest
from typing import List

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

PREAMBLE_LENGTH_TEST = 5
PREAMBLE_LENGTH = 25

def getInput(inputFile):
    numbers = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            numbers.append(int(line))
    return numbers


def findExceptionNum(nums, preambleLength):
    preamble = nums[0: preambleLength]
    for i in range(0, len(nums)):
        if not areAnyTwoNumsAddingUpToNum(set(preamble), nums[i+preambleLength]):
            return nums[i+preambleLength]
        preamble = nums[i+1: 1+i + preambleLength]

    raise ValueError("No exception number found")



#def getPreambleNums(nums, preambleLength):


def areAnyTwoNumsAddingUpToNum(numsContainer, num):
    visitedNums = set()
    for numCandidate in numsContainer:
        if num - numCandidate in visitedNums:
            return True
        visitedNums.add(numCandidate)
    return False



nums = getInput(TEST_INPUT_FILE)
exceptionNum = findExceptionNum(nums, PREAMBLE_LENGTH_TEST)
print(exceptionNum)

nums = getInput(INPUT_FILE)
exceptionNum = findExceptionNum(nums, PREAMBLE_LENGTH)
print(exceptionNum)
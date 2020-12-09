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


def getContinuousNumsAddingUpToTarget(nums, target):
    startIndex = 0
    chunkLength = 0
    currentSum = 0
    numsToTry = []

    while chunkLength <= len(nums):
        numsToTry = []
        for i in range(startIndex, chunkLength):
            numsToTry.append(nums[i])
            currentSum = sum(numsToTry)
            if currentSum == target:
                return numsToTry
            if currentSum > target:
                startIndex += 1
        chunkLength += 1


    return numsToTry


def getSumSmallestAndLargestNumInArray(array: List[int]):
    return min(array) + max(array)





def areAnyTwoNumsAddingUpToNum(numsContainer, num):
    visitedNums = set()
    for numCandidate in numsContainer:
        if num - numCandidate in visitedNums:
            return True
        visitedNums.add(numCandidate)
    return False



#nums = getInput(TEST_INPUT_FILE)
#exceptionNum = findExceptionNum(nums, PREAMBLE_LENGTH_TEST)
#print(exceptionNum)

#numsAddingUpToTarget = getContinuousNumsAddingUpToTarget(nums, exceptionNum)
#print(numsAddingUpToTarget)
#print("test: ", getSumSmallestAndLargestNumInArray(numsAddingUpToTarget))

nums = getInput(INPUT_FILE)
exceptionNum = findExceptionNum(nums, PREAMBLE_LENGTH)
#print(exceptionNum) # 2089807806
numsAddingUpToTarget = getContinuousNumsAddingUpToTarget(nums, exceptionNum)
print(numsAddingUpToTarget)

#print(len(numsAddingUpToTarget))
#firstNumInChunk = numsAddingUpToTarget[0]
#print(firstNumInChunk)
#print("indexOfFirstNumInChunk: ", nums.index(firstNumInChunk))

testing = []
for i in range(554, (554+17)):
    testing.append(nums[i])

#print(testing == numsAddingUpToTarget)
#print(sum(testing)==sum(numsAddingUpToTarget)==exceptionNum)
print("min: ", min(numsAddingUpToTarget))
print("max: ", max(numsAddingUpToTarget))
print("res: ", min(numsAddingUpToTarget) + max(numsAddingUpToTarget))

print(getSumSmallestAndLargestNumInArray(numsAddingUpToTarget))

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


# def getContinuousNumsAddingUpToTarget(nums, target):
#     startIndex = 0
#     chunkLength = 0
#     numsToSum = []
#
#     while chunkLength <= len(nums):
#         numsToSum = []
#         for i in range(startIndex, chunkLength):
#             numsToSum.append(nums[i])
#             currentSum = sum(numsToSum)
#             if currentSum == target:
#                 return numsToSum
#             if currentSum > target:
#                 startIndex += 1
#         chunkLength += 1
#
#
#     return numsToSum

def getChunkAddingUpToTarget(nums, target):
    upperIndex = 0
    startIndex = 0
    numsToSum = []
    while upperIndex < len(nums):
        numsToSum = nums[startIndex:upperIndex]
        currentSum = sum(numsToSum)
        if currentSum == target:
            return numsToSum
        if currentSum > target:
            startIndex += 1
            upperIndex = startIndex
        upperIndex += 1

    return numsToSum



def getSmallestAndLargestNumInArraySum(array: List[int]):
    return min(array) + max(array)





def areAnyTwoNumsAddingUpToNum(numsContainer, num):
    visitedNums = set()
    for numCandidate in numsContainer:
        if num - numCandidate in visitedNums:
            return True
        visitedNums.add(numCandidate)
    return False



nums = getInput(TEST_INPUT_FILE)
exceptionNum = findExceptionNum(nums, PREAMBLE_LENGTH_TEST)
#print(exceptionNum)

numsAddingUpToTarget = getChunkAddingUpToTarget(nums, exceptionNum)
print(numsAddingUpToTarget)
print("test: ", getSmallestAndLargestNumInArraySum(numsAddingUpToTarget))

nums = getInput(INPUT_FILE)
exceptionNum = findExceptionNum(nums, PREAMBLE_LENGTH)
#print(exceptionNum) # 2089807806
numsAddingUpToTarget = getChunkAddingUpToTarget(nums, exceptionNum)
#print(numsAddingUpToTarget)

#print(len(numsAddingUpToTarget))
#firstNumInChunk = numsAddingUpToTarget[0]
#print(firstNumInChunk)
#print("indexOfFirstNumInChunk: ", nums.index(firstNumInChunk))



#print(testing == numsAddingUpToTarget)
#print(sum(testing)==sum(numsAddingUpToTarget)==exceptionNum)


print("solution: ", getSmallestAndLargestNumInArraySum(numsAddingUpToTarget))
print(getSmallestAndLargestNumInArraySum(numsAddingUpToTarget) == 245848639)

import unittest
from typing import List

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

PREAMBLE_LENGTH = 25
PREAMBLE_LENGTH_TEST = 5


def getInput(inputFile):
    numbers = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            numbers.append(int(line))
    return numbers


def getNumNotSumOfTwoPreviousNumsInContainer(nums: List[int], preambleLength: int):
    for i in range(0, len(nums) - preambleLength):
        preamble: List[int] = nums[i: i + preambleLength]
        exceptionNumCandidate: int = nums[i + preambleLength]
        if not areAnyTwoNumsInContainerAddingUpToTarget(preamble, exceptionNumCandidate):
            return exceptionNumCandidate

    raise ValueError("No exception number found")


def getChunkAddingUpToTarget(nums: List[int], target: int):
    upperIndex = 0
    startIndex = 0
    while upperIndex < len(nums):
        numsToSum = nums[startIndex: upperIndex]
        currentSum = sum(numsToSum)
        if currentSum == target:
            return numsToSum
        if currentSum > target:
            startIndex += 1
            upperIndex -= 1
        upperIndex += 1

    raise ValueError("No chunk in array to sum up to target.")


def getSumSmallestAndLargestNumsInArray(array: List[int]):
    if not array:
        raise ValueError("Empty array received.")
    return min(array) + max(array)


def areAnyTwoNumsInContainerAddingUpToTarget(numsContainer: List[int], target: int):
    uniqueNumsInContainer = set(numsContainer)
    visitedNums = set()
    for num in uniqueNumsInContainer:
        if target - num in visitedNums:
            return True
        visitedNums.add(num)
    return False


def main():
    numbers = getInput(INPUT_FILE)
    exceptionNum = getNumNotSumOfTwoPreviousNumsInContainer(numbers, PREAMBLE_LENGTH)
    print(exceptionNum)  # 2089807806

    chunkWithContinuousItemsSumUpToTarget = getChunkAddingUpToTarget(numbers, exceptionNum)
    sumSmallestAndLargestNumsInChunkSummingUpToTarget = getSumSmallestAndLargestNumsInArray(
        chunkWithContinuousItemsSumUpToTarget)
    print(sumSmallestAndLargestNumsInChunkSummingUpToTarget)  # 245848639


class ExceptionNumberOperationsTester(unittest.TestCase):
    def test_getNumNotSumOfTwoPreviousNumsInContainer_suchNumPresentInInput_correctNumReturned(self):
        numbers = getInput(TEST_INPUT_FILE)
        exceptionNum = getNumNotSumOfTwoPreviousNumsInContainer(numbers, PREAMBLE_LENGTH_TEST)
        self.assertEqual(127, exceptionNum)

    def test_getSumSmallestAndLargestNumsInArray_correctSumReturned(self):
        numbers = getInput(TEST_INPUT_FILE)
        exceptionNum = getNumNotSumOfTwoPreviousNumsInContainer(numbers, PREAMBLE_LENGTH_TEST)
        self.assertEqual(127, exceptionNum)

        chunkWithContinuousItemsSumUpToTarget = getChunkAddingUpToTarget(numbers, exceptionNum)
        self.assertEqual([15, 25, 47, 40], chunkWithContinuousItemsSumUpToTarget)

        sumSmallestAndLargestNumsInChunkSummingUpToTarget = getSumSmallestAndLargestNumsInArray(
            chunkWithContinuousItemsSumUpToTarget)
        self.assertEqual(62, sumSmallestAndLargestNumsInChunkSummingUpToTarget)


if __name__ == '__main__':
    # main()
    unittest.main()

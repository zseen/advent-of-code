import unittest
from typing import List, Text
from collections import deque

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

PREAMBLE_LENGTH = 25
PREAMBLE_LENGTH_TEST = 5


def getInput(inputFile: Text):
    numbers = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            numbers.append(int(line))
    return numbers


def getInvalidNumberInProcess(nums: List[int], preambleLength: int):
    preamble: deque = deque(nums[0: preambleLength])
    for i in range(preambleLength, len(nums)):
        invalidNumCandidate: int = nums[i]
        if not areAnyTwoNumsInContainerAddingUpToTarget(preamble, invalidNumCandidate):
            return invalidNumCandidate
        preamble.append(nums[i])
        preamble.popleft()

    raise ValueError("No invalid number found")


def areAnyTwoNumsInContainerAddingUpToTarget(numsContainer: deque, target: int):
    visitedNums = set()
    for num in numsContainer:
        if target - num in visitedNums and target != num:
            return True
        visitedNums.add(num)
    return False


def getEncryptionWeakness(array: List[int], preambleLength: int):
    invalidNumber = getInvalidNumberInProcess(array, preambleLength)
    chunk = getChunkAddingUpToTarget(array, invalidNumber)
    if not chunk:
        raise ValueError("Empty chunk returned.")
    return min(chunk) + max(chunk)


def getChunkAddingUpToTarget(nums: List[int], target: int):
    endIndex = 0
    startIndex = 0
    currentSum = 0
    while endIndex < len(nums):
        if currentSum == target:
            return nums[startIndex: endIndex]
        if currentSum > target:
            currentSum -= nums[startIndex]
            startIndex += 1
        else:
            currentSum += nums[endIndex]
            endIndex += 1

    raise ValueError("No chunk in array to sum up to target.")


def main():
    numbers = getInput(INPUT_FILE)
    invalidNum = getInvalidNumberInProcess(numbers, PREAMBLE_LENGTH)
    print(invalidNum)  # 2089807806

    encryptionWeakness = getEncryptionWeakness(numbers, invalidNum)
    print(encryptionWeakness)  # 245848639


class ExceptionNumberOperationsTester(unittest.TestCase):
    def test_getInvalidNumberInProcess_suchNumPresentInInput_correctNumReturned(self):
        numbers = getInput(TEST_INPUT_FILE)
        invalidNum = getInvalidNumberInProcess(numbers, PREAMBLE_LENGTH_TEST)
        self.assertEqual(127, invalidNum)

    def test_getEncryptionWeakness_correctResultReturned(self):
        numbers = getInput(TEST_INPUT_FILE)
        encryptionWeakness = getEncryptionWeakness(numbers, PREAMBLE_LENGTH_TEST)
        self.assertEqual(62, encryptionWeakness)


if __name__ == '__main__':
    # main()
    unittest.main()

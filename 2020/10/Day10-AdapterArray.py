import unittest
from typing import List, Text

INPUT_FILE = "input.txt"
TEST_INPUT_SHORT = "test_input_short.txt"
TEST_INPUT_LONG = "test_input_long.txt"


def getJolts(inputFile: Text):
    jolts: List[int] = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            jolts.append(int(line))
    return jolts


def getJoltageDifferenceCountersProduct(jolts: List[int]):
    if not jolts:
        raise ValueError("No adapters found.")

    jolts.append(max(jolts) + 3)
    numAdaptersWithOneJoltageDifference = 0
    numAdaptersWithThreeJoltageDifference = 0
    currentJoltage = 0
    joltsSet = set(jolts)

    while currentJoltage != max(jolts):
        if currentJoltage + 1 in joltsSet:
            numAdaptersWithOneJoltageDifference += 1
            currentJoltage += 1
        elif currentJoltage + 2 in joltsSet:
            currentJoltage += 2
        elif currentJoltage + 3 in joltsSet:
            numAdaptersWithThreeJoltageDifference += 1
            currentJoltage += 3
        else:
            raise ValueError("Connecting adapters is not possible.")

    return numAdaptersWithOneJoltageDifference * numAdaptersWithThreeJoltageDifference


def countDistictWaysToArrangeAdapters(jolts: List[int]):
    jolts.sort()
    maxJoltage: int = max(jolts)
    memo: List[int] = [0] * (maxJoltage + 1)
    memo[0] = 1

    for jolt in jolts:
        memo[jolt] = memo[jolt - 1] + memo[jolt - 2] + memo[jolt - 3]

    return memo[maxJoltage]


def main():
    jolts: List[int] = getJolts(INPUT_FILE)

    print(getJoltageDifferenceCountersProduct(jolts))  # 2414
    print(countDistictWaysToArrangeAdapters(jolts))  # 21156911906816


class JoltsTester(unittest.TestCase):
    def test_getJoltageDifferenceCountersProduct_shortInput_correctProductReturned(self):
        jolts: List[int] = getJolts(TEST_INPUT_SHORT)
        self.assertEqual(35, getJoltageDifferenceCountersProduct(jolts))

    def test_getJoltageDifferenceCountersProduct_longInput_correctProductReturned(self):
        jolts: List[int] = getJolts(TEST_INPUT_LONG)
        self.assertEqual(220, getJoltageDifferenceCountersProduct(jolts))

    def test_countDistinctWaysToArrangeAdapters_shortInput_correctCountReturned(self):
        jolts: List[int] = getJolts(TEST_INPUT_SHORT)
        self.assertEqual(8, countDistictWaysToArrangeAdapters(jolts))

    def test_countDistinctWaysToArrangeAdapters_longInput_correctCountReturned(self):
        jolts: List[int] = getJolts(TEST_INPUT_LONG)
        self.assertEqual(19208, countDistictWaysToArrangeAdapters(jolts))


if __name__ == '__main__':
    # main()
    unittest.main()

import unittest

INPUT_FILE = "input.txt"
TEST_INPUT_SHORT = "test_input_short.txt"
TEST_INPUT_LONG = "test_input_long.txt"


def getJolts(inputFile):
    jolts = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            jolts.append(int(line))
    return jolts


def getJoltageDifferenceCountersProduct(jolts):
    if not jolts:
        raise ValueError("No adapters found.")

    numAdaptersWithOneJoltageDifference = 0
    # Initialise with one, as the own joltage adapter is 3 larger than the largest adapter from 'jolts'
    numAdaptersWithThreeJoltageDifference = 1
    currentJoltage = 0
    joltsSet = set(jolts)

    while currentJoltage != max(jolts):
        if currentJoltage + 1 in joltsSet:
            numAdaptersWithOneJoltageDifference += 1
            # Could move this after the 'else branch', and subtract 1 from the other additions, but it is easier to understand the logic as it is now
            currentJoltage += 1
        elif currentJoltage + 2 in joltsSet:
            currentJoltage += 2
        elif currentJoltage + 3 in joltsSet:
            numAdaptersWithThreeJoltageDifference += 1
            currentJoltage += 3
        else:
            raise ValueError("Connecting adapters is not possible.")

    return numAdaptersWithOneJoltageDifference * numAdaptersWithThreeJoltageDifference


def countDistictWaysToArrangeAdapters(jolts):
    jolts.sort()
    maxJoltage = max(jolts)
    memo = [0] * (maxJoltage + 1)
    memo[0] = 1

    for jolt in jolts:
        memo[jolt] = memo[jolt - 1] + memo[jolt - 2] + memo[jolt - 3]

    return memo[maxJoltage]


def main():
    jolts = getJolts(INPUT_FILE)

    print(getJoltageDifferenceCountersProduct(jolts))  # 2414
    print(countDistictWaysToArrangeAdapters(jolts))  # 21156911906816


class JoltsTester(unittest.TestCase):
    def test_getJoltageDifferenceCountersProduct_shortInput_correctProductReturned(self):
        jolts = getJolts(TEST_INPUT_SHORT)
        self.assertEqual(35, getJoltageDifferenceCountersProduct(jolts))

    def test_getJoltageDifferenceCountersProduct_longInput_correctProductReturned(self):
        jolts = getJolts(TEST_INPUT_LONG)
        self.assertEqual(220, getJoltageDifferenceCountersProduct(jolts))

    def test_countDistinctWaysToArrangeAdapters_shortInput_correctCountReturned(self):
        jolts = getJolts(TEST_INPUT_SHORT)
        self.assertEqual(8, countDistictWaysToArrangeAdapters(jolts))

    def test_countDistinctWaysToArrangeAdapters_longInput_correctCountReturned(self):
        jolts = getJolts(TEST_INPUT_LONG)
        self.assertEqual(19208, countDistictWaysToArrangeAdapters(jolts))


if __name__ == '__main__':
    # main()
    unittest.main()

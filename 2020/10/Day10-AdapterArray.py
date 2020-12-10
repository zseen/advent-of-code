import unittest

INPUT_FILE = "input.txt"
TEST_INPUT_SHORT = "test_input_short.txt"
TEST_INPUT_LONG = "test_input_long.txt"
JOLTAGE_DIFFERENCE_MAX = 3


class Jolt:
    def __init__(self, joltage: int):
        self.joltage: int = joltage


def getResult(jolts):
    oneDifferenceCounter = 0
    threeDifferenceCounter = 1
    currentJoltage = 0
    usedJolts = set()

    while currentJoltage != max(list(jolts.keys())):
        if currentJoltage + 1 in jolts:
            oneDifferenceCounter += 1
            currentJoltage += 1
            usedJolts.add(jolts[currentJoltage])
        elif currentJoltage + 2 in jolts:
            currentJoltage += 2
            usedJolts.add(jolts[currentJoltage])
        elif currentJoltage + 3 in jolts:
            threeDifferenceCounter += 1
            currentJoltage += 3
            usedJolts.add(jolts[currentJoltage])


    return oneDifferenceCounter * threeDifferenceCounter






def getInput(inputFile):
    joltsValuesToJolts = dict()
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            jolt = Jolt(int(line))
            joltsValuesToJolts[jolt.joltage] = jolt
    return joltsValuesToJolts





jolts = getInput(TEST_INPUT_SHORT)
res = getResult(jolts)
print(res)
print("----------")
jolts2 = getInput(TEST_INPUT_LONG)
res2 = getResult(jolts2)
print(res2)
print("----------")
jolts3 = getInput(INPUT_FILE)
res3 = getResult(jolts3)
print(res3)
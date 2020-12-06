import unittest
import re
from typing import List

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

def getInput(inputFile):
    allGroupsAnswers = [[]]

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            if line == "\n":
                allGroupsAnswers.append([])
            else:
                line = line.strip("\n")
                lineSplit = re.split('', line)
                neededChars = [char for char in lineSplit if char.isalpha()]
                allGroupsAnswers[-1].extend(neededChars)

    return allGroupsAnswers


def countUniqueAnswersInGroup(groupAnswers: List):
    return len(set(groupAnswers))

def getUniqueAnswersCountInAllGroups(allGroups: List[List]):
    allUniqueAnswersCount = 0
    for groupAnswer in allGroups:
        allUniqueAnswersCount += countUniqueAnswersInGroup(groupAnswer)
    return allUniqueAnswersCount


v = getInput(INPUT_FILE)
print(getUniqueAnswersCountInAllGroups(v))
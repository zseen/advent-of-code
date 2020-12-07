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
                allGroupsAnswers[-1].append(line)
    return allGroupsAnswers


def countUniqueAnswersInGroup(groupAnswers: List[str]):
    allAnswersInGroup = list(''.join(groupAnswers))
    return len(set(allAnswersInGroup))


def countUniqueAnswersInAllGroups(allGroups: List[List]):
    return sum(countUniqueAnswersInGroup(group) for group in allGroups)


def countCommonAnswersInGroup(group: List[str]):
    commonAnswers = set(group[0])
    for i in range(1, len(group)):
        currentAnswers = commonAnswers
        nextAnswers = set(group[i])
        commonAnswers = currentAnswers.intersection(nextAnswers)
    return len(commonAnswers)


def countCommonGroupAnswersInAllGroups(allGroups: List[List]):
    return sum(countCommonAnswersInGroup(group) for group in allGroups)


def main():
    allGroupsAnswers = getInput(INPUT_FILE)
    print(countUniqueAnswersInAllGroups(allGroupsAnswers))  # 6416
    print(countCommonGroupAnswersInAllGroups(allGroupsAnswers))  # 3050


class AnswersTester(unittest.TestCase):
    def test_countUniqueAnswersInAllGroups_correntUniqueAnswersCountReturned(self):
        allGroupsAnswers = getInput(TEST_INPUT)
        self.assertEqual(11, countUniqueAnswersInAllGroups(allGroupsAnswers))

    def test_countCommonGroupAnswersInAllGroups_correctCommonAnswersCountReturned(self):
        allGroupsAnswers = getInput(TEST_INPUT)
        self.assertEqual(6, countCommonGroupAnswersInAllGroups(allGroupsAnswers))


if __name__ == '__main__':
    # main()
    unittest.main()

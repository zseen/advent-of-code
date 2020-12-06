import unittest
import re
from typing import List

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"


def getInputForFirstPart(inputFile):
    allGroupsAnswers = [[]]
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            if line == "\n":
                allGroupsAnswers.append([])
            else:
                line = line.strip("\n")
                allGroupsAnswers[-1].extend(line)
    return allGroupsAnswers


def getInputForSecondPart(inputFile):
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


def countUniqueAnswersInGroup(groupAnswers: List):
    return len(set(groupAnswers))


def getUniqueAnswersCountInAllGroups(allGroups: List[List]):
    return sum(countUniqueAnswersInGroup(group) for group in allGroups)


def countCommonAnswersInGroup(group: List):
    commonAnswer = set(group[0])
    for i in range(1, len(group)):
        currentAnswers = commonAnswer
        nextAnswers = set(group[i])
        commonAnswer = currentAnswers.intersection(nextAnswers)
    return len(commonAnswer)


def countCommonGroupAnswersInAllGroups(allGroups: List[List]):
    return sum(countCommonAnswersInGroup(group) for group in allGroups)


def main():
    allGroupsAnswersFirstPart = getInputForFirstPart(INPUT_FILE)
    print(getUniqueAnswersCountInAllGroups(allGroupsAnswersFirstPart))

    allGroupsAnswersSecondPart = getInputForSecondPart(INPUT_FILE)
    print(countCommonGroupAnswersInAllGroups(allGroupsAnswersSecondPart))


class AnswersTester(unittest.TestCase):
    def test_getUniqueAnswersCountInAllGroups_correntUniqueAnswersCountReturned(self):
        allGroupsAnswers = getInputForFirstPart(TEST_INPUT)
        self.assertEqual(11, getUniqueAnswersCountInAllGroups(allGroupsAnswers))

    def test_countCommonGroupAnswersInAllGroups_correctCommonAnswersCountReturned(self):
        allGroupsAnswers = getInputForSecondPart(TEST_INPUT)
        self.assertEqual(6, countCommonGroupAnswersInAllGroups(allGroupsAnswers))


if __name__ == '__main__':
    # main()
    unittest.main()

# I know it should not be here, just please have a look at it!
# def getAnswersEveryoneAgreedOnCount(allGroups: List[List]):
#     allAgreedAnswers = 0
#     for groupAnswer in allGroups:
#         shortestStringInGroupAnswer = min(groupAnswer, key=len)
#         commonCharsNum = 0
#         for char in shortestStringInGroupAnswer:
#             isCharCommonInAllStrings = True
#             for i in range(0, len(groupAnswer)):
#                 if char not in groupAnswer[i]:
#                     isCharCommonInAllStrings = False
#                     break
#             if isCharCommonInAllStrings:
#                 commonCharsNum += 1
#         allAgreedAnswers += commonCharsNum
#
#     return allAgreedAnswers

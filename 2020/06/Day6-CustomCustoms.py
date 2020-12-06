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

    #print(allGroupsAnswers)
    return allGroupsAnswers

def getInputSecondPart(inputFile):
    allGroupsAnswers = [[]]

    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            if line == "\n":
                allGroupsAnswers.append([])
            else:
                line = line.strip("\n")
                #lineSplit = re.split('', line)
                #neededChars = [char for char in lineSplit if char.isalpha()]
                #allGroupsAnswers[-1].extend(neededChars)
                #print(line)
                allGroupsAnswers[-1].append(line)
    #print(allGroupsAnswers)
    return allGroupsAnswers

def countUniqueAnswersInGroup(groupAnswers: List):
    return len(set(groupAnswers))

def getUniqueAnswersCountInAllGroups(allGroups: List[List]):
    allUniqueAnswersCount = 0
    for groupAnswer in allGroups:
        allUniqueAnswersCount += countUniqueAnswersInGroup(groupAnswer)
    return allUniqueAnswersCount


def getAnswersCountEveryoneAgreedOn(allGroups: List[List]):
    allAgreedAnswers = 0
    for groupAnswer in allGroups:
        if len(groupAnswer) == 1:
            allAgreedAnswers += len(groupAnswer[0])
        else:
            firstStringInGroup = groupAnswer[0]
            allStringInGroupNum = len(groupAnswer)
            commonCharsNum = 0
            for char in firstStringInGroup:
                currCharCount = 0
                for i in range(0, allStringInGroupNum):
                    if char in groupAnswer[i]:
                        currCharCount += 1
                if currCharCount == allStringInGroupNum:
                    commonCharsNum += 1
            allAgreedAnswers += commonCharsNum



    return allAgreedAnswers







v = getInput(TEST_INPUT)
#print(getUniqueAnswersCountInAllGroups(v)) # 6416

b = getInputSecondPart(TEST_INPUT)
c = getInputSecondPart(INPUT_FILE)
print(b)
#print(c)

print(getAnswersCountEveryoneAgreedOn(b))
print(getAnswersCountEveryoneAgreedOn(c)) # 3225 is too high 3128 too high

#print(getAnswersCountEveryoneAgreedOn([c[0]]))
print(getAnswersCountEveryoneAgreedOn([['e', 'e', 'e', 'e']])) #1
print(getAnswersCountEveryoneAgreedOn([ ['pfyh', 'hyf', 'dhfy']])) #3
print(getAnswersCountEveryoneAgreedOn([['dqbpwhoar', 'pqohgd']])) #5
print(getAnswersCountEveryoneAgreedOn([['sakhxnu', 'cdowx', 'xlj', 'lnxh', 'njxhf']])) #1

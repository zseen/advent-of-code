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


def getAnswersEveryoneAgreedOnCount(allGroups: List[List]):
    allAgreedAnswers = 0
    for groupAnswer in allGroups:
        shortestStringInGroupAnswer = min(groupAnswer, key=len)
        commonCharsNum = 0
        for char in shortestStringInGroupAnswer:
            isCharCommonInAllStrings = True
            for i in range(0, len(groupAnswer)):
                if char not in groupAnswer[i]:
                    isCharCommonInAllStrings = False
                    break
            if isCharCommonInAllStrings:
                commonCharsNum += 1
        allAgreedAnswers += commonCharsNum

    return allAgreedAnswers


def getAnswersEveryoneAgreedOnCount2(ga):
    intersection = set(ga[0])
    for i in range(1, len(ga)):
        currentStringAsSet = intersection
        nextStringAsSet = set(ga[i])
        intersection = currentStringAsSet.intersection(nextStringAsSet)
    return len(intersection)


def getAll(allGroups: List[List]):
    allAg =  0
    for groupAnswer in allGroups:
        allAg += getAnswersEveryoneAgreedOnCount2(groupAnswer)
    return allAg










v = getInput(TEST_INPUT)
#print(getUniqueAnswersCountInAllGroups(v)) # 6416

b = getInputSecondPart(TEST_INPUT)
c = getInputSecondPart(INPUT_FILE)
#print(b)
#print(c)

#print(getAnswersEveryoneAgreedOnCount(b))
#print(getAnswersEveryoneAgreedOnCount(c)) # 3225 is too high 3128 too high  3050!!!!

#print(getAnswersEveryoneAgreedOnCount2(c))
print(getAll(c))


#print(getAnswersCountEveryoneAgreedOn([c[0]]))
#print(getAnswersCountEveryoneAgreedOn([['e', 'e', 'e', 'e']])) #1
#print(getAnswersCountEveryoneAgreedOn([ ['pfyh', 'hyf', 'dhfy']])) #3
#print(getAnswersCountEveryoneAgreedOn([['dqbpwhoar', 'pqohgd']])) #5
#print(getAnswersCountEveryoneAgreedOn([['sakhxnu', 'cdowx', 'xlj', 'lnxh', 'njxhf']])) #1

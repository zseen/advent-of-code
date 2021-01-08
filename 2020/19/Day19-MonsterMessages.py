import unittest
from typing import List, Dict
from copy import  deepcopy

TEST_INPUT_FILE = "test_input.txt"
TEST_INPUT_FILE_TWO = "test_input_two.txt"

def getInput(fileName: str):
    rules = {}
    with open(fileName, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            lineSplit = line.split(": ")
            rules[int(lineSplit[0])] = lineSplit[1].strip('""').split(" ")
    return rules






def getSubstitutedRules(rules: Dict):
    rulesModified = dict()
    rulesCopy = deepcopy(rules)

    for i in range(0, len(rules)):
        if i not in rules:
            raise ValueError("Problem with rules.")

        values = rulesCopy[i]
        rulesModified[i] = []

        for value in values:
            if not value.isnumeric():
                rulesModified[i].append(" ".join(value))
            else:
                rulesModified[i].append(" ".join((rulesCopy[int(value)])))

        # for value in values:
        #     if not value.isnumeric():
        #         rulesModified[i].append(" ".join(value))
        #     else:
        #         rulesModified[i].append(" ".join((rulesCopy[int(value)])))
        #
        #
        #

            # for key, ruleValue in rulesCopy.items():
            #     if value in ruleValue:
            #         indexesToChange = getIndexesOfValueInValues(value, ruleValue)
            #         if value.isnumeric():
            #             for indexToChange in indexesToChange:
            #                 rulesCopy[key][indexToChange] =  " ".join((rulesCopy[int(value)]))
    #print(rulesModified)


    for key, ruleValues in rulesModified.items():
        for i in range(0, len(ruleValues)):
            for char in ruleValues[i]:
                if char.isnumeric():
                    indexesToChange = getIndexesOfValueInValues(char, ruleValues[i])
                    charsToReplaceWith = "".join(rulesModified[int(char)])
                    rulesModified[key][i]= replaceStringCharsInValue(rulesModified[key][i], indexesToChange, charsToReplaceWith)

    return rulesModified


def replaceStringCharsInValue(value, indexesToChange, charsToReplaceWith):
    value = list(value)
    for indexToChange in indexesToChange:
        value[indexToChange] = charsToReplaceWith
    return "".join(value)





def getIndexesOfValueInValues(value, ruleValue):
    indexes = []
    for i in range(0, len(ruleValue)):
        if ruleValue[i] == value:
            indexes.append(i)
    return indexes



def isMessagePossible(message, rulesModified):
    return message in evaluateRules(rulesModified)


def evaluateRules(rulesModified):
    possibilities = []
    rulesToEvaluate = rulesModified[0]

    currentPoss = ""
    for rule in rulesToEvaluate:
        if "|" not in rule:
            currentPoss += rule
        else:
            chunkBeforeStick = evaluateStickValue(rule)[0]
            chunkAfterStick = evaluateStickValue(rule)[1]
            possibleCombination1 = currentPoss + "".join(chunkBeforeStick)
            possibleCombination2 = currentPoss + "".join(chunkAfterStick)
            possibilities.append(possibleCombination1)
            possibilities.append(possibleCombination2)

    return possibilities

def evaluateStickValue(value):
    flattenedValue = []
    for subvalue in value:
        if subvalue != " ":
            flattenedValue.extend(subvalue)

    indexOfStick = flattenedValue.index("|")
    return [flattenedValue[0:indexOfStick], flattenedValue[indexOfStick+1: ]]

c = getInput(TEST_INPUT_FILE_TWO)
print(c)
modifiedRules = getSubstitutedRules(c)
print(modifiedRules)

poss = evaluateRules(modifiedRules)
print(poss)

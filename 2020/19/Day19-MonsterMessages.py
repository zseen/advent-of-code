import unittest
from typing import List, Dict
from copy import  deepcopy
import re

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
TEST_INPUT_FILE_TWO = "test_input_two.txt"

def getInput(fileName: str):
    rules: Dict[int, List[str]] = {}
    messages: List[str] = []
    with open(fileName, "r") as inputFile:
        lines = inputFile.read()
        linesSplitByEmptyLine = lines.split("\n\n")
        rulesRawSeparated = linesSplitByEmptyLine[0].split("\n")

        for line in rulesRawSeparated:
            line = line.strip("\n")
            lineSplit = line.split(": ")
            rules[int(lineSplit[0])] = lineSplit[1].strip('""').split(" ")

        messagesSeparated = linesSplitByEmptyLine[1].split("\n")
        for line in messagesSeparated:
            messages.append(line)


    return rules, messages


# find the num witch char a and b first, add them to resolved
# go through all others to see if any of them can be resolved (this case num 3 with values 4 and 5 will be resolvable)
# check what can be resolved with this added num


def resolve(rules):
    resolvedNumToValues = dict()

    for key, values in rules.items():
        if "a" in values:
            resolvedNumToValues[key] = "a"
        elif "b" in values:
            resolvedNumToValues[key] = "b"

    #print(resolvedNumToValues)



    while len(resolvedNumToValues) != len(rules) - 1:
        for key, values in rules.items():
            isAllValueInResolved = True
            if key not in resolvedNumToValues and key != 0:
                resolvedValue = ""
                if "|" in values:
                    resolvedValue += "("
                for value in values:
                    if value.isnumeric() and int(value) not in resolvedNumToValues:
                        isAllValueInResolved = False
                    else:
                        if value.isnumeric():
                            resolvedValue += resolvedNumToValues[int(value)]
                        elif value == "|":
                            resolvedValue += "|"
                if isAllValueInResolved:
                    if "|" in values:
                        resolvedValue += ")"
                    resolvedNumToValues[key] = resolvedValue

    #print(resolvedNumToValues)

    expressionForZero = ""
    for value in rules[0]:
        expressionForZero += "(" + resolvedNumToValues[int(value)] + ")"

    return expressionForZero


def getAllValidMessagesCount(messages: List[str], rules):
    return len([message for message in messages if isMessageValid(message, rules)])



def isMessageValid(wordCandidate: str, rules):
    patternForMessage = resolve(rules)
    matching = re.fullmatch(patternForMessage, wordCandidate)
    return matching is not None




rules, messages = getInput(INPUT_FILE)
validMessages = getAllValidMessagesCount(messages, rules)
print(validMessages)
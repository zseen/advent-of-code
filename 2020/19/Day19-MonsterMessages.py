import unittest
from typing import List, Dict
from copy import  deepcopy
import re

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
TEST_INPUT_FILE_TWO = "test_input_two.txt"

def getInput(fileName: str):
    rules: Dict[int, List[str]] = {}

    with open(fileName, "r") as inputFile:
        lines = inputFile.read()
        linesChunks = lines.split("\n\n")

        rawRules = linesChunks[0].split("\n")
        for rawRule in rawRules:
            rawRuleSplit = rawRule.split(": ")
            rules[int(rawRuleSplit[0])] = rawRuleSplit[1].strip('""').split(" ")

        messages= linesChunks[1].split("\n")

    return rules, messages



def resolve(rules):
    resolvedNumToValues = initializeResolvedNumToValues(rules)

    while len(resolvedNumToValues) != len(rules):
        for key, values in rules.items():
            if key not in resolvedNumToValues:
                resolvedValue = createResolvedValueFromValues(values, resolvedNumToValues)
                if resolvedValue:
                    resolvedNumToValues[key] = "(" + resolvedValue + ")"

    if 0 not in resolvedNumToValues:
        raise ValueError("0 not in resolvedNumToValues.")

    return resolvedNumToValues[0]

def initializeResolvedNumToValues(rules):
    resolvedNumToValues: Dict[int, str] = dict()
    for key, values in rules.items():
        if "a" in values:
            resolvedNumToValues[key] = "a"
        elif "b" in values:
            resolvedNumToValues[key] = "b"
    return resolvedNumToValues


def createResolvedValueFromValues(values, resolvedNumToValues):
    resolvedValue = ""
    for value in values:
        if value.isnumeric() and int(value) not in resolvedNumToValues:
            return ""
        resolvedValue += buildResolvedValue(value, resolvedNumToValues)
    return resolvedValue



def buildResolvedValue(value, resolvedNumToValues):
    if value.isnumeric():
        return resolvedNumToValues[int(value)]
    elif value == "|":
        return "|"


def getAllValidMessagesCount(messages: List[str], rules):
    return len([message for message in messages if isMessageValid(message, rules)])



def isMessageValid(wordCandidate: str, rules):
    patternForMessage = resolve(rules)
    return re.fullmatch(patternForMessage, wordCandidate)


rules, messages = getInput(INPUT_FILE)
validMessages = getAllValidMessagesCount(messages, rules)
print(validMessages)
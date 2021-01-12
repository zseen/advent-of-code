import unittest
from typing import List, Dict
import re

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
TEST_INPUT_FILE_TWO = "test_input_two.txt"

RulesType = Dict[int, List[str]]


class ValidMessagesFinder:
    def __init__(self, rules: RulesType, messages: List[str]):
        self._rules = rules
        self._messages = messages
        self._resolvedRuleNumToValues: Dict[int, str] = dict()

    def getAllValidMessagesCount(self) -> int:
        self._resolveRules()
        return len([message for message in self._messages if self._isMessageValid(message)])

    def _resolveRules(self) -> None:
        self._resolvedRuleNumToValues = self._initializeResolvedNumToValues()

        while len(self._resolvedRuleNumToValues) != len(self._rules):
            for key, values in self._rules.items():
                if key not in self._resolvedRuleNumToValues:
                    resolvedValue = self._createResolvedValueFromValues(values)
                    if resolvedValue:
                        self._resolvedRuleNumToValues[key] = "(" + resolvedValue + ")"

    def _initializeResolvedNumToValues(self) -> Dict[int, str]:
        resolvedNumToValues: Dict[int, str] = dict()
        for key, value in self._rules.items():
            if "a" in value:
                resolvedNumToValues[key] = "a"
            elif "b" in value:
                resolvedNumToValues[key] = "b"
        return resolvedNumToValues


    def _createResolvedValueFromValues(self, values: List[str]) -> str:
        resolvedValue: str = ""
        for value in values:
            if value.isnumeric() and int(value) not in self._resolvedRuleNumToValues:
                return ""
            resolvedValue += self._buildResolvedValue(value)
        return resolvedValue


    def _buildResolvedValue(self, value: str) -> str:
        if value.isnumeric():
            return self._resolvedRuleNumToValues[int(value)]
        elif value == "|":
            return value
        raise ValueError("Unexpected character + ", value)


    def _isMessageValid(self, wordCandidate: str) -> re.Match:
        if 0 not in self._resolvedRuleNumToValues :
            raise ValueError("0 not in resolvedNumToValues.")

        patternForMessage: str = self._resolvedRuleNumToValues[0]
        return re.fullmatch(patternForMessage, wordCandidate)

def getInput(fileName: str) -> (RulesType, List[str]):
    rules: RulesType= {}

    with open(fileName, "r") as inputFile:
        lines = inputFile.read()
        linesChunks = lines.split("\n\n")

        rawRules = linesChunks[0].split("\n")
        for rawRule in rawRules:
            rawRuleSplit = rawRule.split(": ")
            rules[int(rawRuleSplit[0])] = rawRuleSplit[1].strip('""').split(" ")

        messages: List[str] = linesChunks[1].split("\n")

    return rules, messages


rules, messages = getInput(INPUT_FILE)
validMessagesFinder = ValidMessagesFinder(rules, messages)

print(validMessagesFinder.getAllValidMessagesCount())
import unittest
from typing import List, Dict
import re

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

RulesType = Dict[int, List[str]]
RuleToDecipheredValueType = Dict[int, str]


class ValidMessagesCounter:
    def __init__(self, rules: RulesType, messages: List[str]):
        self._rules = rules
        self._messages = messages
        self._ruleNumToDecipheredValue: RuleToDecipheredValueType = dict()

    def getValidMessagesCount(self) -> int:
        return len([message for message in self._messages if self._isMessageValid(message)])

    def decipherRules(self) -> None:
        self._ruleNumToDecipheredValue: RuleToDecipheredValueType = self._initializeDecipheredRuleNumToValues()

        while len(self._ruleNumToDecipheredValue) != len(self._rules):
            for key, values in self._rules.items():
                if key not in self._ruleNumToDecipheredValue:
                    decipheredValue: str = self._createDecipheredValueFromValues(values)
                    if decipheredValue:
                        self._ruleNumToDecipheredValue[key] = "(" + decipheredValue + ")"

    def _initializeDecipheredRuleNumToValues(self) -> RuleToDecipheredValueType:
        decipheredNumToValues: RuleToDecipheredValueType = dict()
        for key, value in self._rules.items():
            if "a" in value:
                decipheredNumToValues[key] = "a"
            elif "b" in value:
                decipheredNumToValues[key] = "b"

        return decipheredNumToValues

    def _createDecipheredValueFromValues(self, values: List[str]) -> str:
        decipheredValue: str = ""
        for value in values:
            if value.isnumeric() and int(value) not in self._ruleNumToDecipheredValue:
                return ""
            decipheredValue += self._buildDecipheredValue(value)
        return decipheredValue

    def _buildDecipheredValue(self, value: str) -> str:
        if value.isnumeric():
            return self._ruleNumToDecipheredValue[int(value)]
        elif value == "|":
            return value
        raise ValueError("Unexpected character: ", value)

    def _isMessageValid(self, message: str) -> re.Match:
        if 0 not in self._ruleNumToDecipheredValue:
            raise ValueError("0 not in ruleNumToDecipheredValue.")

        return re.fullmatch(self._ruleNumToDecipheredValue[0], message)


class ValidMessagesCounterForLoopyRules(ValidMessagesCounter):
    def __init__(self, rules: RulesType, messages: List[str]):
        super().__init__(rules, messages)
        self._ruleNumToDecipheredValue: RuleToDecipheredValueType = dict()

    def updateSpecificRules(self) -> None:
        self.decipherRules()

        if not 8 in self._ruleNumToDecipheredValue or not 11 in self._ruleNumToDecipheredValue or not 0 in self._ruleNumToDecipheredValue:
            raise ValueError("8, 11, or 0 not in ruleNumToDecipheredValue.")

        self._ruleNumToDecipheredValue[8] = "(" + self._ruleNumToDecipheredValue[42] + "+" + ")"
        self._ruleNumToDecipheredValue[11] = "(" + self.getRegexBodyForEleven() + ")"
        self._ruleNumToDecipheredValue[0] = self._ruleNumToDecipheredValue[8] + self._ruleNumToDecipheredValue[11]

    def getRegexBodyForEleven(self) -> str:
        if not 42 in self._ruleNumToDecipheredValue or not 31 in self._ruleNumToDecipheredValue:
            raise ValueError("42 or 31 not in ruleNumToDecipheredValue.")

        regexBodyFor11: str = ""
        for i in range(1, 5):
            regexBodyFor11 += self._ruleNumToDecipheredValue[42] + "{" + str(i) + "}" + self._ruleNumToDecipheredValue[31] + "{" + str(i) + "}" + "|"

        # The last pipe is not needed in the regex
        return regexBodyFor11[:-1]


def getInput(fileName: str) -> (RulesType, List[str]):
    rules: RulesType = dict()

    with open(fileName, "r") as inputFile:
        lines = inputFile.read()
        linesChunks = lines.split("\n\n")

        rawRules: List = linesChunks[0].split("\n")
        for rawRule in rawRules:
            rawRuleSplit = rawRule.split(": ")
            rules[int(rawRuleSplit[0])] = rawRuleSplit[1].strip('""').split(" ")

        messages: List[str] = linesChunks[1].split("\n")

    return rules, messages


def main():
    rules, messages = getInput(INPUT_FILE)

    validMessagesCounter = ValidMessagesCounter(rules, messages)
    validMessagesCounter.decipherRules()
    print(validMessagesCounter.getValidMessagesCount())  # 187

    validMessagesCounterForLoopyRules = ValidMessagesCounterForLoopyRules(rules, messages)
    validMessagesCounterForLoopyRules.updateSpecificRules()
    print(validMessagesCounterForLoopyRules.getValidMessagesCount())  # 392


class ValidMessagesCounterTester(unittest.TestCase):
    def test_getValidMessagesCount_noLoopInRules_correctCountReturned(self):
        rules, messages = getInput(TEST_INPUT_FILE)
        validMessagesCounter = ValidMessagesCounter(rules, messages)
        validMessagesCounter.decipherRules()
        self.assertEqual(validMessagesCounter.getValidMessagesCount(), 3)

    def test_getValidMessagesCount_loopInRules_correctCountReturned(self):
        rules, messages = getInput(TEST_INPUT_FILE)
        validMessagesCounterForLoopyRules = ValidMessagesCounterForLoopyRules(rules, messages)
        validMessagesCounterForLoopyRules.updateSpecificRules()
        self.assertEqual(validMessagesCounterForLoopyRules.getValidMessagesCount(), 12)


if __name__ == '__main__':
    # main()
    unittest.main()

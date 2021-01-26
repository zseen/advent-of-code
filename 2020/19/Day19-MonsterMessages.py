import unittest
from typing import List, Dict, Optional
import re

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

RuleNumberToRule = Dict[int, List[str]]
RuleNumToDecipheredValue = Dict[int, str]


class ValidMessagesCounter:
    def __init__(self, rules: RuleNumberToRule, messages: List[str]):
        self._rules = rules
        self._messages = messages
        self._ruleNumToDecipheredValue: RuleNumToDecipheredValue = dict()

    def getValidMessagesCount(self) -> int:
        return len([message for message in self._messages if self._isMessageValid(message)])

    def decipherRules(self) -> None:
        self._ruleNumToDecipheredValue = self._decipherBaseRules()

        unresolvedRules = set(self._rules).difference(set(self._ruleNumToDecipheredValue))
        while unresolvedRules:
            for ruleNumber, rules in self._rules.items():
                if ruleNumber not in self._ruleNumToDecipheredValue:
                    decipheredValue = self._createDecipheredValueFromValues(rules)
                    if decipheredValue is not None:
                        self._ruleNumToDecipheredValue[ruleNumber] = "(" + decipheredValue + ")"
                        unresolvedRules.remove(ruleNumber)

    def _decipherBaseRules(self) -> RuleNumToDecipheredValue:
        decipheredNumToValues: RuleNumToDecipheredValue = dict()
        for ruleNumber, rule in self._rules.items():
            if "a" in rule:
                decipheredNumToValues[ruleNumber] = "a"
            elif "b" in rule:
                decipheredNumToValues[ruleNumber] = "b"

        return decipheredNumToValues

    def _createDecipheredValueFromValues(self, values: List[str]) -> Optional[str]:
        decipheredValue: str = ""
        for value in values:
            if value.isnumeric() and int(value) not in self._ruleNumToDecipheredValue:
                return None

            decipheredValue += self._buildDecipheredValue(value)

        assert decipheredValue is not None
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


class ValidMessagesCounterForLoopedRules(ValidMessagesCounter):
    def __init__(self, rules: RuleNumberToRule, messages: List[str]):
        super().__init__(rules, messages)
        self._ruleNumToDecipheredValue: RuleNumToDecipheredValue = dict()

    def decipherRules(self) -> None:
        super().decipherRules()

        if not 8 in self._ruleNumToDecipheredValue or not 11 in self._ruleNumToDecipheredValue or not 0 in self._ruleNumToDecipheredValue:
            raise ValueError("8, 11, or 0 not in ruleNumToDecipheredValue.")

        self._ruleNumToDecipheredValue[8] = "{}{}{}{}".format("(", self._ruleNumToDecipheredValue[42], "+", ")")
        self._ruleNumToDecipheredValue[11] = "{}{}{}".format("(", self._getRegexBodyForEleven(), ")")
        self._ruleNumToDecipheredValue[0] = self._ruleNumToDecipheredValue[8] + self._ruleNumToDecipheredValue[11]

    def _getRegexBodyForEleven(self) -> str:
        if not 42 in self._ruleNumToDecipheredValue or not 31 in self._ruleNumToDecipheredValue:
            raise ValueError("42 or 31 not in ruleNumToDecipheredValue.")

        regexBodyForElevenParts = [
            "{}{}{}{}{}{}{}{}".format(self._ruleNumToDecipheredValue[42], "{", str(i), "}", self._ruleNumToDecipheredValue[31], "{", str(i), "}") for
            i in range(1, 5)]
        
        return "|".join(regexBodyForElevenParts)


def getInput(fileName: str) -> (RuleNumberToRule, List[str]):
    rules: RuleNumberToRule = dict()

    with open(fileName, "r") as inputFile:
        lines = inputFile.read()
        linesChunks = lines.split("\n\n")

        rawRules: List = linesChunks[0].split("\n")
        for rawRule in rawRules:
            rawRuleSplit = rawRule.split(": ")
            rules[int(rawRuleSplit[0])] = rawRuleSplit[1].strip('"').split(" ")

        messages: List[str] = linesChunks[1].split("\n")

    return rules, messages


def main():
    rules, messages = getInput(INPUT_FILE)

    validMessagesCounter = ValidMessagesCounter(rules, messages)
    validMessagesCounter.decipherRules()
    print(validMessagesCounter.getValidMessagesCount())  # 187

    validMessagesCounterForLoopedRules = ValidMessagesCounterForLoopedRules(rules, messages)
    validMessagesCounterForLoopedRules.decipherRules()
    print(validMessagesCounterForLoopedRules.getValidMessagesCount())  # 392


class ValidMessagesCounterTester(unittest.TestCase):
    def test_getValidMessagesCount_noLoopInRules_correctCountReturned(self):
        rules, messages = getInput(TEST_INPUT_FILE)
        validMessagesCounter = ValidMessagesCounter(rules, messages)
        validMessagesCounter.decipherRules()
        self.assertEqual(validMessagesCounter.getValidMessagesCount(), 3)

    def test_getValidMessagesCount_loopInRules_correctCountReturned(self):
        rules, messages = getInput(TEST_INPUT_FILE)
        validMessagesCounterForLoopedRules = ValidMessagesCounterForLoopedRules(rules, messages)
        validMessagesCounterForLoopedRules.decipherRules()
        self.assertEqual(validMessagesCounterForLoopedRules.getValidMessagesCount(), 12)


if __name__ == '__main__':
    # main()
    unittest.main()

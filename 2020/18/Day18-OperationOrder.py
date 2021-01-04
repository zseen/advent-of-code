import unittest
from typing import List, Tuple
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

ADDITION = "+"
MULTIPLICATION = "*"
OPENING_PARENTHESIS = "("
CLOSING_PARENTHESIS = ")"


class OperationOrder(Enum):
    NO_PREFERENCE = "no preference",
    ADDITION_PREFERENCE = "addition preference"


class Calculator:
    def __init__(self, expression: str, operationOrder: Enum):
        self._expression: List[str] = list(expression.replace(" ", ""))
        self._operationOrder = operationOrder

    def evaluate(self) -> int:
        while OPENING_PARENTHESIS in self._expression:
            index = self._expression.index(OPENING_PARENTHESIS)
            self._extractInnermostParenthesis(index)

        return self.evaluateWithoutParentheses()

    def _extractInnermostParenthesis(self, startingIndex: int) -> None:
        lastOpeningParenthesisIndex, closingParenthesisIndex = self._findInnermostOpeningParenthesisIndex(startingIndex)
        evaluatedSubExpression = str(self.evaluateWithoutParentheses(lastOpeningParenthesisIndex + 1,
                                                                     closingParenthesisIndex))
        self._substitutePartInExpression(evaluatedSubExpression, lastOpeningParenthesisIndex, closingParenthesisIndex)

    def _findInnermostOpeningParenthesisIndex(self, startingIndex: int) -> Tuple[int, int]:
        if startingIndex > len(self._expression):
            raise ValueError("Starting index larger than expression length.")

        lastOpeningParenthesesIndex: int = 0
        for i in range(startingIndex, len(self._expression)):
            if self._expression[i] == OPENING_PARENTHESIS:
                lastOpeningParenthesesIndex = i
            elif self._expression[i] == CLOSING_PARENTHESIS:
                return (lastOpeningParenthesesIndex, i)

    def _substitutePartInExpression(self, evaluatedSubExpression: str, startingPosition: int, endingPosition: int) -> None:
        if startingPosition >= len(self._expression) or endingPosition >= len(self._expression):
            raise ValueError("Starting or ending index larger than expression length.")

        self._expression[startingPosition] = str(evaluatedSubExpression)
        del self._expression[startingPosition + 1: endingPosition + 1]

    def evaluateWithoutParentheses(self, startingIndex=None, endingIndex=None) -> int:
        if startingIndex is None or endingIndex is None:
            startingIndex = 0
            endingIndex = len(self._expression)

        if self._operationOrder == OperationOrder.ADDITION_PREFERENCE:
            return Calculator._calculateOperationsWithPrecedence(self._expression[startingIndex: endingIndex])

        return Calculator._calculateOperationsWithoutPrecedence(self._expression[startingIndex: endingIndex])

    @staticmethod
    def _calculateOperationsWithPrecedence(expression: List[str]) -> int:
        Calculator._evaluateAllAdditions(expression)
        Calculator._evaluateAllMultiplications(expression)

        if not expression or not expression[0].isnumeric():
            raise ValueError("Error after evaluating additions and multiplications.")

        return int(expression[0])

    @staticmethod
    def _evaluateAllAdditions(expression: List[str]) -> None:
        while ADDITION in expression:
            additionIndex = expression.index(ADDITION)
            Calculator._helpEvaluate(expression, additionIndex, lambda a, b: int(a) + int(b))

    @staticmethod
    def _evaluateAllMultiplications(expression: List[str]) -> None:
        while MULTIPLICATION in expression:
            multiplicationIndex = expression.index(MULTIPLICATION)
            Calculator._helpEvaluate(expression, multiplicationIndex, lambda a, b: int(a) * int(b))

    @staticmethod
    def _calculateOperationsWithoutPrecedence(expression: List[str]) -> int:
        while len(expression) > 1:
            if expression[1] == ADDITION:
                Calculator._helpEvaluate(expression, 1, lambda a, b: int(a) + int(b))
            elif expression[1] == MULTIPLICATION:
                Calculator._helpEvaluate(expression, 1, lambda a, b: int(a) * int(b))
            else:
                raise ValueError("Problem with expression format.")

        if not expression or not expression[0].isnumeric():
            raise ValueError("Error after evaluating additions and multiplications.")

        return int(expression[0])

    @staticmethod
    def _helpEvaluate(expression: List[str], index: int, func: callable):
        result = func(expression[index - 1], expression[index + 1])
        expression[index - 1] = str(result)
        del expression[index: index + 2]


def getExpressions(inputFileName: str) -> List[str]:
    expressions: List[str] = []
    with open(inputFileName, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            expressions.append(line.strip("\n"))
    return expressions


def sumAllExpressions(allExpressions: List[str], operationOrderPreference: Enum) -> int:
    allExpressionsSum = 0
    for expression in allExpressions:
        calculator = Calculator(expression, operationOrderPreference)
        allExpressionsSum += calculator.evaluate()

    return allExpressionsSum


def main():
    allExpressions = getExpressions(INPUT_FILE)

    allExpressionsSumWithoutPrecedence = sumAllExpressions(allExpressions, OperationOrder.NO_PREFERENCE)
    print(allExpressionsSumWithoutPrecedence)  # 45283905029161

    allExpressionsSumWithPrecedence = sumAllExpressions(allExpressions, OperationOrder.ADDITION_PREFERENCE)
    print(allExpressionsSumWithPrecedence)  # 216975281211165


class CalculatorTester(unittest.TestCase):
    def test_evaluate_operationOrderNoPreference_correctSumReturned(self):
        allExpressions = getExpressions(TEST_INPUT_FILE)
        allExpressionsSum = sumAllExpressions(allExpressions, OperationOrder.NO_PREFERENCE)
        self.assertEqual(26457, allExpressionsSum)

    def test_evaluate_operationOrderAdditionPreference_correctSumReturned(self):
        allExpressions = getExpressions(TEST_INPUT_FILE)
        allExpressionsSum = sumAllExpressions(allExpressions, OperationOrder.ADDITION_PREFERENCE)
        self.assertEqual(694173, allExpressionsSum)


if __name__ == '__main__':
    # main()
    unittest.main()

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

    def _extractInnermostParenthesis(self, startingIndex: int):
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
    def _calculateOperationsWithPrecedence(expression) -> int:
        Calculator._evaluateAllAdditions(expression)
        return Calculator._evaluateAllMultiplications(expression)

    @staticmethod
    def _evaluateAllAdditions(expression: List[str]) -> None:
        while ADDITION in expression:
            additionIndex = expression.index(ADDITION)
            evaluatedSubExpression = int(expression[additionIndex - 1]) + int(expression[additionIndex + 1])
            expression[additionIndex - 1] = str(evaluatedSubExpression)
            del expression[additionIndex: additionIndex + 2]


    @staticmethod
    def _evaluateAllMultiplications(expression) -> int:
        currentResult = 1
        for i in range(0, len(expression), 2):
            currentResult *= int(expression[i])
        return currentResult

    @staticmethod
    def _calculateOperationsWithoutPrecedence(expression) -> int:
        result = int(expression[0])
        for i in range(1, len(expression) - 1, 2):
            if expression[i] == ADDITION:
                result += int(expression[i + 1])
            elif expression[i] == MULTIPLICATION:
                result *= int(expression[i + 1])
        return result


def getExpressions(inputFileName: str) -> List[str]:
    expressions: List[str] = []
    with open(inputFileName, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            expressions.append(line.strip("\n"))
    return expressions


def main():
    allExpressions = getExpressions(INPUT_FILE)

    allExpressionsSumWithoutPrecedence = 0
    allExpressionsSumWithPrecedence = 0

    for expression in allExpressions:
        calculatorWithoutPrecedence = Calculator(expression, operationOrderMatters=False)
        calculatorWithPrecedence = Calculator(expression, operationOrderMatters=True)
        allExpressionsSumWithoutPrecedence += calculatorWithoutPrecedence.evaluate()
        allExpressionsSumWithPrecedence += calculatorWithPrecedence.evaluate()

    print(allExpressionsSumWithoutPrecedence)  # 45283905029161
    print(allExpressionsSumWithPrecedence)  # 216975281211165


class CalculatorTester(unittest.TestCase):
    def test_calculate_operationOrderDoesNotMatter_correctSumReturned(self):
        allExpressions = getExpressions(TEST_INPUT_FILE)
        allExpressionsSum = 0
        for expression in allExpressions:
            calculator = Calculator(expression, OperationOrder.NO_PREFERENCE)
            allExpressionsSum += calculator.evaluate()

        self.assertEqual(26457, allExpressionsSum)

    def test_calculate_operationOrderMatters_correctSumReturned(self):
        allExpressions = getExpressions(TEST_INPUT_FILE)
        allExpressionsSum = 0
        for expression in allExpressions:
            calculator = Calculator(expression, OperationOrder.ADDITION_PREFERENCE)
            allExpressionsSum += calculator.evaluate()

        self.assertEqual(694173, allExpressionsSum)


if __name__ == '__main__':
    # main()
    unittest.main()

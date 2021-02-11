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
    def __init__(self, expression: str, operationOrder: OperationOrder):
        self._expression: List[str] = list(expression.replace(" ", ""))
        self._operationOrder = operationOrder

    def evaluate(self) -> int:
        while OPENING_PARENTHESIS in self._expression:
            index = self._expression.index(OPENING_PARENTHESIS)
            self._extractInnermostParenthesis(index)

        return self.evaluateWithoutParentheses()

    def _extractInnermostParenthesis(self, startingIndex: int) -> None:
        openingParenthesisIndex, closingParenthesisIndex = self._findFirstClosedParenthesisIndices(startingIndex)
        evaluatedSubExpression = str(self.evaluateWithoutParentheses(openingParenthesisIndex + 1,
                                                                     closingParenthesisIndex))
        Calculator._replaceNTokensWithOne(self._expression, openingParenthesisIndex, closingParenthesisIndex, evaluatedSubExpression)

    def _findFirstClosedParenthesisIndices(self, startingIndex: int) -> Tuple[int, int]:
        if startingIndex > len(self._expression):
            raise ValueError("Starting index larger than expression length.")

        lastOpeningParenthesisIndex: int = 0
        for i in range(startingIndex, len(self._expression)):
            if self._expression[i] == OPENING_PARENTHESIS:
                lastOpeningParenthesisIndex = i
            elif self._expression[i] == CLOSING_PARENTHESIS:
                return (lastOpeningParenthesisIndex, i)

    def evaluateWithoutParentheses(self, startingIndex=None, endingIndex=None) -> int:
        if startingIndex is None or endingIndex is None:
            startingIndex = 0
            endingIndex = len(self._expression)

        if self._operationOrder == OperationOrder.ADDITION_PREFERENCE:
            return Calculator._calculateOperationsWithAdditionPrecedence(self._expression[startingIndex: endingIndex])

        return Calculator._calculateOperationsWithoutPrecedence(self._expression[startingIndex: endingIndex])

    @staticmethod
    def _calculateOperationsWithAdditionPrecedence(expression: List[str]) -> int:
        Calculator._evaluateAllAdditions(expression)
        Calculator._evaluateAllMultiplications(expression)

        if not expression or not expression[0].isnumeric():
            raise ValueError("Error after evaluating additions and multiplications.")

        return int(expression[0])

    @staticmethod
    def _evaluateAllAdditions(expression: List[str]) -> None:
        while ADDITION in expression:
            additionIndex = expression.index(ADDITION)
            Calculator._evaluateSingleExpression(expression, additionIndex, lambda a, b: int(a) + int(b))

    @staticmethod
    def _evaluateAllMultiplications(expression: List[str]) -> None:
        while MULTIPLICATION in expression:
            multiplicationIndex = expression.index(MULTIPLICATION)
            Calculator._evaluateSingleExpression(expression, multiplicationIndex, lambda a, b: int(a) * int(b))

    @staticmethod
    def _calculateOperationsWithoutPrecedence(expression: List[str]) -> int:
        while len(expression) > 1:
            if expression[1] == ADDITION:
                Calculator._evaluateSingleExpression(expression, 1, lambda a, b: int(a) + int(b))
            elif expression[1] == MULTIPLICATION:
                Calculator._evaluateSingleExpression(expression, 1, lambda a, b: int(a) * int(b))
            else:
                raise ValueError("Problem with expression format.")

        if not expression or not expression[0].isnumeric():
            raise ValueError("Error after evaluating additions and multiplications.")

        return int(expression[0])

    @staticmethod
    def _evaluateSingleExpression(expression: List[str], index: int, func: callable):
        result = func(expression[index - 1], expression[index + 1])
        Calculator._replaceNTokensWithOne(expression, index - 1, index + 1, str(result))

    @staticmethod
    def _replaceNTokensWithOne(expression: List[str], startIndex: int, endIndex: int, toReplaceWith: str) -> None:
        if not expression or startIndex > len(expression) or endIndex > len(expression):
            raise ValueError("Cannot replace token, as expression is not long enough.")

        expression[startIndex] = str(toReplaceWith)
        del expression[startIndex + 1: endIndex + 1]


def getExpressions(inputFileName: str) -> List[str]:
    expressions: List[str] = []
    with open(inputFileName, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            expressions.append(line.strip("\n"))
    return expressions


def sumAllExpressions(allExpressions: List[str], operationOrderPreference: OperationOrder) -> int:
    return sum(Calculator(expression, operationOrderPreference).evaluate() for expression in allExpressions)


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

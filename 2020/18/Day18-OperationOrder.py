import unittest
from typing import List
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"


class Operation(Enum):
    ADDITION = "+"
    MULTIPLICATION = "*"
    OPENING_PARENTHESIS = "("
    CLOSING_PARENTHESIS = ")"


class Calculator:
    def __init__(self, expression: str, operationOrderMatters: bool):
        self._expression: List[str] = list(expression.replace(" ", ""))
        self._operationOrderMatters = operationOrderMatters

    def evaluate(self) -> int:
        i = 0
        while Operation.OPENING_PARENTHESIS.value in self._expression and i < len(self._expression):
            if self._expression[i] == Operation.OPENING_PARENTHESIS.value:
                self._extractInnermostParenthesesStartingFromIndex(i)
                i = 0
            else:
                i += 1

        return self._calculateOperations()

    def _extractInnermostParenthesesStartingFromIndex(self, startingIndex: int) -> None:
        if startingIndex > len(self._expression):
            raise ValueError("Double check index and expression length when attempting to extract parentheses.")

        lastOpeningParenthesesIndex: int = 0
        expressionChunk: List[str] = self._expression[startingIndex:]
        for i in range(0, len(expressionChunk)):
            if expressionChunk[i] == Operation.OPENING_PARENTHESIS.value:
                lastOpeningParenthesesIndex = i
            elif expressionChunk[i] == Operation.CLOSING_PARENTHESIS.value:
                extract = self._calculateOperations(expressionChunk[lastOpeningParenthesesIndex + 1: i])
                self._modifyExpressionWithExtract(extract, startingIndex + lastOpeningParenthesesIndex, startingIndex + i)
                break

    def _modifyExpressionWithExtract(self, extract, startingPosition, endingPosition) -> None:
        if startingPosition >= len(self._expression) or endingPosition >= len(self._expression):
            raise ValueError("Double check indexes and expression when modifying the expression.")

        self._expression[startingPosition] = str(extract)
        del self._expression[startingPosition + 1: endingPosition + 1]

    def _calculateOperations(self, expressionChunk=None):
        if not expressionChunk:
            expressionChunk = self._expression

        if self._operationOrderMatters:
            return Calculator._calculateOperationsWithPrecedence(expressionChunk)

        return Calculator._calculateOperationsWithoutPrecedence(expressionChunk)

    @staticmethod
    def _calculateOperationsWithPrecedence(expressionChunk):
        Calculator._extractAddition(expressionChunk)
        return Calculator._carryOutMultiplication(expressionChunk)

    @staticmethod
    def _extractAddition(expressionChunk: List[str]) -> None:
        i = 1
        while Operation.ADDITION.value in expressionChunk:
            if expressionChunk[i] == Operation.ADDITION.value:
                extract = int(expressionChunk[i - 1]) + int(expressionChunk[i + 1])
                expressionChunk[i - 1] = str(extract)
                del expressionChunk[i: i + 2]
                i = 0
            i += 1

    @staticmethod
    def _carryOutMultiplication(expressionChunk):
        currentResult = 1
        for i in range(0, len(expressionChunk), 2):
            currentResult *= int(expressionChunk[i])
        return currentResult

    @staticmethod
    def _calculateOperationsWithoutPrecedence(expressionChunk):
        result = int(expressionChunk[0])
        for i in range(1, len(expressionChunk) - 1, 2):
            if expressionChunk[i] == Operation.ADDITION.value:
                result += int(expressionChunk[i + 1])
            elif expressionChunk[i] == Operation.MULTIPLICATION.value:
                result *= int(expressionChunk[i + 1])
        return result


def getExpressions(inputFile: str):
    expressions = []
    with open(inputFile, "r") as inputFile:
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
            calculator = Calculator(expression, operationOrderMatters=False)
            allExpressionsSum += calculator.evaluate()

        self.assertEqual(26457, allExpressionsSum)

    def test_calculate_operationOrderMatters_correctSumReturned(self):
        allExpressions = getExpressions(TEST_INPUT_FILE)
        allExpressionsSum = 0
        for expression in allExpressions:
            calculator = Calculator(expression, operationOrderMatters=True)
            allExpressionsSum += calculator.evaluate()

        self.assertEqual(694173, allExpressionsSum)


if __name__ == '__main__':
    # main()
    unittest.main()

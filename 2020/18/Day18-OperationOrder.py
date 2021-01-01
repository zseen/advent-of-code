import unittest

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

FIRST_EXAMPLE = "1 + 2 * 3 + 4 * 5 + 6"
SECOND_EXAMPLE = "1 + (2 * 3) + (4 * (5 + 6))"  # 51
THIRD_EXAMPLE = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))" # 12240
FOURTH_EXAMPLE = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2" # 13632

class Calculator:
    def __init__(self, expression: str):
        self.expression = list(expression.replace(" ", ""))

    def calculate(self):
        i = 0
        while "(" in set(self.expression):
            if self.expression[i] == "(":
                self.extractParentheses(i)
                i = 0
            else:
                i += 1

        return self.calculateSumOrProduct(self.expression)

    def extractParentheses(self, offset):
        lastOpeningParenthesesIndex = None
        expressionChunk = self.expression[offset:]
        for j in range(0, len(expressionChunk)):
            if expressionChunk[j] == "(":
                lastOpeningParenthesesIndex = j
            elif expressionChunk[j] == ")":
                subResult = self.calculateSumOrProduct(expressionChunk[lastOpeningParenthesesIndex + 1: j])
                self.expression[offset + lastOpeningParenthesesIndex] = str(subResult)
                del self.expression[offset + lastOpeningParenthesesIndex + 1: offset + j + 1]
                break



    def calculateSumOrProduct(self, expressionChunk):
        if not expressionChunk or not expressionChunk[0].isnumeric():
            raise ValueError("Invalid expression chunk received.")

        currentResult = int(expressionChunk[0])
        i = 1
        while i < len(expressionChunk) - 1:
            if expressionChunk[i] == "+":
                currentResult += int(expressionChunk[i+1])
            elif expressionChunk[i] == "*":
                currentResult *= int(expressionChunk[i+1])
            i += 2

        return currentResult



def getInput(inputFile: str):
    expressions = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            expressions.append(line)
    return expressions


allExpressions = getInput(INPUT_FILE)

sums = 0
for expression in allExpressions:
    c = Calculator(expression)
    sums += c.calculate()

print(sums)





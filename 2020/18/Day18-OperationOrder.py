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
        while "(" in self.expression or ")" in self.expression and i < len(self.expression):
            if self.expression[i] == "(":
                self.findInnermostParentheses(i)
                i = 0
            else:
                i += 1

        print(self.expression)

        currentResult = self.calculateSumOrProduct(self.expression)

        return currentResult




    def findInnermostParentheses(self, currentExpressionIndex):
        lastOpeningParenthesesIndex = None
        expressionChunk = self.expression[currentExpressionIndex:]
        for j in range(0, len(expressionChunk)):
            if expressionChunk[j] == "(":
                lastOpeningParenthesesIndex = j
            elif expressionChunk[j] == ")":
                subResult = self.calculateSumOrProduct(expressionChunk[lastOpeningParenthesesIndex + 1: j])
                self.expression[currentExpressionIndex + lastOpeningParenthesesIndex] = str(subResult)
                del self.expression[currentExpressionIndex + lastOpeningParenthesesIndex+1: currentExpressionIndex+ j+1]
                break



    def calculateSumOrProduct(self, expressionChunk):
        currentResult = int(expressionChunk[0])
        i = 1
        while i < len(expressionChunk) - 1:
            if expressionChunk[i] == "+":
                numToAdd = ""
                j = i + 1
                while j < len(expressionChunk) and expressionChunk[j].isdigit():
                    numToAdd += expressionChunk[j]
                    j += 1
                currentResult += int(numToAdd)
                i = j
            elif expressionChunk[i] == "*":
                numToAdd = ""
                j = i + 1
                while j < len(expressionChunk) and expressionChunk[j].isdigit():
                    numToAdd += expressionChunk[j]
                    j += 1

                currentResult *= int(numToAdd)
                i = j
            #i += 1
        #print(currentResult)
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





import unittest
from typing import List, Dict
from collections import deque

INPUT_FILE = "input.txt"
TEST_INPUT_FILE_SHORT = "test_input_short.txt"
TEST_INPUT_FILE_LONG = "test_input_long.txt"
SHINY_GOLD = "shiny gold"


class Bag:
    def __init__(self, color: str):
        self.color = color
        self.content: List[Dict[str, int]] = []


class BagAnalyzer:
    def __init__(self, allBagsToContent):
        self.allBagsToContent = allBagsToContent

    def getAllBagsContainingTargetColoredBagRecursively(self, targetColor):
        bagsContainingTargetDirectly: List[Bag] = self._getBagsContainingTargetDirectly(targetColor)

        bagsContainingTargetBagRecursively = set(bagsContainingTargetDirectly)
        bagsToVisit = deque()
        visitedBags = set()

        for bag in bagsContainingTargetDirectly:
            bagsToVisit.appendleft(bag)

        while bagsToVisit:
            currentBag = bagsToVisit.pop()
            for bag in self.allBagsToContent:
                if bag in visitedBags:
                    continue
                for bagContent in bag.content:
                    if currentBag.color in bagContent:
                        bagsContainingTargetBagRecursively.add(bag)
                        bagsToVisit.appendleft(bag)
            visitedBags.add(currentBag)

        return len(bagsContainingTargetBagRecursively)

    def countAllBagsInsideTargetColoredBag(self, targetColor):
        targetBag = self._getBagByColor(targetColor)
        return self._countBagsInsideBag(targetBag, 1) - 1

    def _getBagByColor(self, color):
        for bag in self.allBagsToContent:
            if bag.color == color:
                return bag
        raise ValueError("No bag with such color found.")

    def _countBagsInsideBag(self, bag, bagQuantity):
        allBagsCount = bagQuantity
        for nodeData in bag.content:
            for color, quantity in nodeData.items():
                nextBag = self._getBagByColor(color)
                allBagsCount += self._countBagsInsideBag(nextBag, bagQuantity * quantity)
        return allBagsCount

    def _getBagsContainingTargetDirectly(self, targetBagColor):
        bagsContainingTargetDirectly = []
        for bag in self.allBagsToContent:
            for bagColors in bag.content:
                if targetBagColor in bagColors:
                    bagsContainingTargetDirectly.append(bag)
        return bagsContainingTargetDirectly


def getInput(inputFile):
    allBagsToContents = {}
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" ")
            mainBag = createBagFromLine(line)
            allBagsToContents[mainBag] = mainBag.content

    return allBagsToContents


def createBagFromLine(line: List):
    mainBagColor = " ".join(line[0:2])
    mainBag = Bag(mainBagColor)
    bagsInsideMainBagColorToQuantity = []
    quantity = 0
    color = None
    for i in range(4, len(line)):
        if i % 4 == 0:
            if line[i] == "no":
                quantity = 0
            else:
                quantity = int(line[i])
        elif i % 4 == 1:
            color = " ".join(line[i:i + 2])
        if color and quantity:
            bagsInsideMainBagColorToQuantity.append({color: quantity})
        color = None

    mainBag.content = bagsInsideMainBagColorToQuantity
    return mainBag


def main():
    allBags = getInput(INPUT_FILE)
    bagAnalyzer = BagAnalyzer(allBags)
    target = SHINY_GOLD

    allBagsContainingTarget = bagAnalyzer.getAllBagsContainingTargetColoredBagRecursively(target)
    print(allBagsContainingTarget)  # 229

    allBagsCountInTarget = bagAnalyzer.countAllBagsInsideTargetColoredBag(target)
    print(allBagsCountInTarget)  # 6683


class BagsCounterTest(unittest.TestCase):
    def test_getAllBagsContainingTargetRecursively_correctBagsNumReturned(self):
        allBags = getInput(TEST_INPUT_FILE_SHORT)
        bagAnalyzer = BagAnalyzer(allBags)
        targetColor = SHINY_GOLD
        numAllBagsContainingTargetColoredBag = bagAnalyzer.getAllBagsContainingTargetColoredBagRecursively(
            targetColor)
        self.assertEqual(4, numAllBagsContainingTargetColoredBag)

    def test_countAllBagsInsideTargetColoredBag_shorterInput_correctBagsInsideNumReturned(self):
        allBags = getInput(TEST_INPUT_FILE_SHORT)
        bagAnalyzer = BagAnalyzer(allBags)
        targetColor = SHINY_GOLD
        numAllBagsInsideTarget = bagAnalyzer.countAllBagsInsideTargetColoredBag(targetColor)
        self.assertEqual(32, numAllBagsInsideTarget)

    def test_countAllBagsInsideTargetColoredBag_longerInput_correctBagsInsideNumReturned(self):
        allBags = getInput(TEST_INPUT_FILE_LONG)
        bagAnalyzer = BagAnalyzer(allBags)
        targetColor = SHINY_GOLD
        numAllBagsInsideTarget = bagAnalyzer.countAllBagsInsideTargetColoredBag(targetColor)
        self.assertEqual(126, numAllBagsInsideTarget)


if __name__ == '__main__':
    # main()
    unittest.main()

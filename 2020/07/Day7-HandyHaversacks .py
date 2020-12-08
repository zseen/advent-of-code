import unittest
from typing import List, Dict
from collections import deque

INPUT_FILE = "input.txt"
TEST_INPUT_FILE_SHORT = "test_input_short.txt"
TEST_INPUT_FILE_LONG = "test_input_long.txt"
SHINY_GOLD = "shiny gold"


class Bag:
    def __init__(self, colour: str):
        self.colour = colour
        self.content: List[Dict[str:int]] = []


class AllBagsToContent:
    def __init__(self, allBagsToContent):
        self.allBagsToContent = allBagsToContent

    def getAllBagsContainingTargetColouredBagDirectlyOrIndirectly(self, targetColour):
        bagsDirect: List[Bag] = self._getBagsContainingTargetDirectly(targetColour)

        bagsContainingTargetBag = set(bagsDirect)
        bagsToVisit = deque()
        visitedBags = set()

        for bag in bagsDirect:
            bagsToVisit.appendleft(bag)

        while bagsToVisit:
            currentBag = bagsToVisit.pop()
            for bag in self.allBagsToContent:
                if bag not in visitedBags:
                    for bagContent in bag.content:
                        if currentBag.colour in bagContent:
                            bagsContainingTargetBag.add(bag)
                            bagsToVisit.appendleft(bag)
            visitedBags.add(currentBag)

        return len(bagsContainingTargetBag)

    def getBagByColour(self, colour):
        for bag in self.allBagsToContent:
            if bag.colour == colour:
                return bag
        raise ValueError("No bag with such colour found.")

    def countAllBagsInsideTargetColouredBag(self, targetColour):
        targetBag = self.getBagByColour(targetColour)

        def countBagsInsideBag(bag, bagQuantity):
            allBagsCount = bagQuantity
            for nodeData in bag.content:
                for colour, quantity in nodeData.items():
                    # The "self" part below looks bad
                    nextBag = AllBagsToContent.getBagByColour(self, colour)
                    allBagsCount += countBagsInsideBag(nextBag, bagQuantity * quantity)
            return allBagsCount

        return countBagsInsideBag(targetBag, 1) - 1

    def _getBagsContainingTargetDirectly(self, targetBagColour):
        bagsContainingTargetDirectly = []
        for bag in self.allBagsToContent:
            for bagColours in bag.content:
                if targetBagColour in bagColours:
                    bagsContainingTargetDirectly.append(bag)
        return bagsContainingTargetDirectly


def getInput(inputFile):
    allBagsToContents = {}
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" ")
            mainBag = getAllBagsInsideBagFromLine(line)
            allBagsToContents[mainBag] = mainBag.content

    return allBagsToContents


def getAllBagsInsideBagFromLine(line: List):
    mainBagColour = " ".join(line[0:2])
    mainBag = Bag(mainBagColour)
    bagsInsideMainBagColourToQuantity = []
    quantity = 0
    colour = None
    for i in range(2, len(line)):
        if i % 4 == 0:
            if line[i] == "no":
                quantity = 0
            else:
                quantity = int(line[i])
        elif i % 4 == 1:
            colour = " ".join(line[i:i + 2])
        if colour and quantity:
            bagsInsideMainBagColourToQuantity.append({colour: quantity})
        colour = None

    mainBag.content = bagsInsideMainBagColourToQuantity
    return mainBag


def main():
    allBags = getInput(INPUT_FILE)
    allBagsToContent = AllBagsToContent(allBags)
    target = SHINY_GOLD

    allBagsContainingTarget = allBagsToContent.getAllBagsContainingTargetColouredBagDirectlyOrIndirectly(target)
    print(allBagsContainingTarget)  # 229

    allBagsCountInTarget = allBagsToContent.countAllBagsInsideTargetColouredBag(target)
    print(allBagsCountInTarget)  # 6683


class BagsCounterTest(unittest.TestCase):
    def test_getAllBagsContainingTargetDirectlyOrIndirectly_correctBagsNumReturned(self):
        allBags = getInput(TEST_INPUT_FILE_SHORT)
        allBagsToContent = AllBagsToContent(allBags)
        targetColour = SHINY_GOLD
        allBagsContainingTargetColouredBag = allBagsToContent.getAllBagsContainingTargetColouredBagDirectlyOrIndirectly(
            targetColour)
        self.assertEqual(4, allBagsContainingTargetColouredBag)

    def test_countAllBagsInsideTargetColouredBag_shorterInput_correctBagsInsideNumReturned(self):
        allBags = getInput(TEST_INPUT_FILE_SHORT)
        allBagsToContent = AllBagsToContent(allBags)
        targetColour = SHINY_GOLD
        allBagsInsideTarget = allBagsToContent.countAllBagsInsideTargetColouredBag(targetColour)
        self.assertEqual(32, allBagsInsideTarget)

    def test_countAllBagsInsideTargetColouredBag_longerInput_correctBagsInsideNumReturned(self):
        allBags = getInput(TEST_INPUT_FILE_LONG)
        allBagsToContent = AllBagsToContent(allBags)
        targetColour = SHINY_GOLD
        allBagsInsideTarget = allBagsToContent.countAllBagsInsideTargetColouredBag(targetColour)
        self.assertEqual(126, allBagsInsideTarget)


if __name__ == '__main__':
    # main()
    unittest.main()

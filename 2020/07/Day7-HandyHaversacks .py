import unittest
from typing import List, Dict, Set
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
    def __init__(self, allBagsToContent: Dict[Bag, List[Dict[str, int]]]):
        self.allBagsToContent = allBagsToContent
        self.bagColorToContainingBags: Dict[str, Set[Bag]] = dict()

    def countAllBagsInsideTargetColoredBag(self, targetColor: str) -> int:
        targetBag = self._getBagByColor(targetColor)
        return self._countBagsInsideBag(targetBag, 1) - 1

    def countBagsContainingTargetColoredBagRecursively(self, targetColor: str) -> int:
        if not self.bagColorToContainingBags:
            raise ValueError("Bag colors not analyzed yet.")

        if targetColor not in self.bagColorToContainingBags:
            raise ValueError("No bag with target color found inside any bag.")

        return len(self.bagColorToContainingBags[targetColor])

    def findAllContentBagColorsToContainingBags(self) -> None:
        allContentBagColors = self._findAllContentBagColors()
        for bagColor in allContentBagColors:
            self.bagColorToContainingBags[bagColor] = self._getAllBagsContainingTargetColoredBagRecursively(bagColor)

    def _getBagByColor(self, color: str) -> Bag:
        for bag in self.allBagsToContent:
            if bag.color == color:
                return bag
        raise ValueError("No bag with such color found.")

    def _countBagsInsideBag(self, bag: Bag, bagQuantity: int) -> int:
        allBagsCount = bagQuantity
        for nodeData in bag.content:
            for color, quantity in nodeData.items():
                nextBag = self._getBagByColor(color)
                allBagsCount += self._countBagsInsideBag(nextBag, bagQuantity * quantity)
        return allBagsCount

    def _getBagsContainingTargetDirectly(self, targetBagColor: str) -> List[Bag]:
        bagsContainingTargetDirectly = []
        for bag in self.allBagsToContent:
            for bagColors in bag.content:
                if targetBagColor in bagColors:
                    bagsContainingTargetDirectly.append(bag)
        return bagsContainingTargetDirectly

    def _findAllContentBagColors(self) -> Set[str]:
        allBagColors = set()
        for bag, content in self.allBagsToContent.items():
            for contentColorsToQuantities in content:
                for contentColor in contentColorsToQuantities.keys():
                    allBagColors.add(contentColor)
        return allBagColors

    def _getAllBagsContainingTargetColoredBagRecursively(self, targetColor: str) -> Set[Bag]:
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
        return bagsContainingTargetBagRecursively


def getInput(inputFile: str) -> Dict[Bag, List[Dict[str, int]]]:
    allBagsToContents = {}
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" ")
            mainBag = createBagFromLine(line)
            allBagsToContents[mainBag] = mainBag.content

    return allBagsToContents


def createBagFromLine(line: List[str]) -> Bag:
    # Line format should be like "wavy maroon bags contain 2 dull magenta bags, 3 dark red bags, 5 dull green bags, 4 bright turquoise bags."
    # Format: two adjectives (to describe the main bag's color) + word "bags" + word "contain" + numeral quantity of inside bags + two adjectives (for these inside bags' color) + word "bags"
    # More inside bags could be mentioned in the same sentence, they all have the above mentioned description format

    if len(line) < 3:
        raise ValueError("Invalid line format - line is too short.")

    mainBagColor = " ".join(line[0:2])
    mainBag = Bag(mainBagColor)

    assert "contain" in line
    mainBagContents = line[line.index("contain") + 1:]

    bagsInsideMainBagColorToQuantity = []
    for i in range(0, len(mainBagContents) - 3, 4):
        if not mainBagContents[i].isnumeric():
            break

        quantity = int(mainBagContents[i])
        color = " ".join(mainBagContents[i + 1: i + 3])
        bagsInsideMainBagColorToQuantity.append({color: quantity})

    mainBag.content = bagsInsideMainBagColorToQuantity
    return mainBag


def main():
    allBags = getInput(INPUT_FILE)
    bagAnalyzer = BagAnalyzer(allBags)
    target = SHINY_GOLD

    bagAnalyzer.findAllContentBagColorsToContainingBags()
    allBagsContainingTarget = bagAnalyzer.countBagsContainingTargetColoredBagRecursively(target)
    print(allBagsContainingTarget)  # 229

    allBagsCountInTarget = bagAnalyzer.countAllBagsInsideTargetColoredBag(target)
    print(allBagsCountInTarget)  # 6683


class BagsCounterTest(unittest.TestCase):
    def test_getAllBagsContainingTargetRecursively_correctBagsNumReturned(self):
        allBags = getInput(TEST_INPUT_FILE_SHORT)
        bagAnalyzer = BagAnalyzer(allBags)
        bagAnalyzer.findAllContentBagColorsToContainingBags()
        targetColor = SHINY_GOLD
        numAllBagsContainingTargetColoredBag = bagAnalyzer.countBagsContainingTargetColoredBagRecursively(
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

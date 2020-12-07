import unittest
from typing import List
from collections import deque

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
TEST_INPUT_FILE_SECOND_PART = "test_input_part2.txt"
SHINY_GOLD = "shiny gold"


class Bag:
    def __init__(self, colour: str):
        self.colour = colour
        self.content: List[dict] = []

    def addContentToBag(self, otherBag, otherBagQuantity):
        self.content.append({otherBag: otherBagQuantity})

class AllBagsToContent:
    def __init__(self, allBags, allBagsToContent):
        self.allBags = allBags
        self.allBagsToContent = allBagsToContent


def getAllBagsInsideBagFromLine(line: List):
    mainBagColour = " ". join(line[0:2])
    mainBag = Bag(mainBagColour)
    bagsInsideMainBagColourToQuantity = []
    quantity = 0
    colour = None
    for i in range(2, len(line)):
        if i % 4 == 0:
            if line[i] == "no":
                quantity = 0
                colour = None
            else:
                quantity = int(line[i])
        elif i % 4 == 1:
            colour = " ". join(line[i:i+2])

        if colour and quantity:
            bagsInsideMainBagColourToQuantity.append({colour:quantity})
        colour = None

    mainBag.content = bagsInsideMainBagColourToQuantity
    return mainBag


def getInput(inputFile):
    allBagsToContents = {}
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" ")
            mainBag = getAllBagsInsideBagFromLine(line)
            allBagsToContents[mainBag] = mainBag.content
    #print(allBagsToContents)
    allBagsToContentsClass = AllBagsToContent(allBagsToContents.keys(), allBagsToContents)
    return allBagsToContentsClass



def getBagsContainingTargetDirectly(targetBagColour, allBagsToContent: AllBagsToContent):
    allBags = allBagsToContent.allBagsToContent
    bagsContainingTargetDirectly = []
    #targetBag = getBagByColour(targetBagColour, allBagsToContent)
    for bag in allBags:
        for bagColours in bag.content:
            if targetBagColour in bagColours:
                bagsContainingTargetDirectly.append(bag)
    return bagsContainingTargetDirectly


def getBagByColour(colour, allBagsToContent):
    for bag in allBagsToContent.allBagsToContent:
        if bag.colour == colour:
            return bag


# {<__main__.Bag object at 0x016DC5F8>: [{'bright white': 1}, {'muted yellow': 2}], <__main__.Bag object at 0x016DC700>: [{'bright white': 3}, {'muted yellow': 4}], <__main__.Bag object at 0x016DC748>: [{'shiny gold': 1}], <__main__.Bag object at 0x037FCEF8>: [{'shiny gold': 2}, {'faded blue': 9}], <__main__.Bag object at 0x03815520>: [{'dark olive': 1}, {'vibrant plum': 2}], <__main__.Bag object at 0x03815670>: [{'faded blue': 3}, {'dotted black': 4}], <__main__.Bag object at 0x03858430>: [{'faded blue': 5}, {'dotted black': 6}], <__main__.Bag object at 0x03858460>: [], <__main__.Bag object at 0x03858490>: []}
def getAllBagsContainingTargetDirectlyOrIndirectly(targetColour, allBagsToContent: AllBagsToContent):
    bagsDirect = getBagsContainingTargetDirectly(targetColour, allBagsToContent)
    allBags = allBagsToContent.allBagsToContent

    matches = set(bagsDirect)

    bagsToVisit = deque()
    visitedBags = set()

    for bag in bagsDirect:
        bagsToVisit.appendleft(bag)

    while bagsToVisit:
        currentBag = bagsToVisit.pop()
        for bag in allBags:
            if bag not in visitedBags:
                for bagContent in bag.content:
                    if currentBag.colour in bagContent:
                        matches.add(bag)
                        bagsToVisit.appendleft(bag)

    return len(matches)


def countAllBagsInsideTargetBag(targetColour, allBagsToContent: AllBagsToContent):
    targetBag = getBagByColour(targetColour, allBagsToContent)
    allBags = allBagsToContent.allBagsToContent

    def cost(bag, thisQuantity):
        costy = thisQuantity
        for nodeData in bag.content:
            for colour, quantity in nodeData.items():
                nextBag = getBagByColour(colour, allBagsToContent)
                costy += cost(nextBag, thisQuantity * quantity)
        return costy

    return cost(targetBag, 1) - 1




def getEmptyBags(allBagsToContent: AllBagsToContent):
    allEmpty = []
    for bag in allBagsToContent.allBagsToContent:
        if allBagsToContent.allBagsToContent[bag] == []:
            allEmpty.append(bag)
    return allEmpty


t1 = getInput(TEST_INPUT_FILE)
t2 = getInput(TEST_INPUT_FILE_SECOND_PART)
t3 = getInput(INPUT_FILE)


target = SHINY_GOLD

allBagsCountInTarget = countAllBagsInsideTargetBag(target, t1)
print(allBagsCountInTarget)
allBagsCountInTarget2 = countAllBagsInsideTargetBag(target, t2)
print(allBagsCountInTarget2)

allBagsCoun3 = countAllBagsInsideTargetBag(target, t3)
print(allBagsCoun3)







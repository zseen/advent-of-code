import unittest
import enum

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "inputPractice.txt"


class MapObject(enum.Enum):
    tree = "#"
    square = "."


class StepsInDirections:
    def __init__(self, rightSteps, downSteps):
        self.rightSteps = rightSteps
        self.downSteps = downSteps


class Map:
    def __init__(self, sourceFile):
        self.originalMap = self.getMap(sourceFile)

    def getMap(self, sourceFile):
        originalMap = []
        with open(sourceFile, "r") as inputFile:
            lines = inputFile.readlines()
            for line in lines:
                originalMap.append(line.strip('\n'))
        return originalMap


def countTrees(map: Map, stepsInDirections: StepsInDirections):
    treeCount = 0
    currentRow = 0
    currentColumn = 0
    currentMap = map.originalMap
    bottomIndex = len(map.originalMap) - 1
    mapWidth = len(currentMap[0])

    while currentRow != bottomIndex:
        currentRow += stepsInDirections.downSteps
        currentColumn = (currentColumn + stepsInDirections.rightSteps) % mapWidth
        currentCell = currentMap[currentRow][currentColumn]
        if currentCell == MapObject.tree.value:
            treeCount += 1

    return treeCount


def getTreesCountProductWithDifferentDirections(map, allStepsInDirections):
    allTreesCombined = 1
    for stepsInDirections in allStepsInDirections:
        allTreesCombined *= countTrees(map, stepsInDirections)

    return allTreesCombined


def main():
    mapFromInput = Map(INPUT_FILE)
    allWalkMethodsDirections = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    allStepsInDirections = []
    for walkMethodDirection in allWalkMethodsDirections:
        allStepsInDirections.append(StepsInDirections(walkMethodDirection[0], walkMethodDirection[1]))

    print(countTrees(mapFromInput, StepsInDirections(3, 1)))  # 270
    print(getTreesCountProductWithDifferentDirections(mapFromInput, allStepsInDirections))  # 2122848000


class TreesCountTester(unittest.TestCase):
    def test_countTrees_3stepsRight1StepRight_correctTreesCountReturned(self):
        mapFromInput = Map(TEST_INPUT_FILE)
        treesCount = countTrees(mapFromInput, StepsInDirections(3, 1))
        self.assertEqual(7, treesCount)

    def test_getTreesCountProductWithDifferentDirections_multipleWalkingWays_correctTreesCountProductReturned(self):
        mapFromInput = Map(TEST_INPUT_FILE)
        allWalkMethodsDirections = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
        allStepsInDirections = []
        for walkMethodDirection in allWalkMethodsDirections:
            allStepsInDirections.append(StepsInDirections(walkMethodDirection[0], walkMethodDirection[1]))
        treeCountsProduct = getTreesCountProductWithDifferentDirections(mapFromInput, allStepsInDirections)
        self.assertEqual(336, treeCountsProduct)


if __name__ == '__main__':
    # main()
    unittest.main()

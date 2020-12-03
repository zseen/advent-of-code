import unittest
import enum
from SlopeGradient import SlopeGradient

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
ALL_WALK_METHODS_DIRECTIONS = [SlopeGradient(1, 1), SlopeGradient(3, 1), SlopeGradient(5, 1), SlopeGradient(7, 1),
                               SlopeGradient(1, 2)]


class MapObject(enum.Enum):
    TREE = "#"
    OPEN_SQUARE = "."


class Map:
    def __init__(self, layout):
        self.layout = layout

    def countTrees(self, slopeGradient: SlopeGradient):
        treeCount = 0
        currentRow = 0
        currentColumn = 0
        mapWidth = len(self.layout[0])

        while currentRow < len(self.layout) - 1:
            currentRow += slopeGradient.downSteps
            currentColumn = (currentColumn + slopeGradient.rightSteps) % mapWidth
            currentCell = self.layout[currentRow][currentColumn]
            if currentCell == MapObject.TREE.value:
                treeCount += 1

        return treeCount


def getMap(sourceFile):
    mapLayout = []
    with open(sourceFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            mapLayout.append(line.strip('\n'))
    return mapLayout


def getTreesCountProductWithDifferentDirections(mapFromInput, allStepsInDirections):
    allTreesCombinedProduct = 1
    for stepsInDirections in allStepsInDirections:
        allTreesCombinedProduct *= mapFromInput.countTrees(stepsInDirections)

    return allTreesCombinedProduct


def main():
    mapLayout = getMap(INPUT_FILE)
    mapFromInput = Map(mapLayout)

    THREE_RIGHT_ONE_DOWN = SlopeGradient(3, 1)
    print(mapFromInput.countTrees(THREE_RIGHT_ONE_DOWN))  # 270
    print(getTreesCountProductWithDifferentDirections(mapFromInput, ALL_WALK_METHODS_DIRECTIONS))  # 2122848000


class TreesCountTests(unittest.TestCase):
    def getTestingMap(self):
        mapLayout = getMap(TEST_INPUT_FILE)
        mapFromInput = Map(mapLayout)
        return mapFromInput

    def test_countTrees_3stepsRight1stepDown_correctTreesCountReturned(self):
        mapFromInput = self.getTestingMap()
        THREE_RIGHT_ONE_DOWN = SlopeGradient(3, 1)
        treesCount = mapFromInput.countTrees(THREE_RIGHT_ONE_DOWN)
        self.assertEqual(7, treesCount)

    def test_getTreesCountProductWithDifferentDirections_correctTreesCountProductReturned(self):
        mapFromInput = self.getTestingMap()
        treeCountsProduct = getTreesCountProductWithDifferentDirections(mapFromInput, ALL_WALK_METHODS_DIRECTIONS)
        self.assertEqual(336, treeCountsProduct)


if __name__ == '__main__':
    # main()
    unittest.main()

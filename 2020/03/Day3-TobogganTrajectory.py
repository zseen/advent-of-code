import unittest
import enum

INPUT_FILE = "input.txt"


class MapObject(enum.Enum):
    tree = "#"
    square = "."


class StepsInDirections:
    def __init__(self, rightSteps, downSteps):
        self.rightSteps = rightSteps
        self.downSteps = downSteps


class Map:
    def __init__(self):
        self.originalMap = self.getMap()
        self.repeatedMap = []

    def getMap(self):
        originalMap = []
        with open(INPUT_FILE, "r") as inputFile:
            lines = inputFile.readlines()
            for line in lines:
                originalMap.append(line.strip('\n'))
        return originalMap

    def getRepeatedMap(self, stepsInDirections: StepsInDirections):
        self.repeatedMap = []
        if not self.originalMap:
            raise ValueError("Map not found")

        originalWidth = len(self.originalMap[0])
        rowsCount = len(self.originalMap)

        rightMovemenInOriginalMapCount = originalWidth // stepsInDirections.rightSteps
        repeatNeeded = (rowsCount // rightMovemenInOriginalMapCount // stepsInDirections.downSteps) + 1

        for row in self.originalMap:
            self.repeatedMap.append(row * repeatNeeded)

        return self.repeatedMap


def countTrees(map: Map, stepsInDirections: StepsInDirections):
    treeCount = 0
    currentRow = 0
    currentColumn = 0
    currentMap = map.getRepeatedMap(stepsInDirections)
    bottomIndex = len(map.repeatedMap) - 1

    while currentRow != bottomIndex:
        currentRow += stepsInDirections.downSteps
        currentColumn += stepsInDirections.rightSteps
        currentCell = currentMap[currentRow][currentColumn]
        if currentCell == MapObject.tree.value:
            treeCount += 1

    return treeCount


def getTreesCountWithDifferentDirections(map, allStepsInDirections):
    allTreesCombined = 1
    for stepsInDirections in allStepsInDirections:
        allTreesCombined *= countTrees(map, stepsInDirections)

    return allTreesCombined


def main():
    map = Map()
    allWalkMethodsDirections = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
    allStepsInDirections = []
    for walkMethodDirection in allWalkMethodsDirections:
        allStepsInDirections.append(StepsInDirections(walkMethodDirection[0], walkMethodDirection[1]))

    print(countTrees(map, StepsInDirections(3, 1)))  # 270
    print(getTreesCountWithDifferentDirections(map, allStepsInDirections))  # 2122848000


if __name__ == '__main__':
    main()

import unittest
import enum

INPUT_FILE = "input.txt"

class MapObject(enum.Enum):
    tree = "#"
    square = "."

class Map:
    def __init__(self):
        self.originalWidth = None
        self.originalLength = None
        self.originalMap = []
        self.repeatedMap = []


    def getMap(self):
        with open(INPUT_FILE, "r") as inputFile:
            lines = inputFile.readlines()
            for line in lines:
                self.originalMap.append(line.strip('\n'))


    def getRepeatedMap(self):
        self.getMap()
        if not self.originalMap:
            raise ValueError("Map not found")
        self.originalWidth = len(self.originalMap[0])
        self.originalLength = len(self.originalMap)

        canGoInOneOriginalMap = self.originalWidth // 3
        repeatNeeded = self.originalLength // canGoInOneOriginalMap

        for row in self.originalMap:
            self.repeatedMap.append(row * repeatNeeded)
        return self.repeatedMap


def countTrees(map: Map):
    treeCount = 0
    currentRow = 0
    currentColumn = 0
    # print(map.repeatedMap)
    # #print(map.repeatedMap[currentRow][currentColumn])
    # print(map.repeatedMap[currentRow+1][currentColumn+3])
    # print(map.repeatedMap[currentRow + 2][currentColumn + 6])
    # print(map.repeatedMap[currentRow + 3][currentColumn + 9])
    # print(map.repeatedMap[currentRow + 4][currentColumn + 12])
    # print(map.repeatedMap[currentRow + 5][currentColumn + 15])
    # print(map.repeatedMap[currentRow + 6][currentColumn + 18])
    # print(map.repeatedMap[currentRow + 7][currentColumn + 21])
    # print(map.repeatedMap[currentRow + 8][currentColumn + 24])
    # print(map.repeatedMap[currentRow + 9][currentColumn + 27])
    # print(map.repeatedMap[currentRow + 10][currentColumn + 30])

    while currentRow != map.originalLength - 1:
        currentRow += 1
        currentColumn += 3
        currentCell = map.repeatedMap[currentRow][currentColumn]
        if currentCell == MapObject.tree.value:
            treeCount += 1

    return treeCount




def main():
    map = Map()
    map.getRepeatedMap()
    print(countTrees(map))

if __name__ == '__main__':
    main()

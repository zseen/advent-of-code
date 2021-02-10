import numpy as np
import math
from copy import deepcopy
from typing import List, Dict, Set

from Tile import Tile
from Puzzle import Puzzle
from SeaMonster import SeaMonster

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
SEA_MONSTER_PICTURE_FILE = "seaMonster.txt"




class Sea(Tile):
    def __init__(self, pixelRows, seaMonster: SeaMonster):
        self.pixelRows = pixelRows
        self.seaMonster = seaMonster

    def calculateWaterRoughness(self):
        allRaughnessCount = sum(1 for j in range(0, len(self.pixelRows)) for i in range(0, len(self.pixelRows[j]))
                if self.pixelRows[j][i] == "#")

        return allRaughnessCount - (self._getSeaMonsterCount() * seaMonster.bodyPartsCount)

    def _getSeaMonsterCount(self):
        seaMonstersCount = self._checkForSeaMonsterInBoard()
        if seaMonstersCount:
            return seaMonstersCount

        self.flipSideways()
        seaMonstersCount = self._checkForSeaMonsterInBoard()
        if seaMonstersCount:
            return seaMonstersCount

        raise ValueError("Not a single sea monster...really?")

    def _checkForSeaMonsterInBoard(self) -> int:
        for _ in range(0, 4):
            seaMonsterCount = self._countSeaMonstersInCurrentSeaAlignment()
            if seaMonsterCount > 0:
                return seaMonsterCount
            self.rotateRight()


    def _countSeaMonstersInCurrentSeaAlignment(self):
        seaMonstersCount = 0

        for j in range(1, len(self.pixelRows) - 1):
            for i in range(0, (len(self.pixelRows[j]) - self.seaMonster.length - 1)):
                if self.pixelRows[j][i] == "#":
                    isSeaMonsterPossible = True
                    for seaMonsterCoordinate in self.seaMonster.coordinates:
                        if self.pixelRows[j + seaMonsterCoordinate.y][i + seaMonsterCoordinate.x] != "#":
                            isSeaMonsterPossible = False
                            break
                    if isSeaMonsterPossible:
                        seaMonstersCount += 1

        return seaMonstersCount









def getInput(fileName: str) -> List[Tile]:
    with open(fileName, "r") as inputFile:
        return [createTile(rawTileData) for rawTileData in inputFile.read().split("\n\n")]


def createTile(rawTileData) -> Tile:
    rawTileDataSplit = rawTileData.split()

    if not rawTileDataSplit[1] or not rawTileDataSplit[1][: - 1].isnumeric():
        raise ValueError("Problem with data format after splitting in createTile()")

    tileID = rawTileDataSplit[1][:- 1]
    tiles = list(rawTileDataSplit[2:])

    tile = Tile(tileID, tiles)
    tile.setEdges()

    return tile

def getSeaMonsterInput(fileName) -> List[str]:
    with open(fileName, "r") as inputFile:
        return inputFile.read().split("\n")


def cutEdgesOfCompletedPuzzle(puzzleWithTilesPositioned):
    boardWithTrimmedEdges = []

    rowIndex, columnIndex = 0, 0
    maxRowIndex, maxColumnIndex = len(puzzleWithTilesPositioned), len(puzzleWithTilesPositioned)


    tileRowIndex = 1
    while rowIndex < maxRowIndex and columnIndex < maxColumnIndex:
        while tileRowIndex < len(puzzleWithTilesPositioned[0][0].pixelRows) - 1:
            currentRow = ""
            while columnIndex < len(puzzleWithTilesPositioned[0]):
                currentTile = puzzleWithTilesPositioned[rowIndex][columnIndex]
                for tileColumnIndex in range(1, len(currentTile.pixelRows[0]) - 1):
                    currentRow += currentTile.pixelRows[tileRowIndex][tileColumnIndex]
                columnIndex += 1
            boardWithTrimmedEdges.append(currentRow)
            tileRowIndex += 1
            columnIndex = 0
        rowIndex+= 1
        tileRowIndex = 1

    return boardWithTrimmedEdges





tiles = getInput(TEST_INPUT_FILE)
puzzle = Puzzle(tiles)
puzzle.putPuzzleTogether()
print(puzzle.getCornerTilesIdsProduct() == 20899048083289)

trimmedBoard = cutEdgesOfCompletedPuzzle(puzzle._puzzleWithTilesPositioned)


seaMonster = SeaMonster()
seaMonsterRawInput = getSeaMonsterInput(SEA_MONSTER_PICTURE_FILE)
seaMonster.setCoordinates(seaMonsterRawInput)

sea = Sea(trimmedBoard, seaMonster)

print(sea.calculateWaterRoughness()) #273


#28057939502729
tiles2 = getInput(INPUT_FILE)
puzzle2 = Puzzle(tiles2)
puzzle2.putPuzzleTogether()
print(puzzle2.getCornerTilesIdsProduct() == 28057939502729)

trimmedBoard2 = cutEdgesOfCompletedPuzzle(puzzle2._puzzleWithTilesPositioned)


seaMonster2 = SeaMonster()
seaMonster2.setCoordinates(seaMonsterRawInput)
sea2 = Sea(trimmedBoard2, seaMonster)


print(sea2.calculateWaterRoughness()) # 2489




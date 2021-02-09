import numpy as np
import math
from copy import deepcopy
from typing import List, Dict, Set

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
SEA_MONSTER_PICTURE_FILE = "seaMonster.txt"

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class SeaMonster:
    def __init__(self):
        self.rawInput = []
        self.coordinates: List[Coordinate] = []

    def readInput(self) -> List[List[str]]:
        rawInput = []
        with open(SEA_MONSTER_PICTURE_FILE, "r") as inputFile:
            lines = inputFile.readlines()
            for line in lines:
                emp = []
                line = line.strip("\n\n")
                line = line.strip("\n")

                for char in line:
                    emp.append(char)
                rawInput.append(emp)


        self.rawInput = rawInput
        return rawInput

    def findCoordinates(self):
        self.readInput()
        coordinates = []

        for j in range(0, len(self.rawInput)):
            for i in range(0, len(self.rawInput[j])):
                if self.rawInput[j][i] == "#":
                    coordinates.append(Coordinate(i, j - 1))
        self.coordinates = sorted(coordinates , key=lambda coordinate: coordinate.x)









class Tile:
    def __init__(self, id: str, pixels: List[str]):
        self.id = id
        self.pixels = pixels
        self.topEdge = None
        self.bottomEdge = None
        self.leftEdge = None
        self.rightEdge = None
        self.neighbourTiles = set()


    def setEdges(self):
        if not self.pixels:
            raise ValueError("Problem with setting edges")

        self.topEdge = self.pixels[0]
        self.bottomEdge = self.pixels[-1]
        self.rightEdge = self.buildEdge(-1)
        self.leftEdge = self.buildEdge(0)

    def buildEdge(self, pixelPosition):
        edge = ""
        for item in self.pixels:
            edge += item[pixelPosition]

        return edge
    
    def flipSideways(self):
        self.flipPixelsSideways()
        self.setEdges()

    def flipPixelsSideways(self):
        pixelsReversed: List[str] = []
        for line in self.pixels:
            pixelsReversed.append(line[::-1])

        self.pixels = pixelsReversed
    #build column naming
    def rotateRight(self):
        edges = []
        for i in range(0, len(self.pixels)):
            edges.append(self.buildEdge(i)[::-1])

        self.pixels = edges
        self.setEdges()


class Puzzle:
    def __init__(self, tiles: List[Tile]):
        self.corners: List[Tile] = []
        self.edges: List[Tile] = []
        self.tiles = tiles
        self.correctlyAlignedTiles: Set[Tile] = set()
        self.puzzleWithPiecesPositioned = [[ 0 for _ in range(int(math.sqrt(len(self.tiles))))] for _ in range(int(math.sqrt(len(self.tiles))))]
        self.allAlignedTilePixelsWithoutBorders: List[str] = []


    def puzzleTiles(self):
        while True:
            for i in range(0, len(self.tiles)):
                for j in range(0, len(self.tiles)):
                    if i != j:
                        tile1 = self.tiles[i]
                        tile2 = self.tiles[j]
                        # if self.isAlignmentFound(tile1, tile2):
                        #     self.correctlyAlignedTiles.add(tile1)
                        #     self.correctlyAlignedTiles.add(tile2)
                        if self.areTilesNeighbours(tile1, tile2):
                            tile1.neighbourTiles.add(tile2)
                            tile2.neighbourTiles.add(tile1)


            self.findCorners()
            self.findEdgeTiles()
            self.putPuzzleTogether()
            self.cutEdgesOfCompletedPuzzle()
            return self.calculateProduct()
        
    def isAlignmentFound(self, tile1, tile2):
        if tile1.topEdge == tile2.bottomEdge or tile1.bottomEdge == tile2.topEdge:
            return True

        if tile1.rightEdge == tile2.leftEdge or tile1.leftEdge == tile2.rightEdge:
            return True

        return False

    def areTilesNeighbours(self, tile1: Tile, tile2: Tile):
        for edge in [tile1.topEdge, tile1.bottomEdge, tile1.leftEdge, tile1.rightEdge]:
            if edge in [tile2.topEdge, tile2.bottomEdge, tile2.rightEdge, tile2.leftEdge]:
                return True

        for edge in [tile1.topEdge, tile1.bottomEdge, tile1.leftEdge, tile1.rightEdge]:
            reversedEdge = edge[::-1]
            if reversedEdge in [tile2.topEdge, tile2.bottomEdge, tile2.rightEdge, tile2.leftEdge]:
                return True

        return False

    # def alignTilesToAlredyAlignedTiles(self) -> None:
    #     while True:
    #         for correctlyAlignedTile in list(self.correctlyAlignedTiles):
    #             neighbours = correctlyAlignedTile.neighbourTiles
    #             for neighbour in neighbours:
    #                 if neighbour not in self.correctlyAlignedTiles:
    #                     self.alignTileToAlignedTile(neighbour, correctlyAlignedTile)
    #             if len(self.correctlyAlignedTiles) == len(self.tiles):
    #                 return


    def alignTileToAlignedTile(self, neighbour, correctlyAlignedTile) -> bool:
        for _ in range(0, 4):
            if neighbour.leftEdge == correctlyAlignedTile.rightEdge:
                return True
            neighbour.rotateRight()


        neighbour.flipSideways()
        for _ in range(0, 4):
            if neighbour.leftEdge == correctlyAlignedTile.rightEdge:
                return True
            neighbour.rotateRight()

        neighbour.flipSideways()
        return False



    def calculateProduct(self):
        tilesWithTwoNeighboursIdsProduct = 1
        for tile in self.corners:
            tilesWithTwoNeighboursIdsProduct *= int(tile.id)

        return tilesWithTwoNeighboursIdsProduct

    def findCorners(self):
        for tile in self.tiles:
            if len(tile.neighbourTiles) == 2:
                self.corners.append(tile)

    def findEdgeTiles(self):
        for tile in self.tiles:
            if len(tile.neighbourTiles) == 3:
                self.edges.append(tile)

    def alignNeighbourTopBottomWay(self, neighbour, correctlyAlignedTile):
        for _ in range(0, 4):
            if neighbour.topEdge == correctlyAlignedTile.bottomEdge:
                return True
            neighbour.rotateRight()


        neighbour.flipSideways()
        for _ in range(0, 4):
            if neighbour.topEdge == correctlyAlignedTile.bottomEdge:
                return True
            neighbour.rotateRight()


        neighbour.flipSideways()
        return False



    def putPuzzleTogether(self):
        topLeftCorner = self.findTopLeftCorner()

        self.puzzleWithPiecesPositioned[0][0] = topLeftCorner
        currentTile = topLeftCorner


        # fill up the first row
        for columnIndex in range(1, len(self.puzzleWithPiecesPositioned[0])):
            for neigbour in currentTile.neighbourTiles:
                if self.alignTileToAlignedTile(neigbour, currentTile):
                    self.puzzleWithPiecesPositioned[0][columnIndex] = neigbour
                    currentTile = neigbour


        # fill up the rest
        for j in range(1, len(self.puzzleWithPiecesPositioned)):
            for i in range(0, len(self.puzzleWithPiecesPositioned[0])):
                currentTile = self.puzzleWithPiecesPositioned[j-1][i]
                for neigbour in currentTile.neighbourTiles:
                    if self.alignNeighbourTopBottomWay(neigbour, currentTile):
                        self.puzzleWithPiecesPositioned[j][i] = neigbour


        # for j in range(0, len(self.puzzleWithPiecesPositioned)):
        #     for i in range(0, len(self.puzzleWithPiecesPositioned[0])):
        #         print(self.puzzleWithPiecesPositioned[j][i].id, " ", end="")
        #     print("")



        # boardWithTrimmedEdges = []
        # rowIndex, columnIndex = 0, 0
        # tileJindex = 0
        # while rowIndex < 12 and columnIndex < 12:
        #     while tileJindex < 10:
        #         currentRow = ""
        #         while columnIndex < len(self.puzzleWithPiecesPositioned[0]):
        #             currentTile = self.puzzleWithPiecesPositioned[rowIndex][columnIndex]
        #             for i in range(0, len(currentTile.pixels[0])):
        #                 currentRow += currentTile.pixels[tileJindex][i]
        #             columnIndex += 1
        #         boardWithTrimmedEdges.append(currentRow)
        #         columnIndex = 0
        #         tileJindex += 1
        #     rowIndex += 1
        #     tileJindex = 0
        #
        # ct = 0
        # for line in boardWithTrimmedEdges:
        #     print(line[0:10], " ", line[10:20], " ", line[20:30], " ", line[30:40], " ", line[40:50], " ", line[50:60], " ", line[60:70], " ", line[70:80], " ", line[80:90], " ", line[90:100], " ", line[100:110], " ", line[110:])
        #     ct += 1
        #     if ct == 10:
        #         print("")
        #         ct = 0








    def findTopLeftCorner(self):
        rightNeighbourFound = False
        bottomNeighbourFound = False

        for corner in self.corners:
            neighboursEdges = []

            for neighbour in corner.neighbourTiles:
                neighboursEdges.append(neighbour.topEdge)
                neighboursEdges.append(neighbour.bottomEdge)
                neighboursEdges.append(neighbour.rightEdge)
                neighboursEdges.append(neighbour.leftEdge)

            for _ in range(0, 4):
                if corner.rightEdge in neighboursEdges:
                    rightNeighbourFound = True

                if corner.bottomEdge in neighboursEdges:
                    bottomNeighbourFound = True

                if corner.rightEdge[::-1] in neighboursEdges:
                    rightNeighbourFound = True

                if corner.bottomEdge[::-1] in neighboursEdges:
                    bottomNeighbourFound = True

                if rightNeighbourFound and bottomNeighbourFound:
                    return corner

                rightNeighbourFound = False
                bottomNeighbourFound = False
                corner.rotateRight()


        raise ValueError("Top left corner not found")


    def cutEdgesOfCompletedPuzzle(self):
        boardWithTrimmedEdges = []

        rowIndex, columnIndex = 0, 0

        maxRowIndex, maxColumnIndex = int(math.sqrt(len(self.tiles))), int(math.sqrt(len(self.tiles)))

        tileJindex = 1
        while rowIndex < maxRowIndex and columnIndex < maxColumnIndex:
            while tileJindex < 9:
                currentRow = ""
                while columnIndex < len(self.puzzleWithPiecesPositioned[0]):
                    currentTile = self.puzzleWithPiecesPositioned[rowIndex][columnIndex]
                    for i in range(1, len(currentTile.pixels[0]) - 1):
                        currentRow += currentTile.pixels[tileJindex][i]
                    columnIndex += 1
                boardWithTrimmedEdges.append(currentRow)
                columnIndex = 0
                tileJindex += 1
            rowIndex+= 1
            tileJindex = 1

        boardAsTile = Tile("Board", boardWithTrimmedEdges)
        boardAsTile.setEdges()
        self.allAlignedTilePixelsWithoutBorders = boardAsTile


        # print("-------------------")
        # ct = 0
        # for line in boardWithTrimmedEdges:
        #     print(line[0:8], " ", line[8:16], " ", line[16:])
        #     ct += 1
        #     if ct == 8:
        #         print("")
        #         ct = 0


    def alignBoardToFindSeaMonsters(self, seaMonster):
        for _ in range(0, 4):
            seaMonsterCount = self.countSeaMonstersInBoard(seaMonster)
            if seaMonsterCount > 0:
                #print(self.allAlignedTilePixelsWithoutBorders.topEdge)
                return seaMonsterCount
            self.allAlignedTilePixelsWithoutBorders.rotateRight()


        self.allAlignedTilePixelsWithoutBorders.flipSideways()
        for _ in range(0, 4):
            seaMonsterCount = self.countSeaMonstersInBoard(seaMonster)
            if seaMonsterCount > 0:
                return seaMonsterCount
            self.allAlignedTilePixelsWithoutBorders.rotateRight()


        raise ValueError("Not a single sea monster...really?")



    def countSeaMonstersInBoard(self, seaMonster: SeaMonster):
        seaMonstersCount = 0
        seaMonsterCharsFound = 0
        seaMonsterLength = 20

        for j in range(1, len(self.allAlignedTilePixelsWithoutBorders.pixels) - 1):
            for i in range(0, (len(self.allAlignedTilePixelsWithoutBorders.pixels[j])-seaMonsterLength)):
                if self.allAlignedTilePixelsWithoutBorders.pixels[j][i] == "#":
                    isSeaMonsterPossible = True
                    for seaMonsterCoordinate in seaMonster.coordinates:
                        if self.allAlignedTilePixelsWithoutBorders.pixels[j + seaMonsterCoordinate.y][i + seaMonsterCoordinate.x] != "#":
                            isSeaMonsterPossible = False
                            seaMonsterCharsFound = 0
                            break
                        else:
                            seaMonsterCharsFound += 1
                    if seaMonsterCharsFound == 15 and isSeaMonsterPossible:
                        seaMonstersCount += 1
                        seaMonsterCharsFound = 0

        return seaMonstersCount


    def countWaterRoughness(self, seaMonster):
        allRaughnessCount = 0
        for j in range(0, len(self.allAlignedTilePixelsWithoutBorders.pixels)):
            for i in range(0, len(self.allAlignedTilePixelsWithoutBorders.pixels[j])):
                if self.allAlignedTilePixelsWithoutBorders.pixels[j][i] == "#":
                    allRaughnessCount += 1

        seaMonstersCount = self.alignBoardToFindSeaMonsters(seaMonster)
        print(seaMonstersCount)

        return allRaughnessCount - (seaMonstersCount * 15)






def getInput(fileName: str):
    tiles: List[Tile] = []
    with open(fileName, "r") as inputFile:
        allDataForTiles = inputFile.read()
        allDataForTilesSplit = allDataForTiles.split("\n\n")
        for rawTileData in allDataForTilesSplit:
            tile = createTile(rawTileData)
            tiles.append(tile)

        return tiles


def createTile(rawTileData) -> Tile:
    rawTileDataSplit = rawTileData.split()

    if not rawTileDataSplit[1] or not rawTileDataSplit[1][: - 1].isnumeric():
        raise ValueError("Problem with data format after splitting in createTile()")

    tileID = rawTileDataSplit[1][:- 1]
    tiles = list(rawTileDataSplit[2:])

    tile = Tile(tileID, tiles)
    tile.setEdges()
    return tile



# tiles = getInput(TEST_INPUT_FILE)
# puzzle = Puzzle(tiles)
# print(puzzle.puzzleTiles() == 20899048083289)
# seaMonster = SeaMonster()
# seaMonster.findCoordinates()
# puzzle.cutEdgesOfCompletedPuzzle()
# print(puzzle.countWaterRoughness(seaMonster)) #273


#28057939502729
tiles2 = getInput(INPUT_FILE)
puzzle2 = Puzzle(tiles2)
print(puzzle2.puzzleTiles() == 28057939502729)
seaMonster2 = SeaMonster()
seaMonster2.findCoordinates()
puzzle2.cutEdgesOfCompletedPuzzle()
print(puzzle2.countWaterRoughness(seaMonster2)) # 2489




import numpy as np
import math
from copy import deepcopy
from typing import List, Dict, Set

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"


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
            #if self.isAlignmentFound(neighbour, correctlyAlignedTile):
            if neighbour.leftEdge == correctlyAlignedTile.rightEdge:
                self.correctlyAlignedTiles.add(neighbour)
                return True
            neighbour.rotateRight()


        neighbour.flipSideways()
        for _ in range(0, 4):
            #if self.isAlignmentFound(neighbour, correctlyAlignedTile):
            if neighbour.leftEdge == correctlyAlignedTile.rightEdge:
                self.correctlyAlignedTiles.add(neighbour)
                return True
            neighbour.rotateRight()

        return False
        #raise ValueError("Tiles still dont match properly: ", neighbour.id, correctlyAlignedTile.id)



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
            #if self.isAlignmentFound(neighbour, correctlyAlignedTile):
            if neighbour.topEdge == correctlyAlignedTile.bottomEdge:
                self.correctlyAlignedTiles.add(neighbour)
                return True
            neighbour.rotateRight()


        neighbour.flipSideways()
        for _ in range(0, 4):
            #if self.isAlignmentFound(neighbour, correctlyAlignedTile):
            if neighbour.topEdge == correctlyAlignedTile.bottomEdge:
                self.correctlyAlignedTiles.add(neighbour)
                return True
            neighbour.rotateRight()

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


        for j in range(0, len(self.puzzleWithPiecesPositioned)):
            for i in range(0, len(self.puzzleWithPiecesPositioned[0])):
                print(self.puzzleWithPiecesPositioned[j][i].id, " ", end="")
            print("")


    def findTopLeftCorner(self):
        noTopNeighbour = True
        noLeftNeighbour = True
        for corner in self.corners:
            neighboursEdges = []
            for neighbour in corner.neighbourTiles:
                neighboursEdges.append(neighbour.topEdge)
                neighboursEdges.append(neighbour.bottomEdge)
                neighboursEdges.append(neighbour.rightEdge)
                neighboursEdges.append(neighbour.leftEdge)

            for _ in range(0, 4):
                if corner.topEdge in neighboursEdges:
                    noTopNeighbour = False
                if corner.leftEdge in neighboursEdges:
                    noLeftNeighbour = False

                if noLeftNeighbour and noTopNeighbour:
                    return corner

                noTopNeighbour = True
                noLeftNeighbour = True
                corner.rotateRight()


        raise ValueError("Top left corner not found")


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

# #28057939502729
tiles2 = getInput(INPUT_FILE)
puzzle2 = Puzzle(tiles2)
print(puzzle2.puzzleTiles() == 28057939502729)




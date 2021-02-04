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
        # self.topLeftPixel = None
        # self.topRightPixel = None
        # self.bottomLeftPixel = None
        # self.bottomRightPixel = None
        self.topEdge = None
        self.bottomEdge = None
        self.leftEdge = None
        self.rightEdge = None
        self.neighbourTiles = set()

    def setCornerPixels(self):
        if not self.pixels:
            raise ValueError("Problem with setting corners")

        self.topLeftPixel = self.pixels[0][0]
        self.topRightPixel = self.pixels[0][-1]
        self.bottomLeftPixel = self.pixels[-1][0]
        self.bottomRightPixel = self.pixels[-1][-1]

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

    def flipPixelsSideways(self):
        pixelsReversed: List[str] = []
        for line in self.pixels:
            pixelsReversed.append(line[::-1])

        self.pixels = pixelsReversed


    def flipSideways(self):
        #self.topLeftPixel, self.topRightPixel = self.topRightPixel, self.topLeftPixel
        #self.bottomLeftPixel, self.bottomRightPixel = self.bottomRightPixel, self.bottomLeftPixel
        self.flipPixelsSideways()
        self.setEdges()


    def flipUpsideDown(self):
        #self.bottomLeftPixel, self.topLeftPixel = self.topLeftPixel, self.bottomLeftPixel
        #self.bottomRightPixel, self.topRightPixel = self.topRightPixel, self.bottomRightPixel
        self.pixels = self.pixels[::-1]
        self.setEdges()

    def rotateRight(self):
        # currentTopLeftPixel = self.topLeftPixel
        # self.topLeftPixel = self.bottomLeftPixel
        # currentTopRigtPixel = self.topRightPixel
        # self.topRightPixel = currentTopLeftPixel
        # currentBottomRightPixel = self.bottomRightPixel
        # self.bottomLeftPixel = currentBottomRightPixel
        # self.bottomRightPixel = currentTopRigtPixel

        # currentTopEdge = self.topEdge
        # self.topEdge = self.leftEdge
        #
        # self.leftEdge = self.bottomEdge
        #
        # currentRightEdge = self.rightEdge
        # self.bottomEdge = currentRightEdge
        #
        # self.rightEdge = currentTopEdge

        #emptyMatrix = [ [ 0 for i in range(len(self.pixels[0])) ] for j in range(len(self.pixes)) ]

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
        self.puzzleWithPiecesPositioned = [ [ 0 for _ in range(len(self.tiles[0].topEdge)) ] for _ in range(len(self.tiles)) ]



    def puzzleTiles(self):
        while True:
            for i in range(0, len(self.tiles)):
                for j in range(0, len(self.tiles)):
                    if i != j:
                        tile1 = self.tiles[i]
                        tile2 = self.tiles[j]
                        if self.isAlignmentFound(tile1, tile2):
                            self.correctlyAlignedTiles.add(tile1)
                            self.correctlyAlignedTiles.add(tile2)

                        if self.doTilesAlign(tile1, tile2):
                            tile1.neighbourTiles.add(tile2)
                            tile2.neighbourTiles.add(tile1)


            if len(self.correctlyAlignedTiles) != len(self.tiles):
                self.alignTilesToAlredyAlignedTiles()

            self.findCorners()
            self.findEdges()
            self.putPuzzleTogether()
            return self.calculateProduct()

    def doTilesAlign(self, tile1: Tile, tile2: Tile):
        for edge in [tile1.topEdge, tile1.bottomEdge, tile1.leftEdge, tile1.rightEdge]:
            if edge in [tile2.topEdge, tile2.bottomEdge, tile2.rightEdge, tile2.leftEdge]:
                return True

        for edge in [tile1.topEdge, tile1.bottomEdge, tile1.leftEdge, tile1.rightEdge]:
            reversedEdge = edge[::-1]
            if reversedEdge in [tile2.topEdge, tile2.bottomEdge, tile2.rightEdge, tile2.leftEdge]:
                return True

        return False

    def alignTilesToAlredyAlignedTiles(self):
        while True:
            for correctlyAlignedTile in list(self.correctlyAlignedTiles):
                neighbours = correctlyAlignedTile.neighbourTiles
                for neighbour in neighbours:
                    if neighbour not in self.correctlyAlignedTiles:
                        self.alignTileToAlignedTile(neighbour, correctlyAlignedTile)
                if len(self.correctlyAlignedTiles) == len(self.tiles):
                    return




    def alignTileToAlignedTile(self, neighbour, correctlyAlignedTile) -> None:
        if not self.isHorizontalFlippingNeeded(neighbour, correctlyAlignedTile):
            for _ in range(0, 4):
                if self.isAlignmentFound(neighbour, correctlyAlignedTile):
                    self.correctlyAlignedTiles.add(neighbour)
                    return
                neighbour.rotateRight()


            neighbour.flipUpsideDown()
            for _ in range(0, 4):
                if self.isAlignmentFound(neighbour, correctlyAlignedTile):
                    self.correctlyAlignedTiles.add(neighbour)
                    return
                neighbour.rotateRight()


            raise ValueError("Horizontal flipping was not needed, still not aligning: ", correctlyAlignedTile.id, neighbour.id)

        if self.isHorizontalFlippingNeeded(neighbour, correctlyAlignedTile):
            neighbour.flipSideways()

            for _ in range(0, 4):
                if self.isAlignmentFound(neighbour, correctlyAlignedTile):
                    self.correctlyAlignedTiles.add(neighbour)
                    return
                neighbour.rotateRight()

            neighbour.flipUpsideDown()
            for _ in range(0, 4):
                if self.isAlignmentFound(neighbour, correctlyAlignedTile):
                    self.correctlyAlignedTiles.add(neighbour)
                    return
                neighbour.rotateRight()

        raise ValueError("somehow these tiles still dont align: ", correctlyAlignedTile, neighbour)



    def isHorizontalFlippingNeeded(self, tile1, tile2):
        if tile1.topEdge == tile2.topEdge or tile1.bottomEdge == tile2.bottomEdge:
            return True

        # if tile1.topEdge == tile2.bottomEdge[::-1] or tile1.bottomEdge == tile2.topEdge[::-1]:
        #     return True

        return False



    def isVerticalFlippingNeeded(self, tile1, tile2) -> bool:
        if tile1.leftEdge == tile2.rightEdge[::-1] or tile1.rightEdge == tile2.leftEdge[::-1]:
            return True

        if tile1.leftEdge == tile2.leftEdge or tile1.rightEdge == tile2.rightEdge:
            return True

        return False

        #raise ValueError("It looks like tile1 and tile2 are not neighbours after all.")


    def calculateProduct(self):
        tilesWithTwoNeighboursIdsProduct = 1
        for tile in self.corners:
            tilesWithTwoNeighboursIdsProduct *= int(tile.id)

        return tilesWithTwoNeighboursIdsProduct

    def findCorners(self):
        for tile in self.tiles:
            if len(tile.neighbourTiles) == 2:
                self.corners.append(tile)

    def findEdges(self):
        for tile in self.tiles:
            if len(tile.neighbourTiles) == 3:
                self.edges.append(tile)


    def isAlignmentFound(self, tile1, tile2):
        if tile1.topEdge == tile2.bottomEdge or tile1.bottomEdge == tile2.topEdge:
            return True

        if tile1.rightEdge == tile2.leftEdge or tile1.leftEdge == tile2.rightEdge:
            return True
        return False


    def putPuzzleTogether(self):
        topLeftCorner = self.findTopLeftCorner()
        print(topLeftCorner.id)

    def findTopLeftCorner(self):
    

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
    #tile.setCornerPixels()
    tile.setEdges()
    return tile

tiles = getInput(TEST_INPUT_FILE)
puzzle = Puzzle(tiles)
print(puzzle.puzzleTiles() == 20899048083289)

#28057939502729
tiles2 = getInput(INPUT_FILE)
puzzle2 = Puzzle(tiles2)
print(puzzle2.puzzleTiles() == 28057939502729)


# print(thatOneTile.topEdge)
# print(thatOneTile.rightEdge)
# print(thatOneTile.bottomEdge)
# print(thatOneTile.leftEdge)
#
# thatOneTile.rotateRight()
# print("--------------")
# print(thatOneTile.topEdge)
# print(thatOneTile.rightEdge)
# print(thatOneTile.bottomEdge)
# print(thatOneTile.leftEdge)

# print(thatOneTile.topLeftPixel)
# print(thatOneTile.topRightPixel)
# print(thatOneTile.bottomLeftPixel)
# print(thatOneTile.bottomRightPixel)
#
# thatOneTile.flipUpsideDown()
# print("--------------")
#
# print(thatOneTile.topLeftPixel)
# print(thatOneTile.topRightPixel)
# print(thatOneTile.bottomLeftPixel)
# print(thatOneTile.bottomRightPixel)





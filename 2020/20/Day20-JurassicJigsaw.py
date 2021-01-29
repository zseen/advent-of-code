import numpy as np
import math
from typing import List, Dict

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"


class Tile:
    def __init__(self, id: str, pixels: List[str]):
        self.id = id
        self.pixels = pixels
        self.topLeftPixel = None
        self.topRightPixel = None
        self.bottomLeftPixel = None
        self.bottomRightPixel = None
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

    def flipSideways(self):
        self.topLeftPixel, self.topRightPixel = self.topRightPixel, self.topLeftPixel
        self.bottomLeftPixel, self.bottomRightPixel = self.bottomRightPixel, self.bottomLeftPixel
        self.rightEdge, self.leftEdge = self.leftEdge, self.rightEdge

    def flipUpsideDown(self):
        self.bottomLeftPixel, self.topLeftPixel = self.topLeftPixel, self.bottomLeftPixel
        self.bottomRightPixel, self.topRightPixel = self.topRightPixel, self.bottomRightPixel
        self.topEdge, self.bottomEdge = self.bottomEdge, self.topEdge

    def rotateRight(self):
        currentTopLeftPixel = self.topLeftPixel
        self.topLeftPixel = self.bottomLeftPixel

        currentTopRigtPixel = self.topRightPixel
        self.topRightPixel = currentTopLeftPixel

        currentBottomRightPixel = self.bottomRightPixel
        self.bottomLeftPixel = currentBottomRightPixel

        self.bottomRightPixel = currentTopRigtPixel

        currentTopEdge = self.topEdge
        self.topEdge = self.leftEdge

        self.leftEdge = self.bottomEdge

        currentRightEdge = self.rightEdge
        self.bottomEdge = currentRightEdge

        self.rightEdge = currentTopEdge




    def rotate180Degrees(self):
        for _ in range(0,2):
            self.rotateRight()

    def rotateLeft(self):
        for _ in range(0, 3):
            self.rotateRight()




def puzzleTiles(tiles: List[Tile]):
    piecesPutTogether = 0
    matchAlreadyFound = set()
    completedPuzzleSideLength = int(math.sqrt(len(tiles)))
    sideConnectionsCount = (completedPuzzleSideLength * (completedPuzzleSideLength - 1)) * 2


    while True:
        for i in range(0, len(tiles)):
            for j in range(0, len(tiles)):
                if i != j:
                    v = tiles[i].id
                    c = tiles[j].id
                    if (v, c) in matchAlreadyFound or (c, v) in matchAlreadyFound:
                        continue
                    if doTilesAlign(tiles[i], tiles[j]):
                        piecesPutTogether += 1
                        tiles[i].neighbourTiles.add(tiles[j])
                        tiles[j].neighbourTiles.add(tiles[i])
                        matchAlreadyFound.add((v, c))
        if piecesPutTogether == sideConnectionsCount:
            return calculateProduct(tiles)


def calculateProduct(tiles: List[Tile]):
    tilesWithTwoNeighboursIdsProduct = 1
    for tile in tiles:
        if len(tile.neighbourTiles) == 2:
            tilesWithTwoNeighboursIdsProduct *= int(tile.id)

    return tilesWithTwoNeighboursIdsProduct


def doTilesAlign(tile1: Tile, tile2: Tile):
    for edge in [tile1.topEdge, tile1.bottomEdge, tile1.leftEdge, tile1.rightEdge]:
        b = edge
        if edge  in [tile2.topEdge, tile2.bottomEdge, tile2.rightEdge, tile2.leftEdge]:
            return True

    for edge in [tile1.topEdge, tile1.bottomEdge, tile1.leftEdge, tile1.rightEdge]:
        v = edge
        reversedEdge = edge[::-1]
        c = reversedEdge
        if reversedEdge  in [tile2.topEdge, tile2.bottomEdge, tile2.rightEdge, tile2.leftEdge]:
            return True

    return False




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
    tile.setCornerPixels()
    tile.setEdges()
    return tile


tiles = getInput(INPUT_FILE)
print(puzzleTiles(tiles))


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





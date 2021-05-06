from typing import List, Set, Dict
from enum import Enum
from collections import Counter
from copy import deepcopy

FLOOR_SIZE = 100

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class NeighbourDirection(Enum):
    WEST = "w"
    EAST = "e"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    NORTHEAST = "ne"
    NORTHWEST = "nw"

class TileColour(Enum):
    WHITE = "W"
    BLACK = "B"

class Tile:
    def __init__(self, coordinateX, coordinateY):
        self.coordinates: Coordinates = Coordinates(coordinateX, coordinateY)
        self.colour = TileColour.WHITE

class Lobby:
    def __init__(self, tileFlippingDirectionsCollection: List[List[NeighbourDirection]]):
        self.centreTile = Tile(0, 0)
        self.currentTile = None
        self.tileFlippingDirectionsCollection = tileFlippingDirectionsCollection
        self.blackTilesCount = 0
        self.coordinatesToTile: Dict[str, Tile] = dict()
        self.repeatedVisitCounter = 0
        self.rep = []
        self.blacktiles = []

    def followFlippingDirections(self):
        for tileFlippingDirections in self.tileFlippingDirectionsCollection:
            self._followFlippingDirection(tileFlippingDirections)

    def _followFlippingDirection(self, tileFlippingDirections: List[NeighbourDirection]):
        self.currentTile = self.centreTile

        for direction in tileFlippingDirections:
            self.moveToTile(direction)

        if (str(self.currentTile.coordinates.x) + "," + str(self.currentTile.coordinates.y)) in self.coordinatesToTile:
            self.currentTile = self.coordinatesToTile[str(self.currentTile.coordinates.x) + "," + str(self.currentTile.coordinates.y)]
            self.flipCurrentTile()
        else:
            self.flipCurrentTile()
            self.coordinatesToTile[str(self.currentTile.coordinates.x) + "," + str(self.currentTile.coordinates.y)] = self.currentTile

        #self.tiles.append(self.coordinatesToTile[str(self.currentTile.coordinates.x) + str(self.currentTile.coordinates.y)])
        #self.flipTile(self.coordinatesToTile[str(self.currentTile.coordinates.x) + str(self.currentTile.coordinates.y)])

    def moveToTile(self, direction: NeighbourDirection):
        if direction == NeighbourDirection.WEST:
            self.currentTile = Tile(self.currentTile.coordinates.x - 2, self.currentTile.coordinates.y)
        elif direction == NeighbourDirection.EAST:
            self.currentTile = Tile(self.currentTile.coordinates.x + 2, self.currentTile.coordinates.y)
        elif direction == NeighbourDirection.NORTHWEST:
            self.currentTile = Tile(self.currentTile.coordinates.x - 1, self.currentTile.coordinates.y + 1)
        elif direction == NeighbourDirection.SOUTHWEST:
            self.currentTile = Tile(self.currentTile.coordinates.x - 1, self.currentTile.coordinates.y - 1)
        elif direction == NeighbourDirection.NORTHEAST:
            self.currentTile = Tile(self.currentTile.coordinates.x + 1, self.currentTile.coordinates.y + 1)
        elif direction == NeighbourDirection.SOUTHEAST:
            self.currentTile = Tile(self.currentTile.coordinates.x + 1, self.currentTile.coordinates.y - 1)
        else:
            raise ValueError("Unknown direction to follow.")

        # if direction == NeighbourDirection.WEST:
        #     self.currentTile.coordinates.x -= 1
        # elif direction == NeighbourDirection.EAST:
        #     self.currentTile.coordinates.x += 1
        # elif direction == NeighbourDirection.NORTHWEST:
        #     self.currentTile.coordinates.x -= 1
        #     self.currentTile.coordinates.y += 1
        # elif direction == NeighbourDirection.SOUTHWEST:
        #     self.currentTile.coordinates.x -= 1
        #     self.currentTile.coordinates.y -= 1
        # elif direction == NeighbourDirection.NORTHEAST:
        #     self.currentTile.coordinates.x += 1
        #     self.currentTile.coordinates.y += 1
        # elif direction == NeighbourDirection.SOUTHEAST:
        #     self.currentTile.coordinates.x += 1
        #     self.currentTile.coordinates.y -= 1
        # else:
        #     raise ValueError("Unknown direction to follow.")


    def flipCurrentTile(self):
        if self.currentTile.colour == TileColour.WHITE:
            self.currentTile.colour = TileColour.BLACK
        elif self.currentTile.colour == TileColour.BLACK:
            self.currentTile.colour = TileColour.WHITE
        else:
            raise ValueError("Unkown tile colour: ", self.currentTile.colour)

    def getBlackTilesCount(self):
        tiles = self.coordinatesToTile.values()
        print("coordinatestotilelength: ", len(self.coordinatesToTile))
        cnt = 0
        for tile in tiles:
            if tile.colour == TileColour.BLACK:
                cnt += 1
        return cnt


class Exhibition:
    def __init__(self, lobby: Lobby):
        self.lobby = lobby
        self.currentFloorAlignment = self.lobby.coordinatesToTile
        self.blackTiles = set([tile for tile in self.currentFloorAlignment.values() if tile.colour == TileColour.BLACK])

    def getBlackTilesCount(self):
        return len(self.blackTiles)

    def flipTile(self, tile: Tile, blackNeighboursCount: int):
        if tile.colour == TileColour.WHITE:
            if blackNeighboursCount == 2:
                tile.colour = TileColour.BLACK
        elif tile.colour == TileColour.BLACK:
            if blackNeighboursCount > 2 or blackNeighboursCount == 0:
                tile.colour = TileColour.WHITE

    def getNeighbourTiles(self, tile: Tile):
        neighbourTiles = set()

        neighbourTiles.add(self.retrieveNeighbour(tile, -2, 0))
        neighbourTiles.add(self.retrieveNeighbour(tile, 2, 0))

        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                neighbourTiles.add(self.retrieveNeighbour(tile, i, j))

        assert len(neighbourTiles) == 6
        return neighbourTiles

    def retrieveNeighbour(self, tile, xCoordinateOffset, yCoordinateOffset):
        neighbourCoordinateInDict = (str(tile.coordinates.x + xCoordinateOffset) + "," + str(tile.coordinates.y + yCoordinateOffset))
        if neighbourCoordinateInDict not in self.currentFloorAlignment:
           self.currentFloorAlignment[neighbourCoordinateInDict] = Tile(tile.coordinates.x + xCoordinateOffset, tile.coordinates.y + yCoordinateOffset)

        return self.currentFloorAlignment[neighbourCoordinateInDict]

    def countBlackNeighbours(self, tile):
        return sum([1 for neighbourTile in self.getNeighbourTiles(tile) if neighbourTile in self.blackTiles])


    def iterate(self):
        tilesToVisit = self.findTilesToVisit()
        visitedTiles = set()
        nextBlackTiles = self.blackTiles.copy()

        while len(tilesToVisit) > 0:
            currentTile = tilesToVisit.pop()
            if currentTile in visitedTiles:
                continue

            visitedTiles.add(currentTile)
            currentTileBlackNeighboursCount = self.countBlackNeighbours(currentTile)
            self.flipTile(currentTile, currentTileBlackNeighboursCount)
            self.addBlackTileOrRemoveWhiteTileInBlackTilesCollection(currentTile, nextBlackTiles)

        self.blackTiles = nextBlackTiles

    def addBlackTileOrRemoveWhiteTileInBlackTilesCollection(self, tile, blackTilesCollection: Set[Tile]):
        if tile.colour == TileColour.BLACK:
            blackTilesCollection.add(tile)
        elif tile.colour == TileColour.WHITE and tile in blackTilesCollection:
            blackTilesCollection.remove(tile)

    def findTilesToVisit(self):
        tilesToVisit = set()
        for tile in self.blackTiles:
            tilesToVisit.add(tile)
            neighbourTiles = self.getNeighbourTiles(tile)
            tilesToVisit.update(neighbourTiles)
        return tilesToVisit








def getInput(inputFile: str):
    directionsCollection: List[List[NeighbourDirection]] = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            directions = []
            charPosition = 0
            while charPosition < len(line) - 1:
                if line[charPosition] + line[charPosition + 1] == NeighbourDirection.NORTHEAST.value:
                    directions.append(NeighbourDirection.NORTHEAST)
                    charPosition += 1
                elif line[charPosition] + line[charPosition + 1] == NeighbourDirection.NORTHWEST.value:
                    directions.append(NeighbourDirection.NORTHWEST)
                    charPosition += 1
                elif line[charPosition] + line[charPosition + 1] == NeighbourDirection.SOUTHEAST.value:
                    directions.append(NeighbourDirection.SOUTHEAST)
                    charPosition += 1
                elif line[charPosition] + line[charPosition + 1] == NeighbourDirection.SOUTHWEST.value:
                    directions.append(NeighbourDirection.SOUTHWEST)
                    charPosition += 1
                elif line[charPosition] == NeighbourDirection.EAST.value:
                    directions.append(NeighbourDirection.EAST)
                elif line[charPosition] == NeighbourDirection.WEST.value:
                    directions.append(NeighbourDirection.WEST)
                else:
                    raise ValueError("Unexpected direction when reading input.", line[charPosition])
                charPosition += 1

            if charPosition == len(line) - 1:
                if line[charPosition] == NeighbourDirection.EAST.value:
                    directions.append(NeighbourDirection.EAST)
                elif line[charPosition] == NeighbourDirection.WEST.value:
                    directions.append(NeighbourDirection.WEST)
                else:
                    raise ValueError("Unexpected direction when reading input.", line[charPosition])

            directionsCollection.append(directions)
    return directionsCollection


dirColl = getInput(TEST_INPUT_FILE)   # 396 too high, 371 too low, 380 too high, not 375,but 373

l = Lobby(dirColl)
print("all tiles count: ", len(dirColl))
l.followFlippingDirections()
print("black tiles count: ", l.getBlackTilesCount())

exhibition = Exhibition(l)
#print(exhibition.getBlackTilesCount())
# for k, v in exhibition.currentFloorAlignment.items():
#     print(k, ":", v.colour)


for i in range(10):
    exhibition.iterate()
    print((len(exhibition.blackTiles)))

# exhibition.getNextFloorAlignment()
# print(exhibition.currentFloorAlignment)
# print(exhibition.getBlackTilesCount())
# for k, v in exhibition.currentFloorAlignment.items():
#     print(k, ":", v.colour)

#print(l.repeatedVisitCounter)
#print(len(l.uniqueTiles))

# 3916
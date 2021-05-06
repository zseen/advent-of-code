from typing import List, Set, Dict, Tuple
from enum import Enum
from collections import Counter
from copy import deepcopy

FLOOR_SIZE = 100

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

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
    
class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Tile:
    def __init__(self, coordinateX: int, coordinateY: int):
        self.coordinates: Coordinates = Coordinates(coordinateX, coordinateY)
        self.colour: TileColour = TileColour.WHITE

class Lobby:
    def __init__(self, tileFlippingDirectionsCollection: List[List[NeighbourDirection]]):
        self.tileFlippingDirectionsCollection = tileFlippingDirectionsCollection
        self._coordinatesToTile: Dict[Tuple, Tile] = dict()
        self._currentTile = None

    def getBlackTilesCount(self):
        return sum([1 for tile in self._coordinatesToTile.values() if tile.colour == TileColour.BLACK])
    
    def getCoordinatesToTile(self):
        return self._coordinatesToTile

    def followFlippingDirections(self) -> None:
        for tileFlippingDirections in self.tileFlippingDirectionsCollection:
            self._followFlippingDirection(tileFlippingDirections)

    def _followFlippingDirection(self, tileFlippingDirections: List[NeighbourDirection]):
        self._currentTile = Tile(0, 0)

        for direction in tileFlippingDirections:
            self._moveToTileInDirection(direction)

        self._setCurrentTile()
        self._flipCurrentTile()


    def _moveToTileInDirection(self, direction: NeighbourDirection):
        if direction == NeighbourDirection.WEST:
            self._currentTile = Tile(self._currentTile.coordinates.x - 2, self._currentTile.coordinates.y)
        elif direction == NeighbourDirection.EAST:
            self._currentTile = Tile(self._currentTile.coordinates.x + 2, self._currentTile.coordinates.y)
        elif direction == NeighbourDirection.NORTHWEST:
            self._currentTile = Tile(self._currentTile.coordinates.x - 1, self._currentTile.coordinates.y + 1)
        elif direction == NeighbourDirection.SOUTHWEST:
            self._currentTile = Tile(self._currentTile.coordinates.x - 1, self._currentTile.coordinates.y - 1)
        elif direction == NeighbourDirection.NORTHEAST:
            self._currentTile = Tile(self._currentTile.coordinates.x + 1, self._currentTile.coordinates.y + 1)
        elif direction == NeighbourDirection.SOUTHEAST:
            self._currentTile = Tile(self._currentTile.coordinates.x + 1, self._currentTile.coordinates.y - 1)
        else:
            raise ValueError("Unknown direction to follow.")

    def _setCurrentTile(self) -> None:
        currentTileCoordinates: Tuple[int, int] = (self._currentTile.coordinates.x, self._currentTile.coordinates.y)
        if currentTileCoordinates not in self._coordinatesToTile:
            self._coordinatesToTile[currentTileCoordinates] = self._currentTile
        self._currentTile = self._coordinatesToTile[currentTileCoordinates]


    def _flipCurrentTile(self):
        if self._currentTile.colour == TileColour.WHITE:
            self._currentTile.colour = TileColour.BLACK
        elif self._currentTile.colour == TileColour.BLACK:
            self._currentTile.colour = TileColour.WHITE
        else:
            raise ValueError("Unkown tile colour: ", self._currentTile.colour)


class Exhibition:
    def __init__(self, coordinatesToTile: Dict[Tuple, Tile]):
        self._coordinatesToTile = coordinatesToTile
        self._blackTiles: Set[Tile] = set([tile for tile in self._coordinatesToTile.values() if tile.colour == TileColour.BLACK])

    def getBlackTilesCount(self) -> int:
        return len(self._blackTiles)

    def executeIteration(self) -> None:
        tilesToVisit = self._findTilesToVisit()
        visitedTiles: Set[Tile] = set()
        nextBlackTiles: Set[Tile] = self._blackTiles.copy()

        while len(tilesToVisit) > 0:
            _currentTile = tilesToVisit.pop()
            if _currentTile in visitedTiles:
                continue

            visitedTiles.add(_currentTile)
            currentTileBlackNeighboursCount = self._countBlackNeighbours(_currentTile)
            self._flipTileAccordingToBlackNeighboursCount(_currentTile, currentTileBlackNeighboursCount)
            self._addBlackTileOrRemoveWhiteTileInBlackTilesCollection(_currentTile, nextBlackTiles)

        self._blackTiles = nextBlackTiles

    def _findTilesToVisit(self) -> Set[Tile]:
        tilesToVisit: Set[Tile] = set()
        for tile in self._blackTiles:
            tilesToVisit.add(tile)
            neighbourTiles = self._getNeighbourTiles(tile)
            tilesToVisit.update(neighbourTiles)
        return tilesToVisit

    def _getNeighbourTiles(self, tile: Tile) -> Set[Tile]:
        neighbourTiles: Set[Tile] = set()

        neighbourTiles.add(self._retrieveNeighbour(tile, -2, 0))
        neighbourTiles.add(self._retrieveNeighbour(tile, 2, 0))

        for i in range(-1, 2, 2):
            for j in range(-1, 2, 2):
                neighbourTiles.add(self._retrieveNeighbour(tile, i, j))

        assert len(neighbourTiles) == 6
        return neighbourTiles

    def _retrieveNeighbour(self, tile: Tile, xCoordinateOffset: int, yCoordinateOffset: int) -> Tile:
        coordinatesForNeighbour: Tuple[int, int] = (tile.coordinates.x + xCoordinateOffset, tile.coordinates.y + yCoordinateOffset)
        if coordinatesForNeighbour not in self._coordinatesToTile:
           self._coordinatesToTile[coordinatesForNeighbour] = Tile(coordinatesForNeighbour[0], coordinatesForNeighbour[1])

        return self._coordinatesToTile[coordinatesForNeighbour]

    def _countBlackNeighbours(self, tile: Tile) -> int:
        return sum([1 for neighbourTile in self._getNeighbourTiles(tile) if neighbourTile in self._blackTiles])


    def _flipTileAccordingToBlackNeighboursCount(self, tile: Tile, blackNeighboursCount: int) -> None:
        if tile.colour == TileColour.WHITE:
            if blackNeighboursCount == 2:
                tile.colour = TileColour.BLACK
        elif tile.colour == TileColour.BLACK:
            if blackNeighboursCount > 2 or blackNeighboursCount == 0:
                tile.colour = TileColour.WHITE


    def _addBlackTileOrRemoveWhiteTileInBlackTilesCollection(self, tile: Tile, blackTilesCollection: Set[Tile]) -> None:
        if tile.colour == TileColour.BLACK:
            blackTilesCollection.add(tile)
        elif tile.colour == TileColour.WHITE and tile in blackTilesCollection:
            blackTilesCollection.remove(tile)





def getInput(inputFile: str) -> List[List[NeighbourDirection]]:
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

exhibition = Exhibition(l.getCoordinatesToTile())
#print(exhibition.getBlackTilesCount())
# for k, v in exhibition.currentFloorAlignment.items():
#     print(k, ":", v.colour)


for i in range(10):
    exhibition.executeIteration()
    print(exhibition.getBlackTilesCount())

# exhibition.getNextFloorAlignment()
# print(exhibition.currentFloorAlignment)
# print(exhibition.getBlackTilesCount())
# for k, v in exhibition.currentFloorAlignment.items():
#     print(k, ":", v.colour)

#print(l.repeatedVisitCounter)
#print(len(l.uniqueTiles))

# 3916
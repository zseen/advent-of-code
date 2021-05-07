import unittest
from typing import List, Set, Dict, Tuple
from Direction import Direction
from Tile import Tile
from TileColour import TileColour
from Coordinates import Coordinates
import InputHandler

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

EXECUTION_REPETITION = 100


class Lobby:
    def __init__(self, directionsCollection: List[List[Direction]]):
        self._directionsCollection = directionsCollection
        self._coordinatesToTile: Dict[Tuple, Tile] = dict()
        self._currentTile = None

    def getBlackTilesCount(self) -> int:
        return sum([1 for tile in self._coordinatesToTile.values() if tile.colour == TileColour.BLACK])

    def getCoordinatesToTile(self) -> Dict[Tuple, Tile]:
        return self._coordinatesToTile

    def followAllDirections(self) -> None:
        for directions in self._directionsCollection:
            self._followDirections(directions)

    def _followDirections(self, directions: List[Direction]) -> None:
        self._currentTile = Tile(0, 0)

        for direction in directions:
            self._moveToTileInDirection(direction)

        self._setCurrentTile()
        self._flipCurrentTile()

    def _moveToTileInDirection(self, direction: Direction) -> None:
        if direction == Direction.WEST:
            self._currentTile = Tile(self._currentTile.coordinates.x - 2, self._currentTile.coordinates.y)
        elif direction == Direction.EAST:
            self._currentTile = Tile(self._currentTile.coordinates.x + 2, self._currentTile.coordinates.y)
        elif direction == Direction.NORTHWEST:
            self._currentTile = Tile(self._currentTile.coordinates.x - 1, self._currentTile.coordinates.y + 1)
        elif direction == Direction.SOUTHWEST:
            self._currentTile = Tile(self._currentTile.coordinates.x - 1, self._currentTile.coordinates.y - 1)
        elif direction == Direction.NORTHEAST:
            self._currentTile = Tile(self._currentTile.coordinates.x + 1, self._currentTile.coordinates.y + 1)
        elif direction == Direction.SOUTHEAST:
            self._currentTile = Tile(self._currentTile.coordinates.x + 1, self._currentTile.coordinates.y - 1)
        else:
            raise ValueError("Unknown direction to follow.")

    def _setCurrentTile(self) -> None:
        currentTileCoordinates: Tuple[int, int] = (self._currentTile.coordinates.x, self._currentTile.coordinates.y)
        if currentTileCoordinates not in self._coordinatesToTile:
            self._coordinatesToTile[currentTileCoordinates] = self._currentTile
        self._currentTile = self._coordinatesToTile[currentTileCoordinates]

    def _flipCurrentTile(self) -> None:
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
        else:
            raise ValueError("Unknown tile colour: ", tile.colour)

    def _addBlackTileOrRemoveWhiteTileInBlackTilesCollection(self, tile: Tile, blackTilesCollection: Set[Tile]) -> None:
        if tile.colour == TileColour.BLACK:
            blackTilesCollection.add(tile)
        elif tile.colour == TileColour.WHITE and tile in blackTilesCollection:
            blackTilesCollection.remove(tile)


def main():
    directionsCollection = InputHandler.getInput(INPUT_FILE)
    lobby = Lobby(directionsCollection)
    lobby.followAllDirections()
    print(lobby.getBlackTilesCount())  # 373

    exhibition = Exhibition(lobby.getCoordinatesToTile())
    for _ in range(EXECUTION_REPETITION):
        exhibition.executeIteration()
    print(exhibition.getBlackTilesCount())  # 3917


class LobbyAndExhibitionTester(unittest.TestCase):
    def setUp(self) -> None:
        self.directionsCollection = InputHandler.getInput(TEST_INPUT_FILE)

    def test_getBlackTilesCount_lobby_correctCountReturned(self):
        lobby = Lobby(self.directionsCollection)
        lobby.followAllDirections()
        self.assertEqual(10, lobby.getBlackTilesCount())

    def test_getBlackTilesCount_exhibition_correctCountReturned(self):
        lobby = Lobby(self.directionsCollection)
        lobby.followAllDirections()
        exhibition = Exhibition(lobby.getCoordinatesToTile())
        for _ in range(EXECUTION_REPETITION):
            exhibition.executeIteration()

        self.assertEqual(2208, exhibition.getBlackTilesCount())


if __name__ == '__main__':
    # main()
    unittest.main()

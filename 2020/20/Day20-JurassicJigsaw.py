import unittest
from typing import List

from Tile import Tile
from Puzzle import Puzzle
import PuzzleHelper as PH
from SeaMonster import SeaMonster
from Sea import Sea
from Coordinates import Coordinates
from TileEdgesRemover import TileEdgesRemover


INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
SEA_MONSTER_PIXELS_FILE = "sea_monster.txt"


def createTiles(fileName: str) -> List[Tile]:
    with open(fileName, "r") as inputFile:
        return [createTile(rawTileData) for rawTileData in inputFile.read().split("\n\n")]


def createTile(rawTileData: str) -> Tile:
    if not rawTileData:
        raise ValueError("Invalid data received for creating a tile.")

    rawTileDataSplit = rawTileData.split("\n")

    if not rawTileDataSplit[1] or len(rawTileDataSplit) < 2:
        raise ValueError("Problem with data format after splitting in createTile()")

    rawTileDataSplitForId = rawTileDataSplit[0].strip(":").split(" ")
    if len(rawTileDataSplitForId) < 2 or not rawTileDataSplitForId[1].isnumeric():
        raise ValueError("Tile ID not extracted properly.")

    tileID = rawTileDataSplitForId[1]
    tiles = list(rawTileDataSplit[1:])

    tile = Tile(tileID, tiles)
    tile.setEdges()

    return tile


def createSeaMonster(fileName: str) -> SeaMonster:
    seaMonsterRawInput = getSeaMonsterInput(fileName)
    seaMonster = SeaMonster()
    coordinates = [Coordinates(i, j - 1) for j in range(0, len(seaMonsterRawInput)) for i in range(0, len(seaMonsterRawInput[j])) if seaMonsterRawInput[j][i] == "#"]
    seaMonster.setCoordinates(coordinates)
    return seaMonster


def getSeaMonsterInput(fileName: str) -> List[str]:
    with open(fileName, "r") as inputFile:
        return inputFile.read().split("\n")


def main():
    tiles = createTiles(INPUT_FILE)
    puzzle = Puzzle(tiles)
    puzzle.assemble()
    print(puzzle.getCornerTilesIdsProduct())  # 28057939502729

    edgeRemover = PH.TileEdgesRemover()
    boardWithTileEdgesRemoved = edgeRemover.removeTileEdgesFromCompletedPuzzle(puzzle.getPuzzleBoard())

    seaMonster = createSeaMonster(SEA_MONSTER_PIXELS_FILE)
    sea = Sea(boardWithTileEdgesRemoved, seaMonster)

    print(sea.calculateWaterRoughness())  # 2489


class PuzzleAndSeaTester(unittest.TestCase):
    def setUp(self) -> None:
        self.tiles = createTiles(TEST_INPUT_FILE)
        self.puzzle = Puzzle(self.tiles)

    def setUpSea(self) -> Sea:
        edgeRemover = TileEdgesRemover()
        puzzleBoard = self.puzzle.getPuzzleBoard()
        boardWithTilePixelsFusedTogether = edgeRemover.createBoardWithTilePixelsFusedTogetherInRows(puzzleBoard)
        boardWithTileEdgesRemoved = edgeRemover.removeTileEdgesPixelsFromBoard(boardWithTilePixelsFusedTogether)
        seaMonster = createSeaMonster(SEA_MONSTER_PIXELS_FILE)
        return Sea(boardWithTileEdgesRemoved, seaMonster)

    def test_getCornerTilesIdsProduct_correctProductReturned(self):
        self.puzzle.assemble()
        self.assertEqual(20899048083289, self.puzzle.getCornerTilesIdsProduct())

    def test_calculateWaterRoughness_seaMonstersPresent_correctRoughnessReturned(self):
        self.puzzle.assemble()
        sea = self.setUpSea()
        self.assertEqual(273, sea.calculateWaterRoughness())





if __name__ == '__main__':
    # main()
    unittest.main()

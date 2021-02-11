import unittest
from typing import List

from Tile import Tile
from Puzzle import Puzzle
import PuzzleHelper as PH
from SeaMonster import SeaMonster
from Sea import Sea

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
SEA_MONSTER_PIXELS_FILE = "seaMonster.txt"


def getTiles(fileName: str) -> List[Tile]:
    with open(fileName, "r") as inputFile:
        return [createTile(rawTileData) for rawTileData in inputFile.read().split("\n\n")]


def createTile(rawTileData: str) -> Tile:
    if not rawTileData:
        raise ValueError("Invalid data received for creating a tile.")

    rawTileDataSplit = rawTileData.split()

    if not rawTileDataSplit[1] or not rawTileDataSplit[1][: - 1].isnumeric() or len(rawTileDataSplit) < 3:
        raise ValueError("Problem with data format after splitting in createTile()")

    tileID = rawTileDataSplit[1][:- 1]
    tiles = list(rawTileDataSplit[2:])

    tile = Tile(tileID, tiles)
    tile.setEdges()

    return tile


def createSeaMonster(fileName: str) -> SeaMonster:
    seaMonsterRawInput = getSeaMonsterInput(fileName)
    seaMonster = SeaMonster()
    seaMonster.setCoordinates(seaMonsterRawInput)
    return seaMonster


def getSeaMonsterInput(fileName: str) -> List[str]:
    with open(fileName, "r") as inputFile:
        return inputFile.read().split("\n")


def main():
    tiles = getTiles(INPUT_FILE)
    puzzle = Puzzle(tiles)
    puzzle.putPuzzleTogether()
    print(puzzle.getCornerTilesIdsProduct())  # 28057939502729

    edgeRemover = PH.TileEdgesRemover()
    boardWithTileEdgesRemoved = edgeRemover.removeTileEdgesFromCompletedPuzzle(puzzle.getPuzzleBoard())

    seaMonster = createSeaMonster(SEA_MONSTER_PIXELS_FILE)
    sea = Sea(boardWithTileEdgesRemoved, seaMonster)

    print(sea.calculateWaterRoughness())  # 2489


class PuzzleAndSeaTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PuzzleAndSeaTester, self).__init__(*args, **kwargs)
        self.puzzle = self.getCompletedPuzzle()

    def getCompletedPuzzle(self) -> Puzzle:
        tiles = getTiles(TEST_INPUT_FILE)
        puzzle = Puzzle(tiles)
        puzzle.putPuzzleTogether()
        return puzzle

    def test_getCornerTilesIdsProduct_correctProductReturned(self):
        self.assertEqual(20899048083289, self.puzzle.getCornerTilesIdsProduct())

    def test_calculateWaterRoughness_seaMonstersPresent_correctRoughnessReturned(self):
        edgeRemover = PH.TileEdgesRemover()
        boardWithTileEdgesRemoved = edgeRemover.removeTileEdgesFromCompletedPuzzle(self.puzzle.getPuzzleBoard())
        seaMonster = createSeaMonster(SEA_MONSTER_PIXELS_FILE)
        sea = Sea(boardWithTileEdgesRemoved, seaMonster)
        self.assertEqual(273, sea.calculateWaterRoughness())


if __name__ == '__main__':
    # main()
    unittest.main()

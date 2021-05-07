import unittest
from typing import List
from Tile import Tile
from Puzzle import Puzzle
import PuzzleHelper as PH
from SeaMonster import SeaMonster
from Sea import Sea
from Coordinates import Coordinates
from TileEdgesRemover import TileEdgesRemover
from TileFuser import TileFuser

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
SEA_MONSTER_PIXELS_FILE = "sea_monster.txt"


def getWaterRoughness(puzzle: Puzzle):
    puzzle.assemble()
    seaWater = createSea(puzzle.getPuzzleBoard())
    seaMonster = createSeaMonster(SEA_MONSTER_PIXELS_FILE)
    sea = Sea(seaWater, seaMonster)
    return sea.calculateWaterRoughness()


def createPuzzle(fileName: str) -> Puzzle:
    tiles = createTiles(fileName)
    return Puzzle(tiles)


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
    return Tile(tileID, tiles)


def createSea(puzzleBoard: PH.BoardType) -> List[str]:
    assert puzzleBoard and puzzleBoard[0][0] is not None
    tileEdgeLength = puzzleBoard[0][0].getTileEdgeLength()
    tileFuser = TileFuser(tileEdgeLength)
    boardWithTilePixelsFusedTogether = tileFuser.createBoardWithTilePixelsFusedTogether(puzzleBoard)
    edgeRemover = TileEdgesRemover(tileEdgeLength)
    return edgeRemover.removeTileEdgePixelsFromBoard(boardWithTilePixelsFusedTogether)


def createSeaMonster(fileName: str) -> SeaMonster:
    seaMonsterRawInput = getSeaMonsterInput(fileName)
    coordinates = [Coordinates(i, j) for j in range(0, len(seaMonsterRawInput)) for i in range(0, len(seaMonsterRawInput[j])) if
                   seaMonsterRawInput[j][i] == "#"]
    return SeaMonster(coordinates)


def getSeaMonsterInput(fileName: str) -> List[str]:
    with open(fileName, "r") as inputFile:
        return inputFile.read().split("\n")


def main():
    puzzle = createPuzzle(INPUT_FILE)
    puzzle.assemble()
    print(puzzle.getCornerTilesIdProduct())  # 28057939502729
    print(getWaterRoughness(puzzle))  # 2489


class PuzzleAndSeaTester(unittest.TestCase):
    def test_getCornerTilesIdsProduct_correctProductReturned(self):
        puzzle = createPuzzle(TEST_INPUT_FILE)
        puzzle.assemble()
        self.assertEqual(20899048083289, puzzle.getCornerTilesIdProduct())

    def test_calculateWaterRoughness_seaMonstersPresent_correctRoughnessReturned(self):
        puzzle = createPuzzle(TEST_INPUT_FILE)
        puzzle.assemble()
        self.assertEqual(273, getWaterRoughness(puzzle))


if __name__ == '__main__':
    # main()
    unittest.main()

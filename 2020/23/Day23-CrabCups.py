import unittest
from typing import List, Set, Dict, Optional
from Profiling import doProfiling
from CupCircularLinkedList import CupCircularLinkedList

CupNode = CupCircularLinkedList.CupNode

TEST_INPUT = "test_input.txt"
INPUT_FILE = "input.txt"

CUPS_TO_PICK_OUT_COUNT = 3
ROUNDS_TO_PLAY_PART_ONE = 100
ROUNDS_TO_PLAY_PART_TWO = 10_000_000
CUPS_NUM_PART_TWO = 1_000_000

DO_PROFILING = True


class CrabCups:
    def __init__(self, cups: CupCircularLinkedList):
        self.cups: Cups = cups
        self.currentCup: Optional[CupNode] = None
        self.destinationCup: Optional[CupNode] = None
        self.cupLabelToCup: Dict[int, CupNode] = self.cups.findCupLabelToCup()
        self.maxCupLabel: Optional[int] = len(self.cupLabelToCup)
        self.pickedOutCups: List[CupNode] = []

    def play(self) -> None:
        self._findCurrentCup()
        self._pickOutCupsNextToCurrentCup()
        self._findDestinationCup()
        self._putPickedOutCupsNextToDestinationCup()

    def _findCurrentCup(self) -> None:
        if self.currentCup:
            self.cups.rotate()
        self.currentCup = self.cups.getHeadCup()

    def _pickOutCupsNextToCurrentCup(self) -> None:
        assert self.currentCup
        currentCup = self.currentCup

        for _ in range(0, CUPS_TO_PICK_OUT_COUNT):
            currentCup = self.cups.getNextCupOfCup(currentCup)
            self.pickedOutCups.append(currentCup)
            self.cups.removeCup(currentCup)

    def _findDestinationCup(self) -> None:
        destinationCupLabelCandidate = self.currentCup.label - 1
        pickedOutCupsLabels = set([cup.label for cup in self.pickedOutCups])

        while True:
            if destinationCupLabelCandidate == 0:
                destinationCupLabelCandidate = self.maxCupLabel
            if destinationCupLabelCandidate not in pickedOutCupsLabels:
                self.destinationCup = self.cupLabelToCup[destinationCupLabelCandidate]
                return
            destinationCupLabelCandidate -= 1

    def _putPickedOutCupsNextToDestinationCup(self) -> None:
        assert len(self.pickedOutCups) == CUPS_TO_PICK_OUT_COUNT

        cupToVisitInOriginalCups = self.destinationCup
        for i in range(0, CUPS_TO_PICK_OUT_COUNT):
            cupToVisitInPickedOutCups = self.pickedOutCups.pop(0)
            self.cups.insertCupAfterSpecificCup(cupToVisitInOriginalCups, cupToVisitInPickedOutCups)
            cupToVisitInOriginalCups = self.cups.getNextCupOfCup(cupToVisitInOriginalCups)


def getInput(fileName: str) -> List[int]:
    with open(fileName, "r") as inputFile:
        cupsRawData = inputFile.read()
        return [int(cupLabel) for cupLabel in cupsRawData.strip()]


def setUpAndPlayWholeCrabCupsGame(cupLabels: List[int], roundsToPlay: int) -> CrabCups:
    cups: Cups = createCupsFromLabels(cupLabels)
    crabCups: CrabCups = CrabCups(cups)
    runGame(crabCups, roundsToPlay)
    crabCups.cups.rotateUntilDesiredHeadLabel(1)
    return crabCups


def createCupsFromLabels(cupLabels: List[int]) -> CupCircularLinkedList:
    cupsLinkedList: CupCircularLinkedList = CupCircularLinkedList()
    for label in cupLabels:
        cupsLinkedList.append(CupNode(label))
    return cupsLinkedList


def runGame(crabCups: CrabCups, roundsToPlay: int) -> None:
    for i in range(0, roundsToPlay):
        crabCups.play()


def addMoreCupLabelsUntilLimitInclusive(cupLabels: List[int], limit: int) -> None:
    for i in range(max(cupLabels) + 1, limit + 1):
        cupLabels.append(i)


def playMatchWithExtendedCups(cupLabels: List[int]) -> int:
    addMoreCupLabelsUntilLimitInclusive(cupLabels, CUPS_NUM_PART_TWO)
    crabCupsAfterGame = setUpAndPlayWholeCrabCupsGame(cupLabels, ROUNDS_TO_PLAY_PART_TWO)
    numberOneCupNext = crabCupsAfterGame.cups.getNextCupOfCup(crabCupsAfterGame.cupLabelToCup[1])
    numberOneCupNextNext = crabCupsAfterGame.cups.getNextCupOfCup(numberOneCupNext)
    return numberOneCupNext.label * numberOneCupNextNext.label


def main():
    cupLabels = getInput(INPUT_FILE)

    crabCupsAfterMatch = setUpAndPlayWholeCrabCupsMatch(cupLabels, ROUNDS_TO_PLAY_PART_ONE)
    print("".join(map(str, [cup.label for cup in crabCupsAfterMatch.cups]))[1:])  # "58427369"
    print(playMatchWithExtendedCups(cupLabels))  # 111057672960

    if DO_PROFILING:
        doProfiling(setUpAndPlayWholeCrabCupsGame, cupLabels, ROUNDS_TO_PLAY_PART_TWO)


class CrabCupsTester(unittest.TestCase):
    def setUp(self) -> None:
        self.cupLabels = getInput(TEST_INPUT)

    def test_fewerCupsAndRounds_cupsLabelsAfterCupOneReturned(self):
        crabCupsAfterGame = setUpAndPlayWholeCrabCupsGame(self.cupLabels, ROUNDS_TO_PLAY_PART_ONE)
        self.assertEqual("".join(map(str, [cup.label for cup in crabCupsAfterGame.cups]))[1:], "67384529")

    def test_moreCupsAndRounds_twoCupsLabelsAfterCupOneMultipledTogetherReturned(self):
        self.assertEqual(playMatchWithExtendedCups(self.cupLabels), 149245887792)


if __name__ == '__main__':
    # main()
    unittest.main()

import unittest
from typing import List, Set, Dict, Optional
from copy import deepcopy
from Profiling import doProfiling
from CupNode import CupNode
from CupCircularLinkedList import CupCircularLinkedList

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
        self.cupsLabels: Set[int] = set()
        self.cupLabelToCup: Dict[int, CupNode] = self._getCupLabelsToCup()
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
            currentCup = currentCup.getNextCup()
            self.pickedOutCups.append(currentCup)
            self.cups.removeCup(currentCup)

    def _findDestinationCup(self) -> None:
        destinationCupLabelCandidate = self.currentCup.label - 1
        pickedOutCupsLabels = set([cup.label for cup in self.pickedOutCups])
        while destinationCupLabelCandidate >= 0:
            if (destinationCupLabelCandidate in self.cupsLabels) and (destinationCupLabelCandidate not in pickedOutCupsLabels):
                self.destinationCup = self.cupLabelToCup[destinationCupLabelCandidate]
                break
            destinationCupLabelCandidate -= 1
            if destinationCupLabelCandidate <= 0:
                destinationCupLabelCandidate = len(self.cupsLabels)

        assert self.destinationCup

    def _putPickedOutCupsNextToDestinationCup(self) -> None:
        assert len(self.pickedOutCups) == CUPS_TO_PICK_OUT_COUNT

        cupToVisitInOriginalCups = self.destinationCup
        for i in range(0, CUPS_TO_PICK_OUT_COUNT):
            cupToVisitInPickedOutCups = self.pickedOutCups.pop(0)
            self.cups.insertCupAfterSpecificCup(cupToVisitInOriginalCups, cupToVisitInPickedOutCups)
            cupToVisitInOriginalCups = cupToVisitInOriginalCups.getNextCup()

    def _getCupLabelsToCup(self) -> Dict[int, CupNode]:
        labelToCup: Dict[int, CupNode] = dict()
        for cup in self.cups:
            labelToCup[cup.label] = cup
            self.cupsLabels.add(cup.label)
        return labelToCup


def getInput(fileName: str) -> List[int]:
    with open(fileName, "r") as inputFile:
        cupsRawData = inputFile.read()
        return [int(cupLabel) for cupLabel in cupsRawData.strip()]


def setUpAndPlayWholeCrabCupsMatch(cupLabels: List[int], roundsToPlay: int) -> CrabCups:
    cups: Cups = createCupsFromLabels(cupLabels)
    crabCups: CrabCups = CrabCups(cups)
    runGame(crabCups, roundsToPlay)
    crabCups.cups.rotateUntilDesiredHeadLabel(1)
    return crabCups


def createCupsFromLabels(cupLabels: List[int]) -> CupCircularLinkedList:
    cupsLinkedList: CupCircularLinkedList = CupCircularLinkedList()
    for label in cupLabels:
        cupsLinkedList.addCup(CupNode(label))
    return cupsLinkedList


def runGame(crabCups: CrabCups, roundsToPlay: int) -> None:
    for i in range(0, roundsToPlay):
        crabCups.play()


def addMoreCupLabelsUntilLimitInclusive(cupLabels: List[int], limit: int) -> None:
    for i in range(max(cupLabels) + 1, limit + 1):
        cupLabels.append(i)


def main():
    cupLabels = getInput(INPUT_FILE)

    crabCupsAfterMatch = setUpAndPlayWholeCrabCupsMatch(cupLabels, ROUNDS_TO_PLAY_PART_ONE)
    print("".join(map(str, [cup.label for cup in crabCupsAfterMatch.cups]))[1:])  # "58427369"

    addMoreCupLabelsUntilLimitInclusive(cupLabels, CUPS_NUM_PART_TWO)
    crabCupsAfterMatch = setUpAndPlayWholeCrabCupsMatch(cupLabels, ROUNDS_TO_PLAY_PART_TWO)
    print(
        crabCupsAfterMatch.cupLabelToCup[1].getNextCup().label * crabCupsAfterMatch.cupLabelToCup[1].getNextCup().getNextCup().label)  # 111057672960

    if DO_PROFILING:
        doProfiling(setUpAndPlayWholeCrabCupsMatch, cupLabels, ROUNDS_TO_PLAY_PART_TWO)


class CrabCupsTester(unittest.TestCase):
    def setUp(self) -> None:
        self.cupLabels = getInput(TEST_INPUT)

    def test_fewerCupsAndRounds_cupsLabelsAfterCupOneReturned(self):
        crabCupsAfterMatch = setUpAndPlayWholeCrabCupsMatch(self.cupLabels, ROUNDS_TO_PLAY_PART_ONE)
        self.assertEqual("".join(map(str, [cup.label for cup in crabCupsAfterMatch.cups]))[1:], "67384529")

    def test_moreCupsAndRounds_twoCupsLabelsAfterCupOneMultipledTogetherReturned(self):
        addMoreCupLabelsUntilLimitInclusive(self.cupLabels, CUPS_NUM_PART_TWO)
        crabCupsAfterMatch = setUpAndPlayWholeCrabCupsMatch(self.cupLabels, ROUNDS_TO_PLAY_PART_TWO)
        self.assertEqual(crabCupsAfterMatch.cupLabelToCup[1].getNextCup().label * crabCupsAfterMatch.cupLabelToCup[1].getNextCup().getNextCup().label,
                         149245887792)


if __name__ == '__main__':
    # main()
    unittest.main()

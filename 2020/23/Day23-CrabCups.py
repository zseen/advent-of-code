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

SHOULD_DO_PROFILING = True


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
        currentCup: CupNode = self.currentCup

        for i in range(0, CUPS_TO_PICK_OUT_COUNT):
            currentCup = currentCup.getNextCup()
            self.pickedOutCups.append(currentCup)
            self.cups.removeCup(currentCup)

        #self.currentCup.setNextCup(currentCup.getNextCup())

    def _findDestinationCup(self) -> None:
        nextSmallerCupLabelCandidate = self.currentCup.label - 1
        pickedOutCupsLabels = set([cup.label for cup in self.pickedOutCups])
        while nextSmallerCupLabelCandidate >= 0:
            if (nextSmallerCupLabelCandidate in self.cupsLabels) and (nextSmallerCupLabelCandidate not in pickedOutCupsLabels):
                self.destinationCup = self.cupLabelToCup[nextSmallerCupLabelCandidate]
                break
            nextSmallerCupLabelCandidate -= 1
            if nextSmallerCupLabelCandidate <= 0:
                nextSmallerCupLabelCandidate = len(self.cupsLabels)

        assert self.destinationCup

    def _putPickedOutCupsNextToDestinationCup(self) -> None:
        assert len(self.pickedOutCups) == CUPS_TO_PICK_OUT_COUNT

        cupToVisitInOriginalCups = self.destinationCup
        originalDestinationCupNextCup = self.destinationCup.getNextCup()
        cupToVisitInPickedOutCups: Optional[CupNode] = None

        for i in range(0, CUPS_TO_PICK_OUT_COUNT):
            cupToVisitInPickedOutCups = self.pickedOutCups.pop(0)
            #cupToVisitInOriginalCups.setNextCup(cupToVisitInPickedOutCups)
            self.cups.insertCupAfterSpecificCup(cupToVisitInOriginalCups, cupToVisitInPickedOutCups)
            cupToVisitInOriginalCups = cupToVisitInOriginalCups.getNextCup()

        #cupToVisitInPickedOutCups.setNextCup(originalDestinationCupNextCup)

    def _getCupLabelsToCup(self) -> Dict[int, CupNode]:
        labelToCup: Dict[int, CupNode] = dict()
        cupToVisit: CupNode = self.cups.getHeadCup()
        for cup in self.cups:
            labelToCup[cup.label] = cup
            self.cupsLabels.add(cup.label)
            #cupToVisit = cupToVisit.getNextCup()
        return labelToCup


def getInput(fileName: str) -> List[int]:
    with open(fileName, "r") as inputFile:
        cupsRawData = inputFile.read()
        return [int(cupLabel) for cupLabel in cupsRawData.strip()]


def createCupsFromLabels(cupLabels: List[int]) -> CupCircularLinkedList:
    cups: CupCircularLinkedList = CupCircularLinkedList()
    cupsToAdd: List[CupNode] = [CupNode(label) for label in cupLabels]
    for cup in cupsToAdd:
        cups.addCup(cup)
    return cups


def addMoreCupLabelsUntilLimitInclusive(cupLabels: List[int], limit: int) -> None:
    for i in range(max(cupLabels) + 1, limit + 1):
        cupLabels.append(i)


def runGame(crabCups: CrabCups, roundsToPlay: int) -> None:
    for i in range(0, roundsToPlay):
        crabCups.play()


def main():
    cupLabels = deepcopy(getInput(INPUT_FILE))

    cups: Cups = createCupsFromLabels(cupLabels)
    crabCups: CrabCups = CrabCups(cups)
    runGame(crabCups, ROUNDS_TO_PLAY_PART_ONE)
    crabCups.cups.rotateUntilDesiredHeadLabel(1)
    print("".join(map(str, [cup.getLabel() for cup in crabCups.cups]))[1:]) # "58427369"

    addMoreCupLabelsUntilLimitInclusive(cupLabels, CUPS_NUM_PART_TWO)
    cups: Cups = createCupsFromLabels(cupLabels)
    crabCups: CrabCups = CrabCups(cups)
    runGame(crabCups, ROUNDS_TO_PLAY_PART_TWO)
    crabCups.cups.rotateUntilDesiredHeadLabel(1)
    print(crabCups.cupLabelToCup[1].nextCup.label * crabCups.cupLabelToCup[1].nextCup.nextCup.label) # 111057672960

    if SHOULD_DO_PROFILING:
        doProfiling(runGame, crabCups, ROUNDS_TO_PLAY_PART_TWO)


class CrabCupsTester(unittest.TestCase):
    def setUp(self) -> None:
        self.cupLabels = deepcopy(getInput(TEST_INPUT))

    def test_fewerCupsAndRounds_cupsLabelsAfterCupOneReturned(self):
        cups: Cups = createCupsFromLabels(self.cupLabels)
        crabCups: CrabCups = CrabCups(cups)
        runGame(crabCups, ROUNDS_TO_PLAY_PART_ONE)
        crabCups.cups.rotateUntilDesiredHeadLabel(1)
        self.assertEqual("".join(map(str, crabCups.cups))[1:], "67384529")

    # def test_moreCupsAndRounds_twoCupsLabelsAfterCupOneMultipledTogetherReturned(self):
    #     addMoreCupLabelsUntilLimitInclusive(self.cupLabels, CUPS_NUM_PART_TWO)
    #     cups: Cups = createCupsFromLabels(self.cupLabels)
    #     crabCups: CrabCups = CrabCups(cups)
    #     runGame(crabCups, ROUNDS_TO_PLAY_PART_TWO)
    #     crabCups.cups.rotateUntilDesiredHeadLabel(1)
    #     self.assertEqual(crabCups.cupLabelToCup[1].nextCup.label * crabCups.cupLabelToCup[1].nextCup.nextCup.label, 149245887792)


if __name__ == '__main__':
    #main()
    unittest.main()

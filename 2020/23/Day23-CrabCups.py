import unittest
from typing import List, Set, Dict, Optional
from copy import deepcopy
from Profiling import doProfiling
from Cup import Cup
from Cups import Cups

TEST_INPUT = "test_input.txt"
INPUT_FILE = "input.txt"

CUPS_TO_PICK_OUT_COUNT = 3
ROUNDS_TO_PLAY_PART_ONE = 100
ROUNDS_TO_PLAY_PART_TWO = 10_000_000
CUPS_NUM_IN_PART_TWO = 1_000_000

SHOULD_DO_PROFILING = False


class CrabCups:
    def __init__(self, cups: Cups):
        self.cups: Cups = cups
        self.currentCup: Optional[Cup] = None
        self.destinationCup: Optional[Cup] = None
        self.cupsLabels: Set[int] = set()
        self.cupLabelToCup: Dict[int, Cup] = self._getCupLabelsToCup()
        self.pickedOutCups: List[Cup] = []

    def play(self) -> None:
        self._findCurrentCup()
        self._pickOutCupsNextToCurrentCup()
        self._findDestinationCup()
        self._putPickedOutCupsNextToDestinationCup()

    def _findCurrentCup(self) -> None:
        assert self.cups
        if self.currentCup:
            self.cups.rotate()
        self.currentCup = self.cups.headCup

    def _pickOutCupsNextToCurrentCup(self) -> None:
        assert self.currentCup
        currentCup: Cup = self.currentCup

        for i in range(0, CUPS_TO_PICK_OUT_COUNT):
            currentCup = currentCup.nextCup
            self.pickedOutCups.append(currentCup)
            self.cups.cupsCount -= 1

        self.currentCup.nextCup = currentCup.nextCup

    def _findDestinationCup(self) -> None:
        possibleDestinationCup = self._findSmallerCupThanCurrentCup()
        if possibleDestinationCup is not None:
            self.destinationCup = possibleDestinationCup
        else:
            self.destinationCup = self._findNotPickedOutCupWithGreatestLabel()

        assert self.destinationCup

    def _putPickedOutCupsNextToDestinationCup(self) -> None:
        assert len(self.pickedOutCups) == CUPS_TO_PICK_OUT_COUNT

        cupToVisitInOriginalCups: Cup = self.destinationCup
        originalDestinationCupNextCup: Cup = self.destinationCup.nextCup
        cupToVisitInPickedOutCups: Optional[Cup] = None

        for i in range(0, CUPS_TO_PICK_OUT_COUNT):
            cupToVisitInPickedOutCups = self.pickedOutCups.pop(0)
            cupToVisitInOriginalCups.nextCup = cupToVisitInPickedOutCups
            cupToVisitInOriginalCups = cupToVisitInOriginalCups.nextCup
            self.cups.cupsCount += 1

        cupToVisitInPickedOutCups.nextCup = originalDestinationCupNextCup

    def _getCupLabelsToCup(self) -> Dict[int, Cup]:
        assert self.cups
        labelToCup: Dict[int, Cup] = dict()
        cupToVisit: Cup = self.cups.headCup
        for i in range(0, self.cups.cupsCount):
            labelToCup[cupToVisit.label] = cupToVisit
            self.cupsLabels.add(cupToVisit.label)
            cupToVisit = cupToVisit.nextCup
        return labelToCup

    def _findSmallerCupThanCurrentCup(self) -> Cup:
        nextSmallerCupCandidate = self.currentCup.label - 1
        pickedOutCupsLabels = set([cup.label for cup in self.pickedOutCups])
        while nextSmallerCupCandidate > 0:
            if (nextSmallerCupCandidate in self.cupsLabels) and (nextSmallerCupCandidate not in pickedOutCupsLabels):
                return self.cupLabelToCup[nextSmallerCupCandidate]
            nextSmallerCupCandidate -= 1

    def _findNotPickedOutCupWithGreatestLabel(self) -> Cup:
        for i in range(CUPS_TO_PICK_OUT_COUNT):
            possibleMaxCup = self.cupLabelToCup[len(self.cupsLabels) - i]
            if possibleMaxCup not in self.pickedOutCups:
                return possibleMaxCup


def getInput(fileName: str) -> List[int]:
    with open(fileName, "r") as inputFile:
        cupsRawData = inputFile.read()
        return [int(cupLabel) for cupLabel in cupsRawData.strip()]


def createCupsFromLabels(cupLabels: List[int]) -> Cups:
    cups: Cups = Cups()
    cupsToAdd: List[Cup] = [Cup(label) for label in cupLabels]
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
    print("".join(map(str, crabCups.cups))[1:]) # "58427369"

    addMoreCupLabelsUntilLimitInclusive(cupLabels, CUPS_NUM_IN_PART_TWO)
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

    def test_moreCupsAndRounds_twoCupsLabelsAfterCupOneMultipledTogetherReturned(self):
        addMoreCupLabelsUntilLimitInclusive(self.cupLabels, CUPS_NUM_IN_PART_TWO)
        cups: Cups = createCupsFromLabels(self.cupLabels)
        crabCups: CrabCups = CrabCups(cups)
        runGame(crabCups, ROUNDS_TO_PLAY_PART_TWO)
        crabCups.cups.rotateUntilDesiredHeadLabel(1)
        self.assertEqual(crabCups.cupLabelToCup[1].nextCup.label * crabCups.cupLabelToCup[1].nextCup.nextCup.label, 149245887792)


if __name__ == '__main__':
    # main()
    unittest.main()

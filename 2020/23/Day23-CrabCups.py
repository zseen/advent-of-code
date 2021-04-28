from typing import List, Set, Dict, Optional
from copy import deepcopy

TEST_INPUT = "test_input.txt"
INPUT_FILE = "input.txt"

CUPS_TO_PICK_OUT_COUNT = 3

ROUNDS_TO_PLAY_PART_ONE = 100
ROUNDS_TO_PLAY_PART_TWO = 10_000_000



class Cup:
    def __init__(self, label: int):
        self.label: int = label
        self.nextCup: Optional[Cup] = None

class Cups:
    def __init__(self):
        self.headCup: Optional[Cup] = None
        self.tailCup: Optional[Cup] = None
        self.cupsCount: int = 0

    def addCup(self, cupToAdd: Cup) -> None:
        if not self.headCup:
            self.headCup = cupToAdd
            self.tailCup = cupToAdd
        else:
            self.tailCup.nextCup = cupToAdd
            self.tailCup = cupToAdd
            self.tailCup.nextCup = self.headCup
        self.cupsCount += 1

    def rotate(self) -> None:
        currentHeadCup = self.headCup
        self.headCup = self.headCup.nextCup
        self.tailCup = currentHeadCup

    def __iter__(self) -> None:
        if self.headCup is None:
            return iter(())
        currentCup: Cup = self.headCup
        for i in range(self.cupsCount):
            yield currentCup.label
            currentCup = currentCup.nextCup


    def printCupsLabels(self) -> None:
        currentCup: Cup = self.headCup
        for i in range(0, self.cupsCount):
            print(currentCup.label)
            currentCup = currentCup.nextCup


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

        cupToVisitInOriginalCups:Cup = self.destinationCup
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
    cups = Cups()
    cupsToAdd: List[Cup] = [Cup(label) for label in cupLabels]
    for cup in cupsToAdd:
        cups.addCup(cup)
    return cups


# Part 1

def main():
    cupLabels = deepcopy(getInput(INPUT_FILE))
    cups: Cups = createCupsFromLabels(cupLabels)

    crabCups: CrabCups = CrabCups(cups)
    for i in range(0, ROUNDS_TO_PLAY_PART_ONE):
        crabCups.play()

    while crabCups.cups.headCup.label != 1:
        crabCups.cups.rotate()

    print("Part 1:", "".join(map(str, crabCups.cups))[1:]) #"67384529" for test input, "58427369" for input

if __name__ == '__main__':
    main()


# # Part 2
# for i in range(max(cups) + 1, 1000000 + 1):
#     cups.append(i)
#
# cupsClass = Cups()
#
# cupsToAdd = [Cup(i) for i in cups]
# for cup in cupsToAdd:
#     cupsClass.addCup(cup)
#
# crabCups = CrabCups(cupsClass)
#
#
#
# def runGame():
#     for i in range(0, ROUNDS_TO_PLAY_PART_TWO):
#         crabCups.play()
#
# import cProfile
#
# #cProfile.run('runGame()')
# pr = cProfile.Profile()
# pr.enable()
#
# for i in range(1):
#     pr.run("runGame()")
# pr.disable()
# pr.print_stats(sort='time')
#
#
# #runGame()
#
#
# while crabCups.cups.headCup.label != 1:
#     crabCups.cups.rotate()
#
# print("Part 2:", crabCups.cupsLabelsToNodes[1].nextCup.label * crabCups.cupsLabelsToNodes[1].nextCup.nextCup.label) # 149245887792 for test input, 111057672960 for real input
#
#
#

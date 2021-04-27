from typing import List, Set, Dict
from copy import deepcopy

TEST_INPUT = "test_input.txt"
INPUT_FILE = "input.txt"

CUPS_TO_PICK_OUT_COUNT = 3

ROUNDS_TO_PLAY_PART_ONE = 100
ROUNDS_TO_PLAY_PART_TWO = 10000000 # ten million
# how to break up large numbers


class Cup:
    def __init__(self, label):
        self.label = label
        self.nextCup = None

class Cups:
    def __init__(self):
        self.headCup = None
        self.tailCup = None
        self.cupsCount = 0

    def addCup(self, cupToAdd: Cup):
        if not self.headCup:
            self.headCup = cupToAdd
            self.tailCup = cupToAdd
        else:
            self.tailCup.nextCup = cupToAdd
            self.tailCup = cupToAdd
            self.tailCup.nextCup = self.headCup
        self.cupsCount += 1

    def rotate(self):
        currentHeadCup = self.headCup
        self.headCup = self.headCup.nextCup
        self.tailCup = currentHeadCup

    def __iter__(self):
        if self.headCup is None:
            return iter(())
        curr = self.headCup
        while True:
            yield curr.label
            curr = curr.nextCup
            if curr == self.headCup:
                break


    def printCupsLabels(self):
        assert self.headCup
        currentCup = self.headCup
        for i in range(0, self.cupsCount):
            print(currentCup.label)
            currentCup = currentCup.nextCup


class CrabCups:
    def __init__(self, cups: Cups):
        self.cups: Cups = cups
        self.currentCup = None
        self.destinationCup = None
        self.cupsLabels = set()
        self.cupsLabelsToNodes: Dict[int, Cup] = self.getCupsLabelsToNodes()
        self.pickedOutCups = []

    def getCupsLabelsToNodes(self):
        assert self.cups
        labelsToNodes = dict()
        cupToVisit = self.cups.headCup
        for i in range(0, self.cups.cupsCount):
            labelsToNodes[cupToVisit.label] = cupToVisit
            self.cupsLabels.add(cupToVisit.label)
            cupToVisit = cupToVisit.nextCup
        return labelsToNodes

    def findCurrentCup(self):
        assert self.cups
        self.currentCup = self.cups.headCup

    def pickOutCupsNextToCurrentCup(self):
        assert self.currentCup
        currentCup = self.currentCup
        remainingCupsToPickOutCount = CUPS_TO_PICK_OUT_COUNT

        while remainingCupsToPickOutCount != 0:
            remainingCupsToPickOutCount -= 1
            self.cups.cupsCount -= 1
            currentCup = currentCup.nextCup
            self.pickedOutCups.append(currentCup)

        self.currentCup.nextCup = currentCup.nextCup

    def findDestinationCup(self):
        assert self.cups
        #cupsAsSetWithoutPicketOutCups = self.cupsLabels.difference(set([cup.label for cup in self.pickedOutCups]))

        possibleDestinationCup = self.findSmallerCupThanCurrentCup()#cupsAsSetWithoutPicketOutCups)
        if possibleDestinationCup is not None:
            self.destinationCup = possibleDestinationCup
        else:
            for i in range(CUPS_TO_PICK_OUT_COUNT):
                possibleMaxCup = self.cupsLabelsToNodes[len(self.cupsLabels) - i]
                if possibleMaxCup not in self.pickedOutCups:
                    self.destinationCup = possibleMaxCup
                    break

        assert self.destinationCup


    def findSmallerCupThanCurrentCup(self) -> Cup:
        nextSmallerCupCandidate = self.currentCup.label - 1
        pickedOutCupsLabels = set([cup.label for cup in self.pickedOutCups])
        while nextSmallerCupCandidate > 0:
            if (nextSmallerCupCandidate in self.cupsLabels) and (nextSmallerCupCandidate not in pickedOutCupsLabels):
                return self.cupsLabelsToNodes[nextSmallerCupCandidate]
            nextSmallerCupCandidate -= 1

    def putPickedOutCupsNextToDestinationCup(self) -> None:
        cupToVisitInOriginalCups = self.destinationCup
        destinationCupNextCup = self.destinationCup.nextCup
        cupToVisitInPickedOutCups = None

        for i in range(0, CUPS_TO_PICK_OUT_COUNT):
            cupToVisitInPickedOutCups = self.pickedOutCups[i]
            cupToVisitInOriginalCups.nextCup = cupToVisitInPickedOutCups
            cupToVisitInOriginalCups = cupToVisitInOriginalCups.nextCup

        cupToVisitInPickedOutCups.nextCup = destinationCupNextCup
        self.cups.cupsCount += CUPS_TO_PICK_OUT_COUNT
        self.pickedOutCups = []
        self.cups.rotate()

    def collectLabelsClockwiseAfterLabelOne(self) -> int:
        pass

    def play(self):
        self.findCurrentCup()
        self.pickOutCupsNextToCurrentCup()
        self.findDestinationCup()
        self.putPickedOutCupsNextToDestinationCup()





def getInput(fileName: str) -> List[int]:
    with open(fileName, "r") as inputFile:
        cupsRawData = inputFile.read()
        return [int(cup) for cup in cupsRawData.strip()]




cups = deepcopy(getInput(INPUT_FILE))

# Part 1
cupsClass = Cups()

cupsToAdd = [Cup(i) for i in cups]
for cup in cupsToAdd:
    cupsClass.addCup(cup)

crabCups: CrabCups = CrabCups(cupsClass)
for i in range(0, ROUNDS_TO_PLAY_PART_ONE):

    crabCups.play()
while crabCups.cups.headCup.label != 1:
    crabCups.cups.rotate()

print("Part 1:", "".join(map(str, crabCups.cups))[1:]) #"67384529" for test input, "58427369" for input




# Part 2
for i in range(max(cups) + 1, 1000000 + 1):
    cups.append(i)

cupsClass = Cups()

cupsToAdd = [Cup(i) for i in cups]
for cup in cupsToAdd:
    cupsClass.addCup(cup)

crabCups = CrabCups(cupsClass)



def runGame():
    for i in range(0, ROUNDS_TO_PLAY_PART_TWO):
        crabCups.play()

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


# runGame()
#
#
# while crabCups.cups.headCup.label != 1:
#     crabCups.cups.rotate()
#
# print("Part 2:", crabCups.cupsLabelsToNodes[1].nextCup.label * crabCups.cupsLabelsToNodes[1].nextCup.nextCup.label) # 149245887792 for test input, 111057672960 for real input
#


# cups = getInput(INPUT_FILE)
# crabCups = CrabCups(cups)
# crabCups.play()
# print(crabCups.collectLabelsClockwiseAfterLabelOne())
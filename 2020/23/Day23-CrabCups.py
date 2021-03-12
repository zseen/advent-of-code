from typing import List, Set

TEST_INPUT = "test_input.txt"
INPUT_FILE = "input.txt"

CUPS_TO_PICK_OUT_COUNT = 3
ROUNDS_TO_PLAY = 100

class CrabCups:
    def __init__(self, cups: List[int]):
        self.cups = cups
        self.currentCup = None
        self.destinationCup = None
        self.pickedOutCups = []

    def findCurrentCup(self) -> None:
        if not self.currentCup:
            self.currentCup = self.cups[0]
        else:
            currentCurrentCupIndex = self.cups.index(self.currentCup)
            self.currentCup = self.cups[currentCurrentCupIndex + 1] if currentCurrentCupIndex < len(self.cups) - 1 else self.cups[0]

    def pickOutCupsNextToCurrentCup(self) -> None:
        assert self.currentCup
        currentCupIndex = self.cups.index(self.currentCup)
        cupsNextToCurrentCupFromRightSide = len(self.cups) - currentCupIndex - 1
        cupsFromRightSideToPickCount = CUPS_TO_PICK_OUT_COUNT if cupsNextToCurrentCupFromRightSide >= CUPS_TO_PICK_OUT_COUNT else cupsNextToCurrentCupFromRightSide
        cupsFromLeftSideToPickCount = CUPS_TO_PICK_OUT_COUNT - cupsFromRightSideToPickCount

        self.pickedOutCups = self.cups[currentCupIndex + 1: currentCupIndex + cupsFromRightSideToPickCount + 1]
        del self.cups[currentCupIndex + 1: currentCupIndex + cupsFromRightSideToPickCount + 1]
        self.pickedOutCups.extend(self.cups[0: cupsFromLeftSideToPickCount])
        del self.cups[0: cupsFromLeftSideToPickCount]


    def selectDestinationCup(self) -> None:
        assert self.currentCup
        cupsAsSet = set(self.cups)

        if self.currentCup - 1 in cupsAsSet:
            self.destinationCup = self.currentCup - 1
        elif self.findSmallerCupThanCurrentCup(cupsAsSet) is not None:
            self.destinationCup = self.findSmallerCupThanCurrentCup(cupsAsSet)
        else:
            self.destinationCup = max(self.cups)


    def findSmallerCupThanCurrentCup(self, cupsAsSet: Set[int]) -> int:
        nextSmallerCupCandidate = self.currentCup - 2
        while nextSmallerCupCandidate > 0:
            if nextSmallerCupCandidate in cupsAsSet:
                return nextSmallerCupCandidate
            nextSmallerCupCandidate -= 1


    def putPickedOutCupsNextToDestionationCup(self) -> None:
        destinationCupIndex  = self.cups.index(self.destinationCup)
        for index in range(destinationCupIndex + 1, destinationCupIndex + len(self.pickedOutCups) + 1):
            self.cups.insert(index, self.pickedOutCups.pop(0))

    def collectLabelsClockwiseAfterLabelOne(self) -> int:
        labelOneIndex = self.cups.index(1)
        chunkBeforeOne = self.cups[:labelOneIndex]
        chunkAfterOne = self.cups[labelOneIndex + 1: ]
        return int("".join(str(label) for label in chunkAfterOne) + "".join(str(label) for label in chunkBeforeOne))


    def play(self) -> None:
        for _ in range(ROUNDS_TO_PLAY):
            #print(self.cups)
            self.findCurrentCup()
            #print(self.currentCup)
            self.pickOutCupsNextToCurrentCup()
            #print(self.pickedOutCups)
            self.selectDestinationCup()
            #print(self.destinationCup)
            self.putPickedOutCupsNextToDestionationCup()

            #print("------------")
        print("FINAL CUPS: ", self.cups)



def getInput(fileName: str) -> List[int]:
    with open(fileName, "r") as inputFile:
        cupsRawData = inputFile.read()
        return [int(cup) for cup in cupsRawData.strip()]




cups = getInput(INPUT_FILE)
crabCups = CrabCups(cups)
crabCups.play()
print(crabCups.collectLabelsClockwiseAfterLabelOne())
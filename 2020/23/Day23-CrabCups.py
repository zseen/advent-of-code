from typing import List, Set

TEST_INPUT = "test_input.txt"
INPUT_FILE = "input.txt"

CUPS_TO_PICK_OUT_COUNT = 3
ROUNDS_TO_PLAY = 10000000



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
        self.cups = cups
        self.currentCup = None
        self.destinationCup = None
        self.cupsLabelsToNodes = self.getCupsLabelsToNodes()
        self.pickedOutCups = []


    def getCupsLabelsToNodes(self):
        assert self.cups
        labelsToNodes = dict()
        cupToVisit = self.cups.headCup
        for i in range(0, self.cups.cupsCount):
            labelsToNodes[cupToVisit.label] = cupToVisit
            cupToVisit = cupToVisit.nextCup
        return labelsToNodes

    def findCurrentCup(self):
        assert self.cups
        self.currentCup = self.cups.headCup


            #self.cups.headCup = self.currentCup

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
        cupsAsSetWithoutPicketOutCups = set(self.cupsLabelsToNodes.keys()) - set([cup.label for cup in self.pickedOutCups])

        if self.currentCup.label - 1 in cupsAsSetWithoutPicketOutCups:
            self.destinationCup = self.cupsLabelsToNodes[self.currentCup.label - 1]
        elif self.findSmallerCupThanCurrentCup(cupsAsSetWithoutPicketOutCups) is not None:
            self.destinationCup = self.findSmallerCupThanCurrentCup(cupsAsSetWithoutPicketOutCups)
        else:
            self.destinationCup = self.cupsLabelsToNodes[max(cupsAsSetWithoutPicketOutCups)]

        assert self.destinationCup


    def findSmallerCupThanCurrentCup(self, cupsAsSet: Set[int]) -> Cup:
        nextSmallerCupCandidate = self.currentCup.label - 2
        while nextSmallerCupCandidate > 0:
            if nextSmallerCupCandidate in cupsAsSet:
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










# class CrabCups:
#     def __init__(self, cups: List[int]):
#         self.cups = cups
#         self.currentCup = None
#         self.destinationCup = None
#         self.pickedOutCups = []
#
#     def findCurrentCup(self) -> None:
#         if not self.currentCup:
#             self.currentCup = self.cups[0]
#         else:
#             currentCurrentCupIndex = self.cups.index(self.currentCup)
#             self.currentCup = self.cups[currentCurrentCupIndex + 1] if currentCurrentCupIndex < len(self.cups) - 1 else self.cups[0]
#
#     def pickOutCupsNextToCurrentCup(self) -> None:
#         assert self.currentCup
#         currentCupIndex = self.cups.index(self.currentCup)
#         cupsNextToCurrentCupFromRightSide = len(self.cups) - currentCupIndex - 1
#         cupsFromRightSideToPickCount = CUPS_TO_PICK_OUT_COUNT if cupsNextToCurrentCupFromRightSide >= CUPS_TO_PICK_OUT_COUNT else cupsNextToCurrentCupFromRightSide
#         cupsFromLeftSideToPickCount = CUPS_TO_PICK_OUT_COUNT - cupsFromRightSideToPickCount
#
#         self.pickedOutCups = self.cups[currentCupIndex + 1: currentCupIndex + cupsFromRightSideToPickCount + 1]
#         del self.cups[currentCupIndex + 1: currentCupIndex + cupsFromRightSideToPickCount + 1]
#         self.pickedOutCups.extend(self.cups[0: cupsFromLeftSideToPickCount])
#         del self.cups[0: cupsFromLeftSideToPickCount]
#
#
#     def selectDestinationCup(self) -> None:
#         assert self.currentCup
#         cupsAsSet = set(self.cups)
#
#         if self.currentCup - 1 in cupsAsSet:
#             self.destinationCup = self.currentCup - 1
#         elif self.findSmallerCupThanCurrentCup(cupsAsSet) is not None:
#             self.destinationCup = self.findSmallerCupThanCurrentCup(cupsAsSet)
#         else:
#             self.destinationCup = max(self.cups)
#
#
#     def findSmallerCupThanCurrentCup(self, cupsAsSet: Set[int]) -> int:
#         nextSmallerCupCandidate = self.currentCup - 2
#         while nextSmallerCupCandidate > 0:
#             if nextSmallerCupCandidate in cupsAsSet:
#                 return nextSmallerCupCandidate
#             nextSmallerCupCandidate -= 1
#
#
#     def putPickedOutCupsNextToDestionationCup(self) -> None:
#         destinationCupIndex  = self.cups.index(self.destinationCup)
#         for index in range(destinationCupIndex + 1, destinationCupIndex + len(self.pickedOutCups) + 1):
#             self.cups.insert(index, self.pickedOutCups.pop(0))
#
#     def collectLabelsClockwiseAfterLabelOne(self) -> int:
#         labelOneIndex = self.cups.index(1)
#         chunkBeforeOne = self.cups[:labelOneIndex]
#         chunkAfterOne = self.cups[labelOneIndex + 1: ]
#         return int("".join(str(label) for label in chunkAfterOne) + "".join(str(label) for label in chunkBeforeOne))
#
#
#     def play(self) -> None:
#         for _ in range(ROUNDS_TO_PLAY):
#             #print(self.cups)
#             self.findCurrentCup()
#             #print(self.currentCup)
#             self.pickOutCupsNextToCurrentCup()
#             #print(self.pickedOutCups)
#             self.selectDestinationCup()
#             #print(self.destinationCup)
#             self.putPickedOutCupsNextToDestionationCup()
#
#             #print("------------")
#         print("FINAL CUPS: ", self.cups)



def getInput(fileName: str) -> List[int]:
    with open(fileName, "r") as inputFile:
        cupsRawData = inputFile.read()
        return [int(cup) for cup in cupsRawData.strip()]




cups = getInput(TEST_INPUT)
#print(cups)
print(cups)

for i in range(max(cups) + 1, 1000000 + 1):
    cups.append(i)


cupsClass = Cups()

cupsToAdd = [Cup(i) for i in cups]
for cup in cupsToAdd:
    cupsClass.addCup(cup)

crabCups = CrabCups(cupsClass)


for i in range(0, ROUNDS_TO_PLAY):
    crabCups.play()



while crabCups.cups.headCup.label != 1:
    crabCups.cups.rotate()

print("Part 2:", crabCups.cups[1].nextCup.label * crabCups.cups[1].nextCup.nextCup.label)



# cups = getInput(INPUT_FILE)
# crabCups = CrabCups(cups)
# crabCups.play()
# print(crabCups.collectLabelsClockwiseAfterLabelOne())
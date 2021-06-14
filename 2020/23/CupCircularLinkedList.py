from typing import Optional, Dict


class CupCircularLinkedList:
    def __init__(self) -> None:
        self._headCup: Optional[CupNode] = None
        self._tailCup: Optional[CupNode] = None
        self._cupsCount: int = 0

    class CupNode:
        def __init__(self, label: int) -> None:
            self.label: int = label
            self.nextCup: Optional[CupNode] = None
            self.previousCup: Optional[CupNode] = None

    def getHeadCup(self) -> CupNode:
        return self._headCup

    def getNextCupOfCup(self, cupToGetNextCupOf: CupNode) -> CupNode:
        return cupToGetNextCupOf.nextCup

    def getPreviousCupOfCup(self, cupToGetPreviousCupOf: CupNode) -> CupNode:
        return cupToGetPreviousCupOf.previousCup

    def findCupLabelToCup(self) -> Dict[int, CupNode]:
        labelToCup: Dict[int, CupNode] = dict()
        currentCup = self._headCup
        for _ in range(self._cupsCount):
            labelToCup[currentCup.label] = currentCup
            currentCup = currentCup.nextCup
        return labelToCup

    def __iter__(self) -> CupNode:
        if self._headCup is None:
            return iter(())
        currentCup: CupNode = self._headCup
        for i in range(self._cupsCount):
            yield currentCup
            currentCup = currentCup.nextCup

    def append(self, cupToAdd: CupNode) -> None:
        if not self._headCup:
            self._headCup = cupToAdd
            self._tailCup = cupToAdd
        else:
            self._tailCup.nextCup = cupToAdd
            cupToAdd.previousCup = self._tailCup
            self._tailCup = cupToAdd
            self._tailCup.nextCup = self._headCup
        self._cupsCount += 1

    def removeCup(self, cupToRemove: CupNode) -> None:
        if self._cupsCount == 1:
            self._headCup, self._tailCup = None, None
        else:
            previousCup = cupToRemove.previousCup
            nextCup = cupToRemove.nextCup
            previousCup.nextCup = nextCup
            nextCup.previousCup = previousCup
        self._cupsCount -= 1

    def insertCupAfterSpecificCup(self, cupToInsertAfter: CupNode, cupToInsert: CupNode) -> None:
        currentCupToInsertAfterNextCup = cupToInsertAfter.nextCup
        cupToInsertAfter.nextCup = cupToInsert
        cupToInsert.previousCup = cupToInsertAfter
        currentCupToInsertAfterNextCup.previousCup = cupToInsert
        cupToInsert.nextCup = currentCupToInsertAfterNextCup
        self._cupsCount += 1

    def rotateUntilDesiredHeadLabel(self, desiredHeadLabel: int) -> None:
        for i in range(self._cupsCount):
            if self._headCup.label == desiredHeadLabel:
                return
            self.rotate()
        raise ValueError("No cup found with desired label.")

    def rotate(self) -> None:
        currentHeadCup = self._headCup
        self._headCup = self._headCup.nextCup
        self._tailCup = currentHeadCup

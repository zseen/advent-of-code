from typing import Optional
from CupNode import CupNode


class CupCircularLinkedList:
    def __init__(self):
        self._headCup: Optional[CupNode] = None
        self._tailCup: Optional[CupNode] = None
        self._cupsCount: int = 0


    def getHeadCup(self) -> CupNode:
        return self._headCup

    def getTailCup(self) -> CupNode:
        return self._tailCup

    def getCupsCount(self) -> CupNode:
        return self._cupsCount

    def __iter__(self) -> CupNode:
        if self._headCup is None:
            return iter(())
        currentCup: CupNode = self._headCup
        for i in range(self._cupsCount):
            yield currentCup
            currentCup = currentCup.getNextCup()

    def addCup(self, cupToAdd: CupNode) -> None:
        if not self._headCup:
            self._headCup = cupToAdd
            self._tailCup = cupToAdd
        else:
            self._tailCup.setNextCup(cupToAdd)
            cupToAdd.setPreviousCup(self._tailCup)
            self._tailCup = cupToAdd
            self._tailCup.setNextCup(self._headCup)
        self._cupsCount += 1

    def removeCup(self, cupToRemove: CupNode) -> None:
        previousCup = cupToRemove.getPreviousCup()
        nextCup = cupToRemove.getNextCup()
        previousCup.setNextCup(nextCup)
        nextCup.setPreviousCup(previousCup)
        self._cupsCount -= 1

    def insertCupAfterSpecificCup(self, cupToInsertAfter: CupNode, cupToInsert: CupNode) -> None:
        currentCupToInsertNextCup = cupToInsertAfter.getNextCup()

        cupToInsertAfter.setNextCup(cupToInsert)
        cupToInsert.setPreviousCup(cupToInsertAfter)
        currentCupToInsertNextCup.setPreviousCup(cupToInsert)
        cupToInsert.setNextCup(currentCupToInsertNextCup)
        self._cupsCount += 1


    def rotateUntilDesiredHeadLabel(self, desiredHeadLabel: int) -> None:
        for i in range(self._cupsCount):
            if self._headCup.label == desiredHeadLabel:
                return
            self.rotate()
        raise ValueError("No cup found with desired label.")

    def rotate(self) -> None:
        currentHeadCup = self._headCup
        self._headCup = self._headCup.getNextCup()
        self._tailCup = currentHeadCup

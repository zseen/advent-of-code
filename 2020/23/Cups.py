from typing import Optional
from Cup import Cup


class Cups:
    def __init__(self):
        self.headCup: Optional[Cup] = None
        self.tailCup: Optional[Cup] = None
        self.cupsCount: int = 0

    def __iter__(self) -> None:
        if self.headCup is None:
            return iter(())
        currentCup: Cup = self.headCup
        for i in range(self.cupsCount):
            yield currentCup.label
            currentCup = currentCup.nextCup

    def addCup(self, cupToAdd: Cup) -> None:
        if not self.headCup:
            self.headCup = cupToAdd
            self.tailCup = cupToAdd
        else:
            self.tailCup.nextCup = cupToAdd
            self.tailCup = cupToAdd
            self.tailCup.nextCup = self.headCup
        self.cupsCount += 1

    def rotateUntilDesiredHeadLabel(self, desiredHeadLabel: int) -> None:
        for i in range(self.cupsCount):
            if self.headCup.label == desiredHeadLabel:
                return
            self.rotate()
        raise ValueError("No cup found with desired label.")

    def rotate(self) -> None:
        currentHeadCup = self.headCup
        self.headCup = self.headCup.nextCup
        self.tailCup = currentHeadCup

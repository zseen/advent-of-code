from typing import Optional


class CupNode:
    def __init__(self, label: int):
        self.label: int = label
        self._nextCup: Optional[CupNode] = None
        self._previousCup: Optional[CupNode] = None

    def getNextCup(self) -> ["CupNode"]:
        return self._nextCup

    def setNextCup(self, nextCup: ["CupNode"]) -> None:
        self._nextCup = nextCup

    def getPreviousCup(self) -> ["CupNode"]:
        return self._previousCup

    def setPreviousCup(self, previousCup: ["CupNode"]) -> None:
        self._previousCup = previousCup



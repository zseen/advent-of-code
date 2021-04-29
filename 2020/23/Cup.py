from typing import Optional


class Cup:
    def __init__(self, label: int):
        self.label: int = label
        self.nextCup: Optional[Cup] = None

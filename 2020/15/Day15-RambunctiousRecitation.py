import unittest
from typing import List
from copy import deepcopy

INPUT = [1, 20, 8, 12, 0, 14]
TEST_INPUT = [0, 3, 6]

UPPER_BOUND_FIRST_PART = 2020
UPPER_BOUND_SECOND_PART = 30000000


def getNthNum(initialNums: List[int], upperBound: int):
    if not initialNums:
        raise ValueError("No initial nums received")

    numsSaid = deepcopy(initialNums)
    numToTurnLastSaid = dict()
    for i in range(len(initialNums)):
        numToTurnLastSaid[numsSaid[i]] = i + 1

    for turnNum in range(len(numsSaid), upperBound):
        lastSaidNum = numsSaid[-1]
        if lastSaidNum not in numToTurnLastSaid:
            numsSaid.append(0)
        else:
            lastTurnNumWasSaid = numToTurnLastSaid[lastSaidNum]
            numsSaid.append(turnNum - lastTurnNumWasSaid)
        numToTurnLastSaid[lastSaidNum] = turnNum

    return numsSaid[-1]


def main():
    print(getNthNum(INPUT, UPPER_BOUND_FIRST_PART))  # 492

    print(getNthNum(INPUT, UPPER_BOUND_SECOND_PART))  # 63644


class NumGameTester(unittest.TestCase):
    def test_getNthNum_smallerUpperBound_correctNumReturned(self):
        self.assertEqual(436, getNthNum(TEST_INPUT, UPPER_BOUND_FIRST_PART))

    def test_getNthNum_largerUpperBound_correctNumReturned(self):
        self.assertEqual(175594, getNthNum(TEST_INPUT, UPPER_BOUND_SECOND_PART))


if __name__ == '__main__':
    # main()
    unittest.main()

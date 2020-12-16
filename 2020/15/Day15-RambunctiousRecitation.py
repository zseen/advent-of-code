import unittest
from typing import List
from copy import deepcopy

INPUT = [1, 20, 8, 12, 0, 14]
TEST_INPUT = [0, 3, 6]

UPPER_RANGE_FIRST_PART = 2020
UPPER_RANGE_SECOND_PART = 30000000


def getUpperRangethNum(initialNums: List[int], upperRange: int):
    numsSaid = deepcopy(initialNums)
    numsToTurnLastSaid = dict()
    for i in range(len(numsSaid)):
        numsToTurnLastSaid[numsSaid[i]] = i + 1

    for turnNum in range(len(numsSaid), upperRange):
        lastSaidNum = numsSaid[-1]
        if lastSaidNum not in numsToTurnLastSaid:
            numsSaid.append(0)
        else:
            lastTurnNumWasSaid = numsToTurnLastSaid[lastSaidNum]
            numsSaid.append(turnNum - lastTurnNumWasSaid)
        numsToTurnLastSaid[lastSaidNum] = turnNum

    return numsSaid[-1]


def main():
    print(getUpperRangethNum(INPUT, UPPER_RANGE_FIRST_PART))  # 492

    print(getUpperRangethNum(INPUT, UPPER_RANGE_SECOND_PART))  # 63644


class NumGameTester(unittest.TestCase):
    def test_getUpperRangethNum_smallerRange_correctNumReturned(self):
        self.assertEqual(436, getUpperRangethNum(TEST_INPUT, UPPER_RANGE_FIRST_PART))

    def test_getUpperRangethNum_largerRange_correctNumReturned(self):
        self.assertEqual(175594, getUpperRangethNum(TEST_INPUT, UPPER_RANGE_SECOND_PART))


if __name__ == '__main__':
    # main()
    unittest.main()

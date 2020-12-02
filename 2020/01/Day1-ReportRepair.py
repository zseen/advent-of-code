import unittest

INPUT_FILE = "input.txt"


def getInputNums():
    inputNums = []
    with open(INPUT_FILE, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            inputNums.append(int(line))
    return inputNums


def getNumPairAddingUpTo2020(inputNums):
    allNums = set(inputNums)
    visitedNums = set()

    for num in allNums:
        if 2020 - num in visitedNums:
            return (num, 2020 - num)
        visitedNums.add(num)

    return None


def getProductOfPairAddingUpTo2020(inputNums):
    pair = getNumPairAddingUpTo2020(inputNums)
    if not pair or len(pair) < 2:
        raise ValueError("Pair not found")
    return pair[0] * pair[1]


def getThreeNumsAddingUpTo2020(inputNums):
    for i in range(0, len(inputNums)):
        for j in range(i + 1, len(inputNums)):
            if inputNums[i] + inputNums[j] >= 2020:
                continue
            for k in range(j + 1, len(inputNums)):
                if inputNums[k] == 2020 - (inputNums[j] + inputNums[i]):
                    return (inputNums[i], inputNums[j], inputNums[k])
    return None


def getProductOfThreeNumsAddingUpTo2020(inputNums):
    nums = getThreeNumsAddingUpTo2020(inputNums)
    if not nums or len(nums) != 3:
        raise ValueError("No such three numbers found")

    return nums[0] * nums[1] * nums[2]


class ProductTester(unittest.TestCase):
    def test_getNumPairAddingUpTo2020_twoDifferentNumsInListAddUp_numsFound(self):
        numsAddingUpTo2020 = getNumPairAddingUpTo2020([1721, 979, 366, 299, 675, 1456])

        self.assertEquals(1721 in numsAddingUpTo2020, True)
        self.assertEquals(299 in numsAddingUpTo2020, True)

    def test_getProductOfPairAddingUpTo2020_numsListGiven_twoNumFoundAndProductCalculated(self):
        product = getProductOfPairAddingUpTo2020([1721, 979, 366, 299, 675, 1456])
        self.assertEqual(514579, product)

    def test_getThreeNumsAddingUpTo2020_threeDifferentNumsInListAddUp_threeNumsFound(self):
        numsAddingUpTo2020 = getThreeNumsAddingUpTo2020([1721, 979, 366, 299, 675, 1456])
        self.assertEquals(979 in numsAddingUpTo2020, True)
        self.assertEquals(366 in numsAddingUpTo2020, True)
        self.assertEquals(675 in numsAddingUpTo2020, True)

    def test_getProductOfThreeNumsAddingUpTo2020_numsListGiven_threeNumsFoundAndProductCalculated(self):
        product = getProductOfThreeNumsAddingUpTo2020([1721, 979, 366, 299, 675, 1456])
        self.assertEqual(241861950, product)


def main():
    inputNums = getInputNums()
    print(getProductOfPairAddingUpTo2020(inputNums))  # 692916 (1582 * 438)
    print(getProductOfThreeNumsAddingUpTo2020(inputNums))  # 289270976 (688 * 514 * 818)


if __name__ == '__main__':
    main()
    # unittest.main()

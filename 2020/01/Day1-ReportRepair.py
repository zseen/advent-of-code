INPUT_FILE = "input.txt"
inputNums = []

def getInputNums():
    with open(INPUT_FILE, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            inputNums.append(int(line))


def getNumPairAddingUpTo2020():
    allNums = set(inputNums)
    visitedNums = set()

    for num in allNums:
        if 2020 - num in allNums and num not in visitedNums:
            return (num, 2020 - num)
        visitedNums.add(num)


def getProductOfPairAddingUpTo2020():
    pair = getNumPairAddingUpTo2020()
    if not pair or len(pair) < 2:
        raise ValueError("Pair not found")
    return pair[0] * pair[1]


def getThreeNumsAddingUpTo2020():
    for i in range(0, len(inputNums)):
        for j in range(i+1, len(inputNums)):
            if inputNums[i] + inputNums[j] >= 2020:
                continue
            for k in range(j+1, len(inputNums)):
                if inputNums[k] == 2020 - (inputNums[j] + inputNums[i]):
                    return (inputNums[i], inputNums[j], inputNums[k])

def getProductOfThreeNumsAddingUpTo2020():
    nums = getThreeNumsAddingUpTo2020()
    if not nums or len(nums) != 3:
        raise ValueError("No such three numbers found")

    return nums[0] * nums[1] * nums[2]




def main():
    getInputNums()
    print(getProductOfPairAddingUpTo2020()) # 692916 (1582 * 438)
    print(getProductOfThreeNumsAddingUpTo2020()) # 289270976 (688 * 514 * 818)


if __name__ == '__main__':
    main()


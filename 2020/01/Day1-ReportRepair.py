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



def main():
    getInputNums()
    print(getProductOfPairAddingUpTo2020()) # 692916 (1582 * 438)

if __name__ == '__main__':
    main()


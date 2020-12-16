import unittest

INPUT = [1,20,8,12,0,14]
TEST_INPUT = [0, 3, 6]

UPPER_RANGE_FIRST_PART = 2020
UPPER_RANGE_SECOND_PART = 30000000


def play(inputArray, upperRange):
    numsToSay = inputArray
    numsToTurn = dict()
    for i in range(len(inputArray)):
        numsToTurn[inputArray[i]] = i + 1

    for i in range(len(inputArray)+1, upperRange + 1):
        lastSaidNum = numsToSay[-1]
        if lastSaidNum not in numsToTurn:
            numsToSay.append(0)
        else:
            lastTurnNumWasSaid = numsToTurn[lastSaidNum]
            numsToSay.append(i - 1 - lastTurnNumWasSaid)

        numsToTurn[lastSaidNum] = i - 1


    return numsToSay


#numsTest1 = play(TEST_INPUT, UPPER_RANGE_FIRST_PART)
#print(numsTest1[-1])
#
# numsTest2 = play([1,3,2], UPPER_RANGE_FIRST_PART)
# print(numsTest2[-1])
#
# numsTest3 = play([2,1,3], UPPER_RANGE_FIRST_PART)
# print(numsTest3[-1])
#
# numsTest4 = play([2,3,1], UPPER_RANGE_FIRST_PART)
# print(numsTest4[-1])
#
# numsTest5 = play([3,2,1], UPPER_RANGE_FIRST_PART)
# print(numsTest5[-1])
#
# numsTest6 = play([3,1,2], UPPER_RANGE_FIRST_PART)
# print(numsTest6[-1])





print("--------------------------------")
numsMainRun = play(INPUT, UPPER_RANGE_FIRST_PART)
print(numsMainRun[-1])
print("--------------------------------")

# numsTest1 = play(TEST_INPUT, UPPER_RANGE_SECOND_PART)
# print(numsTest1[-1])
#
# numsTest2 = play([1,3,2], UPPER_RANGE_SECOND_PART)
# print(numsTest2[-1])
#
# numsTest3 = play([2,1,3], UPPER_RANGE_SECOND_PART)
# print(numsTest3[-1])
#
# numsTest4 = play([2,3,1], UPPER_RANGE_SECOND_PART)
# print(numsTest4[-1])
#
# numsTest5 = play([3,2,1], UPPER_RANGE_SECOND_PART)
# print(numsTest5[-1])
#
# numsTest6 = play([3,1,2], UPPER_RANGE_SECOND_PART)
# print(numsTest6[-1])



numsMainRun = play(INPUT, UPPER_RANGE_SECOND_PART)
print(numsMainRun[-1])
import unittest

INPUT = [1,20,8,12,0,14]
TEST_INPUT = [0, 3, 6]



def play(inputArray):
    numsToSay = inputArray
    numsToTurn = dict()
    for i in range(len(inputArray)):
        numsToTurn[inputArray[i]] = i + 1

    for i in range(len(inputArray)+1, 2021):
        lastSaidNum = numsToSay[-1]
        if numsToSay.count(lastSaidNum) == 1:
            numsToSay.append(0)
        else:
            lastTurnNumWasSaid = numsToTurn[lastSaidNum]
            numsToSay.append(i - 1 - lastTurnNumWasSaid)

        numsToTurn[lastSaidNum] = i - 1


    return numsToSay


numsTest1 = play(TEST_INPUT)
print(numsTest1[-1])

numsTest2 = play([1,3,2])
print(numsTest2[-1])

numsTest3 = play([2,1,3])
print(numsTest3[-1])

numsTest4 = play([2,3,1])
print(numsTest4[-1])

numsTest5 = play([3,2,1])
print(numsTest5[-1])

numsTest6 = play([3,1,2])
print(numsTest6[-1])

print("--------------------------------")
numsMainRun = play(INPUT)
print(numsMainRun[-1])





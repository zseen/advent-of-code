import unittest
from typing import List, Tuple

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

NUM_TO_DIVIDE_BY = 20201227
SUBJECT_NUMBER = 7

class ComboBreaker:
    def __init__(self, publicKey: int) -> None:
        self.publicKey = publicKey
        self.loopSize = self.calculateLoopSize()
        self.encryptionKey = None

    def calculateLoopSize(self):
        value = 1
        loopSize = 1
        while True:
            value *= SUBJECT_NUMBER
            value %= NUM_TO_DIVIDE_BY

            if value == self.publicKey:
                return loopSize

            loopSize += 1


    def calculateEncryptionKey(self, otherDeviceLoopSize):
        self.encryptionKey =  self.transformNumber( otherDeviceLoopSize)



    def transformNumber(self,  timesToTransform):
        value = 1
        for _ in range(timesToTransform):
            value *= self.publicKey
            value %= NUM_TO_DIVIDE_BY
        return value



class Card(ComboBreaker):
    pass

class Door(ComboBreaker):
    pass



def getInput(inputFile: str) -> Tuple[int, int]:
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        assert len(lines) == 2
        return int(lines[0].strip()), int(lines[1].strip())



cardPublicKey, doorPublicKey = getInput(INPUT_FILE)
card = Card(cardPublicKey)
door = Door(doorPublicKey)

print(card.publicKey, card.loopSize)
print(door.publicKey, door.loopSize)

card.calculateEncryptionKey(door.loopSize)
print(card.encryptionKey)
door.calculateEncryptionKey(card.loopSize)
print(door.encryptionKey)




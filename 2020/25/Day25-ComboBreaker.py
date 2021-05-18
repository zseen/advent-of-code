import unittest
from typing import Tuple, Optional

INPUT_FILE = "input.txt"
TEST_INPUT = "test_input.txt"

NUM_TO_DIVIDE_BY = 20201227
SUBJECT_NUMBER = 7


class DeviceEncrypter:
    def __init__(self, publicKey: int) -> None:
        self._publicKey = publicKey
        self._loopSize = self.calculateLoopSize()
        self._encryptionKey: Optional[int] = None

    def getPublicKey(self) -> int:
        return self._publicKey

    def getLoopSize(self) -> int:
        return self._loopSize

    def getEncryptionKey(self) -> int:
        if self._encryptionKey is None:
            raise ValueError("Encryption key not determined yet.")

        return self._encryptionKey

    def calculateLoopSize(self) -> int:
        transformedNumber = 1
        loopSize = 1
        while True:
            transformedNumber = self._transformNumber(transformedNumber, SUBJECT_NUMBER)
            if transformedNumber == self._publicKey:
                return loopSize
            loopSize += 1

    def calculateEncryptionKey(self, otherDeviceLoopSize: int) -> None:
        self._encryptionKey = self._generateTransformedNumberNtimes(otherDeviceLoopSize)

    def _generateTransformedNumberNtimes(self, loopSize: int) -> int:
        transformedNumber = 1
        for _ in range(loopSize):
            transformedNumber = self._transformNumber(transformedNumber, self._publicKey)
        return transformedNumber

    def _transformNumber(self, numToTransform: int, subjectNumber: int) -> int:
        numToTransform *= subjectNumber
        numToTransform %= NUM_TO_DIVIDE_BY
        return numToTransform


def getInput(inputFile: str) -> Tuple[int, int]:
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        assert len(lines) == 2
        return int(lines[0].strip()), int(lines[1].strip())


def main():
    cardPublicKey, doorPublicKey = getInput(INPUT_FILE)
    card = DeviceEncrypter(cardPublicKey)
    door = DeviceEncrypter(doorPublicKey)

    print(card.getLoopSize())  # 397860
    print(door.getLoopSize())  # 16774995

    card.calculateEncryptionKey(door.getLoopSize())
    print(card.getEncryptionKey())  # 16311885 (equal to the door's encryption key)
    door.calculateEncryptionKey(card.getLoopSize())
    print(door.getEncryptionKey())  # 16311885 (equal to the card's encryption key)


class ComboBreakerTester(unittest.TestCase):
    def setUp(self) -> None:
        cardPublicKey, doorPublicKey = getInput(TEST_INPUT)
        self.card = DeviceEncrypter(cardPublicKey)
        self.door = DeviceEncrypter(doorPublicKey)

    def test_calculateLoopSize_forCardAndDoor_calculationCorrect(self):
        self.assertEqual(8, self.card.getLoopSize())
        self.assertEqual(11, self.door.getLoopSize())

    def test_calculateEncryptionKey_forCarAndDoor_equalAndCorrectResultReturned(self):
        self.card.calculateEncryptionKey(self.door.getLoopSize())
        self.door.calculateEncryptionKey(self.card.getLoopSize())
        self.assertEqual(self.card.getEncryptionKey(), self.door.getEncryptionKey())
        self.assertEqual(14897079, self.card.getEncryptionKey())


if __name__ == '__main__':
    # main()
    unittest.main()

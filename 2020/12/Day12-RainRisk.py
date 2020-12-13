import unittest
from typing import List
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"


class Compass(Enum):
    NORTH = "N"
    WEST = "W"
    EAST = "E"
    SOUTH = "S"


class Direction(Enum):
    RIGHT = "R"
    LEFT = "L"


class Move(Enum):
    FORWARD = "F"


class Instruction:
    def __init__(self, action: str, value: int):
        self.action = action
        self.value = value


class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class FerryMover:
    def __init__(self, wayPoint: Coordinate, instructions: List[Instruction]):
        self.position: Coordinate = Coordinate(0, 0)
        self.wayPoint = wayPoint
        self.instructions = instructions

    def followInstructions(self):
        for instruction in self.instructions:
            self.followInstruction(instruction)

    def followInstruction(self, instruction: Instruction):
        if instruction.action in [compass.value for compass in Compass]:
            self.handleCompass(instruction)
        elif instruction.action == Direction.RIGHT.value:
            for i in range(0, instruction.value // 90):
                self.turnRight()
        elif instruction.action == Direction.LEFT.value:
            for i in range(0, instruction.value // 90):
                self.turnLeft()
        elif instruction.action == Move.FORWARD.value:
            self.moveForward(instruction.value)
        else:
            raise ValueError("Unknown instruction received.")

    def handleCompass(self, instruction: Instruction):
        if instruction.action == Compass.NORTH.value:
            self.position.y += instruction.value
        elif instruction.action == Compass.SOUTH.value:
            self.position.y -= instruction.value
        elif instruction.action == Compass.WEST.value:
            self.position.x -= instruction.value
        elif instruction.action == Compass.EAST.value:
            self.position.x += instruction.value

    def turnRight(self):
        self.wayPoint.x, self.wayPoint.y = self.wayPoint.y, self.wayPoint.x * -1

    def turnLeft(self):
        for i in range(0, 3):
            self.turnRight()

    def moveForward(self, value: int):
        self.position.x += self.wayPoint.x * value
        self.position.y += self.wayPoint.y * value

    def getManhattanDistanceFromOrigin(self):
        return abs(self.position.x) + abs(self.position.y)


class FerryMoverWithRelativeWayPoint(FerryMover):
    def handleCompass(self, instruction: Instruction):
        if instruction.action == Compass.NORTH.value:
            self.wayPoint.y += instruction.value
        elif instruction.action == Compass.SOUTH.value:
            self.wayPoint.y -= instruction.value
        elif instruction.action == Compass.WEST.value:
            self.wayPoint.x -= instruction.value
        elif instruction.action == Compass.EAST.value:
            self.wayPoint.x += instruction.value


def getInstructions(inputFile: str):
    instructions = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            instructions.append(Instruction(line[0], int(line[1:])))
    return instructions


def main():
    instructions = getInstructions(INPUT_FILE)

    ferryMover = FerryMover(Coordinate(1, 0), instructions)
    ferryMover.followInstructions()
    print(ferryMover.getManhattanDistanceFromOrigin())  # 1010

    ferryMoverWithRelativeWayPoint = FerryMoverWithRelativeWayPoint(Coordinate(10, 1), instructions)
    ferryMoverWithRelativeWayPoint.followInstructions()
    print(ferryMoverWithRelativeWayPoint.getManhattanDistanceFromOrigin())  # 52742


class FerryMoversTester(unittest.TestCase):
    def test_getManhattanDistance_setWayPoint_correctDistanceReturned(self):
        instructions = getInstructions(TEST_INPUT_FILE)
        ferryMover = FerryMover(Coordinate(1, 0), instructions)
        ferryMover.followInstructions()
        self.assertEqual(25, ferryMover.getManhattanDistanceFromOrigin())

    def test_getManhattanDistance_relativeWaypoint_correctDistanceReturned(self):
        instructions = getInstructions(TEST_INPUT_FILE)
        ferryMoverWithRelativeWayPoint = FerryMoverWithRelativeWayPoint(Coordinate(10, 1), instructions)
        ferryMoverWithRelativeWayPoint.followInstructions()
        self.assertEqual(286, ferryMoverWithRelativeWayPoint.getManhattanDistanceFromOrigin())


if __name__ == '__main__':
    # main()
    unittest.main()

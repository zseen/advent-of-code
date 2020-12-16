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


class Coordinates:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

COORDINATES_FOR_PART_ONE = Coordinates(1, 0)
COORDINATES_FOR_PART_TWO = Coordinates(10, 1)


class FerryMover:
    def __init__(self, waypoint: Coordinates, instructions: List[Instruction]):
        self.position: Coordinates = Coordinates(0, 0)
        self.waypoint = waypoint
        self.instructions = instructions

    def followInstructions(self):
        for instruction in self.instructions:
            self.followInstruction(instruction)

    def followInstruction(self, instruction: Instruction):
        if instruction.action in [compass.value for compass in Compass]:
            self.handleCompass(instruction)
        elif instruction.action == Direction.RIGHT.value:
            self.turnRight(instruction.value)
        elif instruction.action == Direction.LEFT.value:
            self.turnLeft(instruction.value)
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

    def turnRight(self, degree):
        for i in range(0, degree // 90):
            self.waypoint.x, self.waypoint.y = self.waypoint.y, self.waypoint.x * -1

    def turnLeft(self, degree):
        for i in range(0, 3):
            self.turnRight(degree)

    def moveForward(self, value: int):
        self.position.x += self.waypoint.x * value
        self.position.y += self.waypoint.y * value

    def getManhattanDistanceFromOrigin(self):
        return abs(self.position.x) + abs(self.position.y)


class FerryMoverWithRelativeWaypoint(FerryMover):
    def handleCompass(self, instruction: Instruction):
        if instruction.action == Compass.NORTH.value:
            self.waypoint.y += instruction.value
        elif instruction.action == Compass.SOUTH.value:
            self.waypoint.y -= instruction.value
        elif instruction.action == Compass.WEST.value:
            self.waypoint.x -= instruction.value
        elif instruction.action == Compass.EAST.value:
            self.waypoint.x += instruction.value


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

    ferryMover = FerryMover(COORDINATES_FOR_PART_ONE, instructions)
    ferryMover.followInstructions()
    print(ferryMover.getManhattanDistanceFromOrigin())  # 1010

    ferryMoverWithRelativeWaypoint = FerryMoverWithRelativeWaypoint(COORDINATES_FOR_PART_TWO, instructions)
    ferryMoverWithRelativeWaypoint.followInstructions()
    print(ferryMoverWithRelativeWaypoint.getManhattanDistanceFromOrigin())  # 52742


class FerryMoversTester(unittest.TestCase):
    def test_getManhattanDistance_setWaypoint_correctDistanceReturned(self):
        instructions = getInstructions(TEST_INPUT_FILE)
        ferryMover = FerryMover(COORDINATES_FOR_PART_ONE, instructions)
        ferryMover.followInstructions()
        self.assertEqual(25, ferryMover.getManhattanDistanceFromOrigin())

    def test_getManhattanDistance_relativeWaypoint_correctDistanceReturned(self):
        instructions = getInstructions(TEST_INPUT_FILE)
        ferryMoverWithRelativeWaypoint = FerryMoverWithRelativeWaypoint(COORDINATES_FOR_PART_TWO, instructions)
        ferryMoverWithRelativeWaypoint.followInstructions()
        self.assertEqual(286, ferryMoverWithRelativeWaypoint.getManhattanDistanceFromOrigin())


if __name__ == '__main__':
    # main()
    unittest.main()

import unittest
from typing import List
from enum import Enum


INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"


class Instruction:
    def __init__(self, action: str, value: int):
        self.action = action
        self.value = value

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

def getInstructions(inputFile: str):
    instructions = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            instructions.append(Instruction(line[0], int(line[1:])))
    return instructions


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class FerryMover:
    def __init__(self):
        self.position: Coordinate = Coordinate(0,0)
        self.wayPoint: Coordinate = Coordinate(10, 1)


    def turnRight(self):
        self.wayPoint.x, self.wayPoint.y = self.wayPoint.y, self.wayPoint.x * -1


    def turnLeft(self):
        for i in range(0, 3):
            self.turnRight()

    # def handleCompass(self, coordinateToModify):
    #     if instruction.action == Compass.NORTH.value:
    #         coordinateToModify.y += instruction.value
    #     elif instruction.action == Compass.SOUTH.value:
    #         coordinateToModify.y -= instruction.value
    #     elif instruction.action == Compass.WEST.value:
    #         coordinateToModify.x -= instruction.value
    #     elif instruction.action == Compass.EAST.value:
    #         coordinateToModify.x += instruction.value

    def followInstruction(self, instruction: Instruction):
        if instruction.action == Compass.NORTH.value:
            self.wayPoint.y += instruction.value
        elif instruction.action == Compass.SOUTH.value:
            self.wayPoint.y -= instruction.value
        elif instruction.action == Compass.WEST.value:
            self.wayPoint.x -= instruction.value
        elif instruction.action == Compass.EAST.value:
            self.wayPoint.x += instruction.value


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



    def moveForward(self, value):
        self.position.x += self.wayPoint.x * value
        self.position.y += self.wayPoint.y * value

        # vektor 90 fokkal ugy forgatom el jobbra h megcsereleme a ket koordinatajat ;s veszem az y negaltjat

        # kozoes a ket reszben: forward implementacioja az h self.position += self.waypointvector
        # elso resyben a self.waypointvector az


        # self.wayPoint az self.waypointvector
        # self.waypointvector alapbol (1,0), mert east wayPoint a hajo az elso part elejen
        # self.position =+ self.waypointvector
        # amikor forgatod, akkor a waypoint vectort forgatod 90 fokkal
        
        # masodik reszben a north-south-east-west a waypoint vectort valtoztatja
        # nevezheted velocity vectornak is
        # masodik reszben annyi a kulonbseg h a compass nem a positiont(position) valtoztatje hanem a waypointot


    def getManhattanDistanceFromOrigin(self):
        return abs(self.position.x) + abs(self.position.y)



instructions = getInstructions(INPUT_FILE)

ferryMover = FerryMover()

for ins in instructions:
    ferryMover.followInstruction(ins)


print(ferryMover.getManhattanDistanceFromOrigin())

# not 53658 not 55244, should be 52742

# test should be 286






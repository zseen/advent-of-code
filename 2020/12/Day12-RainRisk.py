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
        self.state = Coordinate(0,0)
        self.facing = Compass.EAST

    def followInstruction(self, instruction: Instruction):
        if instruction.action == Compass.NORTH.value:
            self.state.y += instruction.value
        elif instruction.action == Compass.SOUTH.value:
            self.state.y -= instruction.value
        elif instruction.action == Compass.WEST.value:
            self.state.x -= instruction.value
        elif instruction.action == Compass.EAST.value:
            self.state.x += instruction.value
        elif instruction.action == Direction.RIGHT.value or instruction.action == Direction.LEFT.value:
            self.turn(instruction)
        elif instruction.action == Move.FORWARD.value:
            self.moveForward(instruction.value)
        else:
            raise ValueError("Unknown instruction received.")



    def turn(self, instruction):
        if instruction.action == Direction.RIGHT.value:
            if instruction.value == 90:
                if self.facing == Compass.NORTH:
                    self.facing = Compass.EAST
                elif self.facing == Compass.EAST:
                    self.facing = Compass.SOUTH
                elif self.facing == Compass.SOUTH:
                    self.facing = Compass.WEST
                elif self.facing == Compass.WEST:
                    self.facing = Compass.NORTH

            elif instruction.value == 180:
                if self.facing == Compass.NORTH:
                    self.facing = Compass.SOUTH
                elif self.facing == Compass.EAST:
                    self.facing = Compass.WEST
                elif self.facing == Compass.SOUTH:
                    self.facing = Compass.NORTH
                elif self.facing == Compass.WEST:
                    self.facing = Compass.EAST

            elif instruction.value == 270:
                if self.facing == Compass.NORTH:
                    self.facing = Compass.WEST
                elif self.facing == Compass.EAST:
                    self.facing = Compass.NORTH
                elif self.facing == Compass.SOUTH:
                    self.facing = Compass.EAST
                elif self.facing == Compass.WEST:
                    self.facing = Compass.SOUTH

        elif instruction.action == Direction.LEFT.value:
            if instruction.value == 90:
                if self.facing == Compass.NORTH:
                    self.facing = Compass.WEST
                elif self.facing == Compass.WEST:
                    self.facing = Compass.SOUTH
                elif self.facing == Compass.EAST:
                    self.facing = Compass.NORTH
                elif self.facing == Compass.SOUTH:
                    self.facing = Compass.EAST
            elif instruction.value == 180:
                if self.facing == Compass.NORTH:
                    self.facing = Compass.SOUTH
                elif self.facing == Compass.EAST:
                    self.facing = Compass.WEST
                elif self.facing == Compass.SOUTH:
                    self.facing = Compass.NORTH
                elif self.facing == Compass.WEST:
                    self.facing = Compass.EAST

            elif instruction.value == 270:
                if self.facing == Compass.NORTH:
                    self.facing = Compass.EAST
                elif self.facing == Compass.EAST:
                    self.facing = Compass.SOUTH
                elif self.facing == Compass.SOUTH:
                    self.facing = Compass.WEST
                elif self.facing == Compass.WEST:
                    self.facing = Compass.NORTH


    def moveForward(self, value):
        if self.facing == Compass.EAST:
            self.state.x += value
        elif self.facing == Compass.WEST:
            self.state.x -= value
        elif self.facing == Compass.NORTH:
            self.state.y += value
        elif self.facing == Compass.SOUTH:
            self.state.y -= value

    def getManhattanDistanceFromOrigin(self):
        return abs(self.state.x) + abs(self.state.y)



instructions = getInstructions(INPUT_FILE)

ferryMover = FerryMover()

for ins in instructions:
    ferryMover.followInstruction(ins)


print(ferryMover.getManhattanDistanceFromOrigin())








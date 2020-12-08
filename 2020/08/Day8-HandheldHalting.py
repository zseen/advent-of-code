import  unittest
from typing import List
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

class Operation(Enum):
    JUMP = "jmp"
    ACCELERATE = "acc"
    NO_OPERATION = "nop"


class Instruction:
    def __init__(self, operation, argument):
        self.operation = operation
        self.argument = argument
        self.isFollowed = False

def followInstructions(instructions: List):
    accelerator = 0
    if not instructions:
        raise ValueError("No insstructions to follow")
    currentInstruction = instructions[0]

    while True:
        if currentInstruction.operation == Operation.NO_OPERATION.value:
            if currentInstruction.isFollowed:
                break
            currentInstruction.isFollowed = True
            currentInstructionIndex = instructions.index(currentInstruction)
            currentInstruction = instructions[currentInstructionIndex % len(instructions) + 1]
        if currentInstruction.operation == Operation.ACCELERATE.value:
            if currentInstruction.isFollowed:
                break
            currentInstruction.isFollowed = True
            accelerator += int(currentInstruction.argument)
            currentInstructionIndex = instructions.index(currentInstruction)
            currentInstruction = instructions[currentInstructionIndex % len(instructions) + 1]
        if currentInstruction.operation == Operation.JUMP.value:
            if currentInstruction.isFollowed:
                break
            currentInstruction.isFollowed = True
            currentInstructionIndex = instructions.index(currentInstruction)
            currentInstruction = instructions[currentInstructionIndex % len(instructions) + int(currentInstruction.argument)]

    return accelerator




def getInput(inputFile):
    instructionsLines = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" ")
            instruction = Instruction(line[0], line[1])
            instructionsLines.append(instruction)

    return instructionsLines



# l = getInput(TEST_INPUT_FILE)
#
# accValue = followInstructions(l)
# print(accValue)

instructions = getInput(INPUT_FILE)
accValue = followInstructions(instructions)  # 1594
print(accValue)
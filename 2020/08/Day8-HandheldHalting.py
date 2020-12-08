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
    currentInstructionIndex = instructions.index(currentInstruction)
    while True:
        if currentInstruction.operation == Operation.NO_OPERATION.value:
            if currentInstruction.isFollowed:
                break
            prevInstruction = currentInstruction
            currentInstructionIndex = instructions.index(currentInstruction)
            currentInstruction = instructions[currentInstructionIndex + 1]
            prevInstruction.isFollowed = True
        if currentInstruction.operation == Operation.ACCELERATE.value:
            if currentInstruction.isFollowed:
                break
            accelerator += int(currentInstruction.argument)
            currentInstructionIndex = instructions.index(currentInstruction)
            prevInstruction = currentInstruction
            currentInstruction = instructions[currentInstructionIndex + 1]
            prevInstruction.isFollowed = True
        if currentInstruction.operation == Operation.JUMP.value:
            if currentInstruction.isFollowed:
                break
            currentInstructionIndex = instructions.index(currentInstruction)
            prevInstruction = currentInstruction
            currentInstruction = instructions[currentInstructionIndex + int(currentInstruction.argument)]
            prevInstruction.isFollowed = True
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


def extendInstructions(instructions):
    for i in range(10):
        instructions.extend(instructions)
    return instructions

# l = getInput(TEST_INPUT_FILE)
#
# accValue = followInstructions(l)
# print(accValue)

instructions = getInput(INPUT_FILE)
ins = extendInstructions(instructions)
accValue = followInstructions(ins)  # not 87
print(accValue)
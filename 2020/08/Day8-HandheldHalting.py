import unittest
from typing import List
from enum import Enum
from copy import deepcopy

INPUT_FILE = "input.txt"
TEST_INPUT_FILE_LOOP = "test_input_loop.txt"
TEST_INPUT_FILE_TERMINATION = "test_input_termination.txt"


class Operation(Enum):
    JUMP = "jmp"
    ACCELERATE = "acc"
    NO_OPERATION = "nop"


class Instruction:
    def __init__(self, operation, argument):
        self.operation = operation
        self.argument = argument
        self.isFollowed = False


def getAcceleratorCountInOneLoop(instructions: List):
    accelerator = 0
    if not instructions:
        raise ValueError("No instructions to follow")
    currentInstruction = instructions[0]
    nextInstructionOffset = 1

    while True:
        if currentInstruction.isFollowed:
            break

        currentInstructionIndex = instructions.index(currentInstruction)
        if currentInstruction.operation == Operation.NO_OPERATION.value:
            pass
        elif currentInstruction.operation == Operation.ACCELERATE.value:
            accelerator += int(currentInstruction.argument)
        elif currentInstruction.operation == Operation.JUMP.value:
            nextInstructionOffset = int(currentInstruction.argument)
        else:
            raise ValueError("Unexpected instruction")

        currentInstruction.isFollowed = True
        currentInstruction = instructions[(currentInstructionIndex % (len(instructions) - 1)) + nextInstructionOffset]
        nextInstructionOffset = 1

    return accelerator


def getAcceleratorCountWithTermination(instructions: List[Instruction]):
    accelerator = 0
    if not instructions:
        raise ValueError("No instructions to follow")

    currentInstruction = instructions[0]
    nextInstructionOffset = 1
    shouldTerminate = False

    while not shouldTerminate:
        shouldTerminate = currentInstruction == instructions[-1]

        if currentInstruction.isFollowed:
            break

        currentInstructionIndex = instructions.index(currentInstruction)
        if currentInstruction.operation == Operation.NO_OPERATION.value:
            pass
        elif currentInstruction.operation == Operation.ACCELERATE.value:
            accelerator += int(currentInstruction.argument)
        elif currentInstruction.operation == Operation.JUMP.value:
            nextInstructionOffset = int(currentInstruction.argument)

        else:
            raise ValueError("Unexpected instruction")

        currentInstruction.isFollowed = True
        currentInstruction = instructions[(currentInstructionIndex % (len(instructions) - 1)) + nextInstructionOffset]
        nextInstructionOffset = 1

    return accelerator, shouldTerminate


def getAcceleratorCountWithFixedInstructionProcess(instructions: List[Instruction]):
    originalInstructions = deepcopy(instructions)

    for i in range(0, len(instructions)):
        if instructions[i].operation == Operation.JUMP.value:
            instructions[i].operation = Operation.NO_OPERATION.value
        elif instructions[i].operation == Operation.NO_OPERATION.value:
            instructions[i].operation = Operation.JUMP.value
        accWithTerm = getAcceleratorCountWithTermination(instructions)
        if accWithTerm[1]:
            return accWithTerm[0]

        instructions = deepcopy(originalInstructions)


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


def main():
    instructions = getInput(INPUT_FILE)
    acceleratorCountInOneLoop = getAcceleratorCountInOneLoop(instructions)
    print(acceleratorCountInOneLoop)

    instructions = getInput(INPUT_FILE)
    acceleratorIfTerminationFixed = getAcceleratorCountWithFixedInstructionProcess(instructions)
    print(acceleratorIfTerminationFixed)


if __name__ == '__main__':
    main()

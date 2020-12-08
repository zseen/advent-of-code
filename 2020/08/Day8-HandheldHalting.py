import  unittest
from typing import List
from enum import Enum

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"
TEST_INPUT_FILE_SECOND_PART_FIRST = "test_input_second_part_1.txt"
TEST_INPUT_FILE_SECOND_PART_SECOND = "test_input_second_part_2.txt"

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
        currentInstruction = instructions[(currentInstructionIndex % (len(instructions) -1)) + nextInstructionOffset]
        nextInstructionOffset = 1


    return accelerator


#def getNextInstruction(currentInstruction):





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



l = getInput(TEST_INPUT_FILE)
accValue = followInstructions(l)

instructions = getInput(INPUT_FILE)
accValue2 = followInstructions(instructions)  # 1594

ins = getInput(TEST_INPUT_FILE_SECOND_PART_SECOND)
acc = followInstructions(ins)
print(accValue == 5, accValue2 == 1594, acc == 8)
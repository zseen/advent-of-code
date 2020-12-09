import unittest
from typing import List
from enum import Enum
from copy import deepcopy

INPUT_FILE = "input.txt"
TEST_INPUT_FILE_LOOP = "test_input_loop.txt"


class Operation(Enum):
    JUMP = "jmp"
    ACCUMULATE = "acc"
    NO_OPERATION = "nop"


class Instruction:
    def __init__(self, positionInProcess, operation, argument):
        self.positionInProcess: int = positionInProcess
        self.operation: str = operation
        self.argument: str = argument


class TerminationOutcome:
    def __init__(self, accelerationCount, isLoopDetected, isEndOfInstructionsReached):
        self.accumulatorCount: int = accelerationCount
        self.isLoopDetected: bool = isLoopDetected
        self.isEndOfInstructionsReached: bool = isEndOfInstructionsReached


def getAccumulatorCountInOneLoop(instructions: List[Instruction]):
    return getTerminationConditions(instructions).accumulatorCount


def getTerminationConditions(instructions: List[Instruction]):
    accumulatorCount = 0
    if not instructions:
        raise ValueError("No instructions to follow")

    currentInstruction = instructions[0]
    executedInstructionsInProcess = set()
    shouldTerminate = False
    isLoopDetected = False

    while not shouldTerminate:
        shouldTerminate = currentInstruction == instructions[-1]

        if currentInstruction in executedInstructionsInProcess:
            isLoopDetected = True
            break

        currentInstructionIndex = currentInstruction.positionInProcess
        if currentInstruction.operation == Operation.NO_OPERATION.value:
            nextInstructionPositionOffset = 1
        elif currentInstruction.operation == Operation.ACCUMULATE.value:
            accumulatorCount += int(currentInstruction.argument)
            nextInstructionPositionOffset = 1
        elif currentInstruction.operation == Operation.JUMP.value:
            nextInstructionPositionOffset = int(currentInstruction.argument)
        else:
            raise ValueError("Unexpected instruction")

        executedInstructionsInProcess.add(currentInstruction)
        currentInstruction = instructions[
            (currentInstructionIndex % (len(instructions) - 1)) + nextInstructionPositionOffset]

    terminationState = TerminationOutcome(accumulatorCount, isLoopDetected, shouldTerminate)
    return terminationState


def getAccumulatorCountWithFixedInstructionProcess(instructions: List[Instruction]):
    originalInstructions = deepcopy(instructions)

    for i in range(0, len(instructions)):
        if instructions[i].operation == Operation.JUMP.value:
            instructions[i].operation = Operation.NO_OPERATION.value
        elif instructions[i].operation == Operation.NO_OPERATION.value:
            instructions[i].operation = Operation.JUMP.value
        terminationState = getTerminationConditions(instructions)
        if terminationState.isEndOfInstructionsReached:
            return terminationState.accumulatorCount
        instructions[i] = deepcopy(originalInstructions)[i]


def getInput(inputFile):
    instructionsLines = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for i in range(0, len(lines)):
            line = lines[i]
            line = line.strip("\n")
            line = line.split(" ")
            instruction = Instruction(i, line[0], line[1])
            instructionsLines.append(instruction)
    return instructionsLines


def main():
    instructions = getInput(INPUT_FILE)
    accumulatorCountInOneLoop = getAccumulatorCountInOneLoop(instructions)
    print(accumulatorCountInOneLoop)  # 1594

    instructions = getInput(INPUT_FILE)
    accumulatorIfTerminationFixed = getAccumulatorCountWithFixedInstructionProcess(instructions)
    print(accumulatorIfTerminationFixed)  # 758


class AccumulatorCounter(unittest.TestCase):
    def test_getAccumulatorCountInOneLoop_loopingInstructions_correctCountReturned(self):
        instructions = getInput(TEST_INPUT_FILE_LOOP)
        accumulatorCount = getAccumulatorCountInOneLoop(instructions)
        self.assertEqual(5, accumulatorCount)

    def test_getAccumulatorCountWithFixedInstructionProcess_loopingInstructions_correctCountReturned(self):
        instructions = getInput(TEST_INPUT_FILE_LOOP)
        accumulatorCount = getAccumulatorCountWithFixedInstructionProcess(instructions)
        self.assertEqual(8, accumulatorCount)


if __name__ == '__main__':
    main()
    unittest.main()

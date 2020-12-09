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
    def __init__(self, operation: str, argument: int):
        self.operation: str = operation
        self.argument: int = argument


class TerminationOutcome:
    def __init__(self, accumulatorCount: int, isEndOfInstructionsReached: bool):
        self.accumulatorCount: int = accumulatorCount
        self.isEndOfInstructionsReached: bool = isEndOfInstructionsReached


def getAccumulatorCountInOneLoop(instructions: List[Instruction]):
    return getTerminationConditions(instructions).accumulatorCount


def getTerminationConditions(instructions: List[Instruction]):
    accumulatorCount = 0
    if not instructions:
        raise ValueError("No instructions to follow")

    currentInstructionIndex = 0
    executedInstructionsInProcess = set()
    shouldTerminate = False

    while not shouldTerminate:
        currentInstruction = instructions[currentInstructionIndex]
        if currentInstruction in executedInstructionsInProcess:
            break

        if currentInstruction.operation == Operation.NO_OPERATION.value:
            currentInstructionIndex += 1
        elif currentInstruction.operation == Operation.ACCUMULATE.value:
            accumulatorCount += currentInstruction.argument
            currentInstructionIndex += 1
        elif currentInstruction.operation == Operation.JUMP.value:
            currentInstructionIndex += currentInstruction.argument
        else:
            raise ValueError("Unexpected instruction")

        executedInstructionsInProcess.add(currentInstruction)
        shouldTerminate = currentInstructionIndex == len(instructions)

    return TerminationOutcome(accumulatorCount, shouldTerminate)


def getAccumulatorCountWithRepairedInstructionProcess(instructions: List[Instruction]):
    for i in range(0, len(instructions)):
        modifiedInstructions = deepcopy(instructions)
        if modifiedInstructions[i].operation == Operation.JUMP.value:
            modifiedInstructions[i].operation = Operation.NO_OPERATION.value
        elif modifiedInstructions[i].operation == Operation.NO_OPERATION.value:
            modifiedInstructions[i].operation = Operation.JUMP.value
        else:
            continue

        terminationState = getTerminationConditions(modifiedInstructions)
        if terminationState.isEndOfInstructionsReached:
            return terminationState.accumulatorCount

    raise ValueError("Could not be repaired.")


def getInput(inputFile):
    instructionsLines = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            line = line.split(" ")
            instruction = Instruction(line[0], int(line[1]))
            instructionsLines.append(instruction)
    return instructionsLines


def main():
    instructions = getInput(INPUT_FILE)
    accumulatorCountInOneLoop = getAccumulatorCountInOneLoop(instructions)
    print(accumulatorCountInOneLoop)  # 1594

    accumulatorCountIfTerminationRepaired = getAccumulatorCountWithRepairedInstructionProcess(instructions)
    print(accumulatorCountIfTerminationRepaired)  # 758


class AccumulatorCounter(unittest.TestCase):
    def test_getAccumulatorCountInOneLoop_loopingInstructions_correctCountReturned(self):
        instructions = getInput(TEST_INPUT_FILE_LOOP)
        accumulatorCount = getAccumulatorCountInOneLoop(instructions)
        self.assertEqual(5, accumulatorCount)

    def test_getAccumulatorCountWithRepairedInstructionProcess_loopingInstructions_correctCountReturned(self):
        instructions = getInput(TEST_INPUT_FILE_LOOP)
        accumulatorCount = getAccumulatorCountWithRepairedInstructionProcess(instructions)
        self.assertEqual(8, accumulatorCount)


if __name__ == '__main__':
    # main()
    unittest.main()

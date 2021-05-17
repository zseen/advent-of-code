from typing import List
from Direction import Direction


def getInput(inputFile: str) -> List[List[Direction]]:
    directionsCollection: List[List[Direction]] = []
    with open(inputFile, "r") as inputFile:
        lines = inputFile.readlines()
        for line in lines:
            line = line.strip("\n")
            directions: List[Direction] = []
            charPosition = 0
            while charPosition < len(line) - 1:
                currentChar = line[charPosition]
                nextChar = line[charPosition + 1]
                if currentChar + nextChar == Direction.NORTHEAST.value:
                    directions.append(Direction.NORTHEAST)
                    charPosition += 2
                elif currentChar + nextChar == Direction.NORTHWEST.value:
                    directions.append(Direction.NORTHWEST)
                    charPosition += 2
                elif currentChar + nextChar == Direction.SOUTHEAST.value:
                    directions.append(Direction.SOUTHEAST)
                    charPosition += 2
                elif currentChar + nextChar == Direction.SOUTHWEST.value:
                    directions.append(Direction.SOUTHWEST)
                    charPosition += 2
                elif currentChar == Direction.EAST.value:
                    directions.append(Direction.EAST)
                    charPosition += 1
                elif currentChar == Direction.WEST.value:
                    directions.append(Direction.WEST)
                    charPosition += 1
                else:
                    raise ValueError("Unexpected direction when reading input.", currentChar)

            if charPosition == len(line) - 1:
                currentChar = line[charPosition]
                if currentChar == Direction.EAST.value:
                    directions.append(Direction.EAST)
                elif currentChar == Direction.WEST.value:
                    directions.append(Direction.WEST)
                else:
                    raise ValueError("Unexpected direction when reading input.", currentChar)

            directionsCollection.append(directions)

    return directionsCollection

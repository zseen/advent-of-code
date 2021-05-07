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
                if line[charPosition] + line[charPosition + 1] == Direction.NORTHEAST.value:
                    directions.append(Direction.NORTHEAST)
                    charPosition += 1
                elif line[charPosition] + line[charPosition + 1] == Direction.NORTHWEST.value:
                    directions.append(Direction.NORTHWEST)
                    charPosition += 1
                elif line[charPosition] + line[charPosition + 1] == Direction.SOUTHEAST.value:
                    directions.append(Direction.SOUTHEAST)
                    charPosition += 1
                elif line[charPosition] + line[charPosition + 1] == Direction.SOUTHWEST.value:
                    directions.append(Direction.SOUTHWEST)
                    charPosition += 1
                elif line[charPosition] == Direction.EAST.value:
                    directions.append(Direction.EAST)
                elif line[charPosition] == Direction.WEST.value:
                    directions.append(Direction.WEST)
                else:
                    raise ValueError("Unexpected direction when reading input.", line[charPosition])
                charPosition += 1

            if charPosition == len(line) - 1:
                if line[charPosition] == Direction.EAST.value:
                    directions.append(Direction.EAST)
                elif line[charPosition] == Direction.WEST.value:
                    directions.append(Direction.WEST)
                else:
                    raise ValueError("Unexpected direction when reading input.", line[charPosition])

            directionsCollection.append(directions)

    return directionsCollection

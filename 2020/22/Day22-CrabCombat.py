import unittest
from typing import List

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"


def getInput(inputFile: str):
    with open(inputFile, "r") as inputFile:
        lines = inputFile.read()
        linesSplit = lines.split("\n\n")
        playerOneCards = [int(card) for card in linesSplit[0].split(":")[1].split()]
        playerTwoCards = [int(card) for card in linesSplit[1].split(":")[1].split()]

    return playerOneCards, playerTwoCards


def play(playerOneDeck, playerTwoDeck):
    while playerOneCards and playerTwoCards:
        playerOneFirstCard = playerOneDeck.pop(0)
        playerTwoFirstCard = playerTwoDeck.pop(0)

        if playerOneFirstCard > playerTwoFirstCard:
            playerOneDeck.append(playerOneFirstCard)
            playerOneDeck.append(playerTwoFirstCard)
        elif playerTwoFirstCard > playerOneFirstCard:
            playerTwoDeck.append(playerTwoFirstCard)
            playerTwoDeck.append(playerOneFirstCard)
        else:
            ValueError("Cards have the same value.")

    return playerOneDeck if playerOneDeck else playerTwoDeck


def calculateScore(winnerDeck):
    score = 0
    winnerDeckReversed = winnerDeck[::-1]
    for i in range(0, len(winnerDeckReversed)):
        score += winnerDeckReversed[i] * (i + 1)
    return score

playerOneCards, playerTwoCards = getInput(INPUT_FILE)
print(playerOneCards, playerTwoCards)
winner = play(playerOneCards, playerTwoCards)
print(playerOneCards, playerTwoCards)
print(calculateScore(winner))






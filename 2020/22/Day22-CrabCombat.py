import unittest
from typing import List
from enum import Enum
from copy import deepcopy

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"

class Winner(Enum):
    FIRST_PLAYER_WON = "First player won."
    SECOND_PLAYER_WON = "Second player won."

class Player:
    def __init__(self, deck):
        self.deck = deck
        self.previousDecksInMatch = []

    def hasCurrentDeckAppearedBefore(self):
        return self.deck in self.previousDecksInMatch

    def addCardToDeck(self, card: int):
        self.deck.append(card)

    def getCurrentDeckSize(self):
        return len(self.deck)

class CardGame:
    def __init__(self, firstPlayer: Player, secondPlayer: Player):
        self.firstPlayer = firstPlayer
        self.secondPlayer = secondPlayer
        self.gameEndResult = None


    def play(self) -> None:
        while self.firstPlayer.deck and self.secondPlayer.deck:
            playerOneFirstCard = self.firstPlayer.deck.pop(0)
            playerTwoFirstCard = self.secondPlayer.deck.pop(0)

            if playerOneFirstCard > playerTwoFirstCard:
                self.firstPlayer.addCardToDeck(playerOneFirstCard)
                self.firstPlayer.addCardToDeck(playerTwoFirstCard)
            elif playerTwoFirstCard > playerOneFirstCard:
                self.secondPlayer.addCardToDeck(playerTwoFirstCard)
                self.secondPlayer.addCardToDeck(playerOneFirstCard)
            else:
                ValueError("Cards have the same value.")

        self.gameEndResult = Winner.FIRST_PLAYER_WON if self.firstPlayer.deck else Winner.SECOND_PLAYER_WON


    def calculateScore(self):
        if not self.gameEndResult:
            raise ValueError("Winner not determined yet, so score cannot be calculated.")

        winnerDeck = self.firstPlayer.deck if self.gameEndResult == Winner.FIRST_PLAYER_WON else self.secondPlayer.deck
        score = 0
        winnerDeckReversed = winnerDeck[::-1]
        for i in range(0, len(winnerDeckReversed)):
            score += winnerDeckReversed[i] * (i + 1)
        return score

class RecursiveCombat(CardGame):
    def play(self):
        while self.firstPlayer.deck and self.secondPlayer.deck:
            if self.firstPlayer.hasCurrentDeckAppearedBefore() is True and self.secondPlayer.hasCurrentDeckAppearedBefore() is True:
                print(self.firstPlayer.deck, " + ", self.firstPlayer.previousDecksInMatch)
                print(self.secondPlayer.deck, " + ", self.secondPlayer.previousDecksInMatch)
                self.gameEndResult = Winner.FIRST_PLAYER_WON
                return

            self.firstPlayer.previousDecksInMatch.append(deepcopy(self.firstPlayer.deck))
            self.secondPlayer.previousDecksInMatch.append(deepcopy(self.secondPlayer.deck))

            playerOneFirstCard = self.firstPlayer.deck.pop(0)
            playerTwoFirstCard = self.secondPlayer.deck.pop(0)

            if self.firstPlayer.getCurrentDeckSize() >= playerOneFirstCard and self.secondPlayer.getCurrentDeckSize() >= playerTwoFirstCard:
                subgameWinner = self.playSubGame(playerOneFirstCard, playerTwoFirstCard)
                if subgameWinner == Winner.FIRST_PLAYER_WON:
                    self.firstPlayer.addCardToDeck(playerOneFirstCard)
                    self.firstPlayer.addCardToDeck(playerTwoFirstCard)
                elif subgameWinner == Winner.SECOND_PLAYER_WON:
                    self.secondPlayer.addCardToDeck(playerTwoFirstCard)
                    self.secondPlayer.addCardToDeck(playerOneFirstCard)
            else:
                if playerOneFirstCard > playerTwoFirstCard:
                    self.firstPlayer.addCardToDeck(playerOneFirstCard)
                    self.firstPlayer.addCardToDeck(playerTwoFirstCard)
                elif playerTwoFirstCard > playerOneFirstCard:
                    self.secondPlayer.addCardToDeck(playerTwoFirstCard)
                    self.secondPlayer.addCardToDeck(playerOneFirstCard)

        self.gameEndResult = Winner.FIRST_PLAYER_WON if self.firstPlayer.deck else Winner.SECOND_PLAYER_WON



    def playSubGame(self, playerOneFirstCard, playerTwoFirstCard):
        firstPlayerDeckForSubGame = self.firstPlayer.deck[:playerOneFirstCard]
        secondPlayerDeckForSubGame = self.secondPlayer.deck[:playerTwoFirstCard]

        firstPlayerPreviousDecks = []
        secondPlayerPreviousDecks = []


        while firstPlayerDeckForSubGame and secondPlayerDeckForSubGame:
            if firstPlayerDeckForSubGame in firstPlayerPreviousDecks and secondPlayerDeckForSubGame in secondPlayerPreviousDecks:
                return Winner.FIRST_PLAYER_WON

            firstPlayerPreviousDecks.append(deepcopy(firstPlayerDeckForSubGame))
            secondPlayerPreviousDecks.append(deepcopy(secondPlayerDeckForSubGame))

            playerOneFirstCard = firstPlayerDeckForSubGame.pop(0)
            playerTwoFirstCard = secondPlayerDeckForSubGame.pop(0)

            if playerOneFirstCard > playerTwoFirstCard:
                firstPlayerDeckForSubGame.append(playerOneFirstCard)
                firstPlayerDeckForSubGame.append(playerTwoFirstCard)
            elif playerTwoFirstCard > playerOneFirstCard:
                secondPlayerDeckForSubGame.append(playerTwoFirstCard)
                secondPlayerDeckForSubGame.append(playerOneFirstCard)
            else:
                ValueError("Cards have the same value.")

        return Winner.FIRST_PLAYER_WON if firstPlayerDeckForSubGame else Winner.SECOND_PLAYER_WON



def getInput(inputFile: str):
    with open(inputFile, "r") as inputFile:
        lines = inputFile.read()
        linesSplit = lines.split("\n\n")
        playerOneCards = [int(card) for card in linesSplit[0].split(":")[1].split()]
        playerTwoCards = [int(card) for card in linesSplit[1].split(":")[1].split()]

    return playerOneCards, playerTwoCards







playerOneCards, playerTwoCards = getInput(INPUT_FILE)
# playerOne = Player(playerOneCards)
# playerTwo = Player(playerTwoCards)
#
# game = CardGame(playerOne, playerTwo)
# game.play()
# print(game.calculateScore())


playerOne = Player(playerOneCards)
playerTwo = Player(playerTwoCards)

game = RecursiveCombat(playerOne, playerTwo)
game.play()
print(game.calculateScore()) # 9186 is too low








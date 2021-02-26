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

    def addCardsToDeck(self, cards: List[int]):
        for card in cards:
            self.deck.append(card)

    def getCurrentDeckSize(self):
        return len(self.deck)

    def addCurrentDeckToPreviousDecks(self):
        self.previousDecksInMatch.append(deepcopy(self.deck))

class CardGame:
    def __init__(self, firstPlayer: Player, secondPlayer: Player):
        self.firstPlayer = firstPlayer
        self.secondPlayer = secondPlayer
        self.gameEndResult = None
        self.currentRoundResult = None


    def play(self) -> None:
        while self.firstPlayer.deck and self.secondPlayer.deck:
            playerOneFirstCard = self.firstPlayer.deck.pop(0)
            playerTwoFirstCard = self.secondPlayer.deck.pop(0)
            self._determineRoundWinner(playerOneFirstCard, playerTwoFirstCard)
            self._addCardsToRoundWinningPlayerDeck(playerOneFirstCard, playerTwoFirstCard)

        self.gameEndResult = Winner.FIRST_PLAYER_WON if self.firstPlayer.deck else Winner.SECOND_PLAYER_WON

    def _determineRoundWinner(self, playerOneFirstCard, playerTwoFirstCard):
        if playerOneFirstCard > playerTwoFirstCard:
            self.currentRoundResult = Winner.FIRST_PLAYER_WON
        elif playerTwoFirstCard > playerOneFirstCard:
            self.currentRoundResult = Winner.SECOND_PLAYER_WON
        else:
            raise ValueError("Tie for this round.")


    def _addCardsToRoundWinningPlayerDeck(self, playerOneFirstCard, playerTwoFirstCard):
        if self.currentRoundResult == Winner.FIRST_PLAYER_WON:
            self.firstPlayer.addCardsToDeck([playerOneFirstCard, playerTwoFirstCard])
        elif self.currentRoundResult == Winner.SECOND_PLAYER_WON:
            self.secondPlayer.addCardsToDeck([playerTwoFirstCard, playerOneFirstCard])
        else:
            ValueError("No winner was determined for this round.")


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
    def play(self) -> None:
        while self.firstPlayer.deck and self.secondPlayer.deck:
            if self.firstPlayer.hasCurrentDeckAppearedBefore() and self.secondPlayer.hasCurrentDeckAppearedBefore():
                self.gameEndResult = Winner.FIRST_PLAYER_WON
                return

            self.firstPlayer.addCurrentDeckToPreviousDecks()
            self.secondPlayer.addCurrentDeckToPreviousDecks()

            playerOneFirstCard = self.firstPlayer.deck.pop(0)
            playerTwoFirstCard = self.secondPlayer.deck.pop(0)

            if self.firstPlayer.getCurrentDeckSize() >= playerOneFirstCard and self.secondPlayer.getCurrentDeckSize() >= playerTwoFirstCard:
                self.currentRoundResult = self.playSubGame(playerOneFirstCard, playerTwoFirstCard)
            else:
                self._determineRoundWinner(playerOneFirstCard, playerTwoFirstCard)
            self._addCardsToRoundWinningPlayerDeck(playerOneFirstCard, playerTwoFirstCard)

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
print(game.calculateScore()) # 33206








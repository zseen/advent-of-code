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
    def __init__(self, deck: List[int]):
        self.deck: List[int] = deck
        self.previousDecksInMatch: List[List[int]] = []

    def getCurrentDeckSize(self) -> int:
        return len(self.deck)

    def addCardsToDeck(self, cards: List[int]) -> None:
        for card in cards:
            self.deck.append(card)

    def hasCurrentDeckAppearedBefore(self) -> bool:
        return self.deck in self.previousDecksInMatch

    def addCurrentDeckToPreviousDecks(self) -> None:
        self.previousDecksInMatch.append(deepcopy(self.deck))

class CardGame:
    def __init__(self, firstPlayer: Player, secondPlayer: Player):
        self.firstPlayer: Player = firstPlayer
        self.secondPlayer: Player = secondPlayer
        self.gameEndResult: Winner = None
        self.currentRoundResult: Winner = None


    def play(self) -> None:
        while self.firstPlayer.deck and self.secondPlayer.deck:
            self._playRound()
        self.gameEndResult = Winner.FIRST_PLAYER_WON if self.firstPlayer.deck else Winner.SECOND_PLAYER_WON

    def _playRound(self) -> None:
        playerOneFirstCard: int = self.firstPlayer.deck.pop(0)
        playerTwoFirstCard: int = self.secondPlayer.deck.pop(0)
        self._determineRoundWinner(playerOneFirstCard, playerTwoFirstCard)
        self._addCardsToRoundWinningPlayerDeck(playerOneFirstCard, playerTwoFirstCard)

    def _determineRoundWinner(self, playerOneFirstCard: int, playerTwoFirstCard: int) -> None:
        if playerOneFirstCard > playerTwoFirstCard:
            self.currentRoundResult = Winner.FIRST_PLAYER_WON
        elif playerTwoFirstCard > playerOneFirstCard:
            self.currentRoundResult = Winner.SECOND_PLAYER_WON
        else:
            raise ValueError("Tie for this round - this was not meant to happen.")


    def _addCardsToRoundWinningPlayerDeck(self, playerOneFirstCard: int, playerTwoFirstCard: int) -> None:
        if self.currentRoundResult == Winner.FIRST_PLAYER_WON:
            self.firstPlayer.addCardsToDeck([playerOneFirstCard, playerTwoFirstCard])
        elif self.currentRoundResult == Winner.SECOND_PLAYER_WON:
            self.secondPlayer.addCardsToDeck([playerTwoFirstCard, playerOneFirstCard])
        else:
            ValueError("No winner was determined for this round.")


    def calculateScore(self) -> int:
        if not self.gameEndResult:
            raise ValueError("Winner not determined yet, so score cannot be calculated.")

        winnerDeck = self.firstPlayer.deck if self.gameEndResult == Winner.FIRST_PLAYER_WON else self.secondPlayer.deck
        return sum(winnerDeck[::-1][i] * (i + 1) for i in range(0, len(winnerDeck)))

class RecursiveCombat(CardGame):
    def play(self) -> None:
        while self.firstPlayer.deck and self.secondPlayer.deck:
            if self.firstPlayer.hasCurrentDeckAppearedBefore() and self.secondPlayer.hasCurrentDeckAppearedBefore():
                self.gameEndResult = Winner.FIRST_PLAYER_WON
                return

            self.firstPlayer.addCurrentDeckToPreviousDecks()
            self.secondPlayer.addCurrentDeckToPreviousDecks()

            playerOneFirstCard, playerTwoFirstCard  = self.firstPlayer.deck.pop(0), self.secondPlayer.deck.pop(0)

            if self.firstPlayer.getCurrentDeckSize() >= playerOneFirstCard and self.secondPlayer.getCurrentDeckSize() >= playerTwoFirstCard:
                self.currentRoundResult = self.playSubGame(playerOneFirstCard, playerTwoFirstCard)
            else:
                self._determineRoundWinner(playerOneFirstCard, playerTwoFirstCard)
            self._addCardsToRoundWinningPlayerDeck(playerOneFirstCard, playerTwoFirstCard)

        self.gameEndResult = Winner.FIRST_PLAYER_WON if self.firstPlayer.deck else Winner.SECOND_PLAYER_WON


    def playSubGame(self, playerOneFirstCard, playerTwoFirstCard):
        subGame = self._setUpSubGame(playerOneFirstCard, playerTwoFirstCard)
        while subGame.firstPlayer.deck and subGame.secondPlayer.deck:
            if subGame.firstPlayer.hasCurrentDeckAppearedBefore() and subGame.secondPlayer.hasCurrentDeckAppearedBefore():
                return Winner.FIRST_PLAYER_WON
            subGame.firstPlayer.addCurrentDeckToPreviousDecks()
            subGame.secondPlayer.addCurrentDeckToPreviousDecks()

            subGame._playRound()

        return Winner.FIRST_PLAYER_WON if subGame.firstPlayer.deck else Winner.SECOND_PLAYER_WON

    def _setUpSubGame(self, playerOneFirstCard, playerTwoFirstCard) -> CardGame:
        firstPlayerDeckForSubGame = self.firstPlayer.deck[:playerOneFirstCard]
        secondPlayerDeckForSubGame = self.secondPlayer.deck[:playerTwoFirstCard]

        firstPlayer = Player(firstPlayerDeckForSubGame)
        secondPlayer = Player(secondPlayerDeckForSubGame)

        subGame = CardGame(firstPlayer, secondPlayer)
        return subGame



def getInput(inputFile: str):
    with open(inputFile, "r") as inputFile:
        lines = inputFile.read()
        linesSplit = lines.split("\n\n")
        playerOneCards = [int(card) for card in linesSplit[0].split(":")[1].split()]
        playerTwoCards = [int(card) for card in linesSplit[1].split(":")[1].split()]

    return playerOneCards, playerTwoCards




def main():
    playerOneCards, playerTwoCards = getInput(INPUT_FILE)
    playerOne = Player(deepcopy(playerOneCards))
    playerTwo = Player(deepcopy(playerTwoCards))

    game = CardGame(playerOne, playerTwo)
    game.play()
    print(game.calculateScore()) # 32272

    playerOne2 = Player(playerOneCards)
    playerTwo2 = Player(playerTwoCards)

    game = RecursiveCombat(playerOne2, playerTwo2)
    game.play()
    print(game.calculateScore()) # 33206

if __name__ == '__main__':
    main()








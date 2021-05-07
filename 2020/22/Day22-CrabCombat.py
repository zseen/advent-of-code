import unittest
from typing import List, Deque, Tuple
from enum import Enum
from copy import deepcopy
from collections import deque

INPUT_FILE = "input.txt"
TEST_INPUT_FILE = "test_input.txt"


class Result(Enum):
    FIRST_PLAYER_WON = "First player won."
    SECOND_PLAYER_WON = "Second player won."


class Player:
    def __init__(self, deck: Deque[int]):
        self._deck: Deque[int] = deck
        self._previousDecksInMatch: Set[str] = set()

    def getDeck(self) -> Deque[int]:
        return self._deck

    def addCardsToDeck(self, cards: List[int]) -> None:
        self._deck.extend(cards)

    def drawTopCardFromDeck(self) -> int:
        return self._deck.popleft()

    def getCurrentDeckSize(self) -> int:
        return len(self._deck)

    def addCurrentDeckToPreviousDecks(self) -> None:
        self._previousDecksInMatch.add(str(self._deck))

    def hasCurrentDeckAppearedBefore(self) -> bool:
        return str(self._deck) in self._previousDecksInMatch


class Combat:
    def __init__(self, firstPlayer: Player, secondPlayer: Player):
        self._firstPlayer: Player = firstPlayer
        self._secondPlayer: Player = secondPlayer
        self._gameEndResult: Optional[Result] = None

    def play(self) -> None:
        while self._firstPlayer.getDeck() and self._secondPlayer.getDeck():
            self._playRound()
        self._gameEndResult = Result.FIRST_PLAYER_WON if self._firstPlayer.getDeck() else Result.SECOND_PLAYER_WON

    def _playRound(self) -> None:
        playerOneFirstCard: int = self._firstPlayer.drawTopCardFromDeck()
        playerTwoFirstCard: int = self._secondPlayer.drawTopCardFromDeck()
        currentRoundResult = self._determineRoundWinner(playerOneFirstCard, playerTwoFirstCard)
        self._addCardsToRoundWinningPlayerDeck(currentRoundResult, playerOneFirstCard, playerTwoFirstCard)

    def _determineRoundWinner(self, playerOneFirstCard: int, playerTwoFirstCard: int) -> Result:
        assert playerOneFirstCard != playerTwoFirstCard

        if playerOneFirstCard > playerTwoFirstCard:
            return Result.FIRST_PLAYER_WON
        else:
            return Result.SECOND_PLAYER_WON

    def _addCardsToRoundWinningPlayerDeck(self, currentRoundResult, playerOneFirstCard: int, playerTwoFirstCard: int) -> None:
        if not currentRoundResult:
            raise ValueError("No result for current round!")

        if currentRoundResult == Result.FIRST_PLAYER_WON:
            self._firstPlayer.addCardsToDeck([playerOneFirstCard, playerTwoFirstCard])
        elif currentRoundResult == Result.SECOND_PLAYER_WON:
            self._secondPlayer.addCardsToDeck([playerTwoFirstCard, playerOneFirstCard])

    def calculateScore(self) -> int:
        if not self._gameEndResult:
            raise ValueError("Result not determined yet, so score cannot be calculated.")

        winnerDeck = self._firstPlayer.getDeck() if self._gameEndResult == Result.FIRST_PLAYER_WON else self._secondPlayer.getDeck()
        return sum(list(winnerDeck)[::-1][i] * (i + 1) for i in range(0, len(winnerDeck)))


class RecursiveCombat(Combat):
    def play(self) -> None:
        while self._firstPlayer.getDeck() and self._secondPlayer.getDeck():
            if self._firstPlayer.hasCurrentDeckAppearedBefore() and self._secondPlayer.hasCurrentDeckAppearedBefore():
                self._gameEndResult = Result.FIRST_PLAYER_WON
                return

            self._firstPlayer.addCurrentDeckToPreviousDecks()
            self._secondPlayer.addCurrentDeckToPreviousDecks()

            playerOneFirstCard, playerTwoFirstCard = self._firstPlayer.drawTopCardFromDeck(), self._secondPlayer.drawTopCardFromDeck()

            if self._firstPlayer.getCurrentDeckSize() >= playerOneFirstCard and self._secondPlayer.getCurrentDeckSize() >= playerTwoFirstCard:
                currentRoundResult = self._playSubGame(playerOneFirstCard, playerTwoFirstCard)
            else:
                currentRoundResult = self._determineRoundWinner(playerOneFirstCard, playerTwoFirstCard)
            self._addCardsToRoundWinningPlayerDeck(currentRoundResult, playerOneFirstCard, playerTwoFirstCard)

        self._gameEndResult = Result.FIRST_PLAYER_WON if self._firstPlayer.getDeck() else Result.SECOND_PLAYER_WON

    def _playSubGame(self, playerOneFirstCard: int, playerTwoFirstCard: int) -> Result:
        playerOneDeck = self._firstPlayer.getDeck()
        playerTwoDeck = self._secondPlayer.getDeck()

        subGame = self._setUpSubGame(playerOneFirstCard, playerTwoFirstCard, playerOneDeck, playerTwoDeck)
        subGame.play()
        return Result.FIRST_PLAYER_WON if subGame._firstPlayer.getDeck() else Result.SECOND_PLAYER_WON

    def _setUpSubGame(self, playerOneFirstCard: int, playerTwoFirstCard: int, playerOneDeck, playerTwoDeck) -> Combat:
        firstPlayerDeckForSubGame = deque(list(playerOneDeck)[:playerOneFirstCard])
        secondPlayerDeckForSubGame = deque(list(playerTwoDeck)[:playerTwoFirstCard])
        firstPlayer = Player(firstPlayerDeckForSubGame)
        secondPlayer = Player(secondPlayerDeckForSubGame)

        return RecursiveCombat(firstPlayer, secondPlayer)


def getInput(inputFile: str) -> Tuple[Deque[int], Deque[int]]:
    with open(inputFile, "r") as inputFile:
        lines = inputFile.read()
        linesSplit = lines.split("\n\n")
        playerOneCards: Deque[int] = deque([int(card) for card in linesSplit[0].split(":")[1].split()])
        playerTwoCards: Deque[int] = deque([int(card) for card in linesSplit[1].split(":")[1].split()])

    return playerOneCards, playerTwoCards


def main():
    playerOneCards, playerTwoCards = getInput(INPUT_FILE)

    playerOneForCombat = Player(deepcopy(playerOneCards))
    playerTwoForCombat = Player(deepcopy(playerTwoCards))
    combat = Combat(playerOneForCombat, playerTwoForCombat)
    combat.play()
    print(combat.calculateScore())  # 32272

    playerOneForRecursiveCombat = Player(playerOneCards)
    playerTwoRecursiveCombat = Player(playerTwoCards)
    recursiveCombat = RecursiveCombat(playerOneForRecursiveCombat, playerTwoRecursiveCombat)
    recursiveCombat.play()
    print(recursiveCombat.calculateScore())  # 33206


class combatAndRecursiveCombatTester(unittest.TestCase):
    def setUp(self) -> None:
        self.playerOneCards, self.playerTwoCards = getInput(TEST_INPUT_FILE)

    def test_Combat_calculateScore_correctScoreCalculated(self):
        playerOneForCombat = Player(deepcopy(self.playerOneCards))
        playerTwoForCombat = Player(deepcopy(self.playerTwoCards))

        combat = Combat(playerOneForCombat, playerTwoForCombat)
        combat.play()

        self.assertEqual(combat.calculateScore(), 306)

    def test_RecursiveCombat_calculateScore_correctScoreCalculated(self):
        playerOneForRecursiveCombat = Player(deepcopy(self.playerOneCards))
        playerTwoForRecursiveCombat = Player(deepcopy(self.playerTwoCards))

        recursiveCombat = RecursiveCombat(playerOneForRecursiveCombat, playerTwoForRecursiveCombat)
        recursiveCombat.play()

        self.assertEqual(recursiveCombat.calculateScore(), 291)


if __name__ == '__main__':
    # main()
    unittest.main()

import random
from itertools import product
from enum import Enum
from typing import Any


class Card:
    """
    A class containing information about the value of the card.

    Methods:
    -------
    `__str__() -> str`:
        Returns a string representation of the card.

    `set_scores() -> None`:
        Sets the score of the card.
    """

    def __init__(self, suit: str, name: str | int) -> None:
        """Initializing a Card object"""
        self.suit = suit
        self.name = str(name)
        self.scores: set[int] = set()
        self.set_scores()

    def __str__(self) -> str:
        """Returns a string representation of the card."""
        return f"{self.name} of {self.suit}"

    def set_scores(self) -> None:
        """Sets the score of the card."""
        if self.name in {"10", "J", "Q", "K"}:
            self.scores.add(10)
        elif self.name == "A":
            self.scores.update((1, 11))
        else:
            self.scores.add(int(self.name))


class Deck:
    """
    A deck of cards.

    Methods:
    -------
    `shuffle() -> None`:
        Shuffles the deck of cards.

    `pull() -> Card`:
        Removes and returns the card at the beginning of the deck.

    """

    def __init__(self) -> None:
        """Initializing a Deck object"""
        self.cards = [
            Card(card[0], card[1])
            for card in product(
                ["Spades", "Hearts", "Diamonds", "Clubs"],
                list(range(2, 11)) + ["J", "Q", "K", "A"],
            )
        ]
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffles the deck of cards."""
        random.shuffle(self.cards)

    def pull(self) -> Card:
        """Removes and returns the card at the beginning of the deck."""
        return self.cards.pop(0)


class Cards:
    """
    The data-descriptor class for storing cards, scores, and game history.
    """

    def __init__(self) -> None:
        self.data: dict[Hand, dict[str, Any]] = {}

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        if instance not in self.data:
            self.data[instance] = {"cards": [], "scores": {0}, "history": []}
        return self.data[instance]

    def __set__(self, instance: Any, value: Any) -> None:
        self.data[instance] = value


class HandStates(Enum):
    """Enum to indicate the state of the hand."""

    DEFAULT = "The game is on"
    WIN = "Winning hand"
    LOSE = "Losing hand"
    BLACKJACK = "Blackjack"
    DRAWN_GAME = "Equal score"


class Hand:
    """
    The controller class above the Cards data-descriptor.
    The class responsible for the current state of the hand, the bet and the cards.

    Methods:
    -------
    `game_over() -> None`:
        Resets the bet and withdraws the hand from the game.

    `double_down() -> None`:
        Doubles the bet.

    `tripling_bet() -> None`:
        Triples the bet.

    `add_card(card: Card) -> None`:
        Adds a card to his hand and recalculates the scores.

    `calculate_score(card: Card) -> None`:
        Recalculate the scores.

    `check_blackjack() -> bool`:
        Check if there is a blackjack on this hand.

    `get_card(id_card: int) -> Any`:
        Returns the card with the number starting from the first received one.

    `get_scores() -> Any`:
        Returns the scores.

    'get_cards() -> Any':
        Returns the cards

    'show_history() -> None':
        Displays the console history of the player's actions.

    'show_hand(self) -> None':
        Displays the cards on your hand in the console.

    'show_bet(id_player: int) -> None':
        Displays the current bet in the console.

    'show_state(self) -> None':
        Displays the current hand status in the console.
    """

    hand = Cards()

    def __init__(self) -> None:
        """Initializing a Deck object"""
        self.bet = 0
        self.in_playing = True
        self.double_bet = False
        self.tripled_bet = False
        self.state = HandStates.DEFAULT

    def game_over(self) -> None:
        """Resets the bet and withdraws the hand from the game."""
        self.bet = 0
        self.in_playing = False

    def double_down(self) -> None:
        """Doubles the bet."""
        self.bet *= 2
        self.double_bet = True
        self.hand["history"].append("double down")

    def tripling_bet(self) -> None:
        """Triples the bet."""
        self.bet += int(self.bet // 2)
        self.tripled_bet = True
        self.hand["history"].append("tripling bet")

    def add_card(self, card: Card) -> None:
        """
        Adds a card to his hand and recalculate the scores.

        Args:
            card (Card): the card that was added to the hand.
        """
        self.hand["cards"].append(card)
        self.calculate_score(card)
        self.hand["history"].append("add card")

    def calculate_score(self, card: Card) -> None:
        """
        Recalculate the scores.

        Args:
            card (Card): the card that was added to the hand.
        """
        new_scores = set()
        for score in card.scores:
            new_scores.update(
                set(map(lambda x: x + score, self.hand["scores"]))
            )
        self.hand["scores"] = new_scores

    def check_blackjack(self) -> bool:
        """
        Check if there is a blackjack on this hand.

        Returns:
            result (bool): is blackjack
        """
        return 21 in self.hand["scores"] and len(self.hand["cards"]) == 2

    def get_card(self, id_card: int) -> Any:
        """
        Returns the card with the number starting from the first received one.

        Args:
            id_card (int): index of the card in hand.

        Returns:
            result (Any): card is under the desired index.
        """
        return self.hand["cards"][id_card]

    def get_scores(self) -> Any:
        """Returns the scores"""
        return self.hand["scores"]

    def get_cards(self) -> Any:
        """Returns the cards"""
        return self.hand["cards"]

    def show_history(self) -> None:
        """Displays the console history of the player's actions."""
        print("History of actions:")
        print(self.hand["history"], sep=", ")

    def show_hand(self) -> None:
        """Displays the cards on your hand in the console."""
        print("Hand:", end=" ")
        for card in self.hand["cards"]:
            print(card, end="; ")
        print()

        print("Scores:", end=" ")
        if 21 in self.hand["scores"]:
            print(21)
        elif min(self.hand["scores"]) > 21:
            print("bust")
        else:
            print(
                *[score for score in self.hand["scores"] if score <= 21],
                sep=" or ",
            )

    def show_bet(self, id_player: int) -> None:
        """Displays the current bet in the console."""
        print(f"Player's {id_player + 1} bet:", self.bet)

    def show_state(self) -> None:
        """Displays the current hand status in the console."""
        print("Hand condition:", self.state.value)

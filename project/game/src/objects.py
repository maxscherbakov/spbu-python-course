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
    """

    def __init__(self, suit: str, name: str | int) -> None:
        """Initializing a Card object"""
        self.suit = suit
        self.name = str(name)

    def __str__(self) -> str:
        """Returns a string representation of the card."""
        return f"{self.name} of {self.suit}"


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
            self.data[instance] = {"cards": [], "score": 0, "history": []}
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
    OUT = "Out of the game"


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

    `calculate_score() -> None`:
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
        self.calculate_score()
        self.hand["history"].append("add card")

    def calculate_score(self) -> None:
        """Recalculate the scores."""
        scores = {0}
        for card in self.hand["cards"]:
            match card.name:
                case "A":
                    scores = set(map(lambda x: x + 1, scores))
                    scores.update(set(map(lambda x: x + 10, scores)))
                case "K" | "Q" | "J" | "10":
                    scores = set(map(lambda x: x + 10, scores))
                case _:
                    scores = set(map(lambda x: x + int(card.name), scores))
        filter_scores = list(filter(lambda x: x <= 21, scores))
        if len(filter_scores) == 0:
            self.hand["score"] = -1
        else:
            self.hand["score"] = max(filter_scores)

    def check_blackjack(self) -> bool:
        """
        Check if there is a blackjack on this hand.

        Returns:
            result (bool): is blackjack
        """
        return 21 == self.hand["score"] and len(self.hand["cards"]) == 2

    def get_card(self, id_card: int) -> Any:
        """
        Returns the card with the number starting from the first received one.

        Args:
            id_card (int): index of the card in hand.

        Returns:
            result (Any): card is under the desired index.
        """
        return self.hand["cards"][id_card]

    def get_score(self) -> Any:
        """Returns the scores"""
        return self.hand["score"]

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

        print("Score:", end=" ")
        if self.hand["score"] == -1:
            print("bust")
        else:
            print(self.hand["score"])

    def show_bet(self, id_player: int) -> None:
        """Displays the current bet in the console."""
        print(f"Player's {id_player + 1} bet:", end=" ")
        if self.state is HandStates.OUT:
            print("not enough chips")
        else:
            print(self.bet)

    def show_state(self) -> None:
        """Displays the current hand status in the console."""
        print("Hand condition:", self.state.value)

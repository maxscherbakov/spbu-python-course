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
        self._cards = [
            Card(card[0], card[1])
            for card in product(
                ["Spades", "Hearts", "Diamonds", "Clubs"],
                list(range(2, 11)) + ["J", "Q", "K", "A"],
            )
        ]
        self.shuffle()

    def shuffle(self) -> None:
        """Shuffles the deck of cards."""
        random.shuffle(self._cards)

    def pull(self) -> Card:
        """Removes and returns the card at the beginning of the deck."""
        return self._cards.pop(0)


class Cards:
    """
    The data-descriptor class for storing cards, scores, and game history.
    """

    def __init__(self) -> None:
        self._data: dict[Hand, dict[str, Any]] = {}

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        if instance not in self._data:
            self._data[instance] = {"cards": [], "score": 0, "history": []}
        return self._data[instance]

    def __set__(self, instance: Any, value: Any) -> None:
        self._data[instance] = value


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

    'split() -> tuple["Hand", "Hand"]':
        The method for calling the split hand.

    'action_pass() -> None':
        Performs the pass action

    'even_money() -> None':
        Performs the even money action

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
        Returns the cards.

    'get_history(self) -> Any':
        Returns the history.

    'show_history() -> None':
        Displays the console history of the player's actions.

    'show_hand(self) -> None':
        Displays the cards on your hand in the console.

    'show_bet(id_player: int) -> None':
        Displays the current bet in the console.

    'show_state(self) -> None':
        Displays the current hand status in the console.
    """

    _hand = Cards()

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
        self._hand["history"].append("double down")

    def tripling_bet(self) -> None:
        """Triples the bet."""
        self.bet += int(self.bet // 2)
        self.tripled_bet = True
        self._hand["history"].append("tripling bet")

    def split(self) -> tuple["Hand", "Hand"]:
        """
        The method for calling the split hand.

        Returns:
            result ("Hand", "Hand"): two hands after the split.
        """
        bet = self._hand.bet

        split_hand_1 = Hand()
        split_hand_1._hand["history"] = ["split"]
        split_hand_1.bet = bet
        split_hand_1.add_card(self._hand.get_card(0))

        split_hand_2 = Hand()
        split_hand_2._hand["history"] = ["split"]
        split_hand_2.bet = bet
        split_hand_2.add_card(self._hand.get_card(1))
        return split_hand_1, split_hand_2

    def action_pass(self) -> None:
        """Performs the pass action"""
        self._hand["history"].append("pass")

    def even_money(self) -> None:
        """Performs the even money action"""
        self._hand["history"].append("even money")

    def add_card(self, card: Card) -> None:
        """
        Adds a card to his hand and recalculate the scores.

        Args:
            card (Card): the card that was added to the hand.
        """
        self._hand["cards"].append(card)
        self.calculate_score()
        self._hand["history"].append("add card")

    def calculate_score(self) -> None:
        """Recalculate the scores."""
        scores = {0}
        for card in self._hand["cards"]:
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
            self._hand["score"] = -1
        else:
            self._hand["score"] = max(filter_scores)

    def check_blackjack(self) -> bool:
        """
        Check if there is a blackjack on this hand.

        Returns:
            result (bool): is blackjack
        """
        return 21 == self._hand["score"] and len(self._hand["cards"]) == 2

    def get_card(self, id_card: int) -> Any:
        """
        Returns the card with the number starting from the first received one.

        Args:
            id_card (int): index of the card in hand.

        Returns:
            result (Any): card is under the desired index.
        """
        return self._hand["cards"][id_card]

    def get_score(self) -> Any:
        """Returns the scores"""
        return self._hand["score"]

    def get_cards(self) -> Any:
        """Returns the cards"""
        return self._hand["cards"]

    def get_history(self) -> Any:
        """Returns the history."""
        return self._hand["history"]

    def show_history(self) -> None:
        """Displays the console history of the player's actions."""
        print("History of actions:")
        print(self._hand["history"], sep=", ")

    def show_hand(self) -> None:
        """Displays the cards on your hand in the console."""
        print("Hand:", end=" ")
        for card in self._hand["cards"]:
            print(card, end="; ")
        print()

        print("Score:", end=" ")
        if self._hand["score"] == -1:
            print("bust")
        else:
            print(self._hand["score"])

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

from project.game.src.objects import Deck, Hand, Card
import random
from project.game.src.strategies import Basic, Strategy


class Player:
    """
    The player's class stores the number of chips and the strategy of the game.
    """

    def __init__(self, strategy: Strategy = Basic(), chips: int = 100) -> None:
        """Initializing a Player object."""
        self.strategy = strategy
        self.chips = chips


class Dealer:
    """
    The dealer's class that stores the dealer's decks and hand.

    Methods:
    -------
    'give_card() -> Card':
        A method for extracting a card from the deck.

    'show_hand() -> None':
        A method for displaying information about the dealer's hand in the console.

    'restart() -> None':
        A method that returns the dealer's state to the beginning of the game.
    """

    def __init__(self, num_decks: int) -> None:
        """Initializing a Dealer object."""
        self._num_decks = num_decks
        self.hand = Hand()
        self._decks = [Deck() for _ in range(num_decks)]

    def give_card(self) -> Card:
        """A method for extracting a card from the deck."""
        id_deck = random.randint(0, self._num_decks - 1)
        return self._decks[id_deck].pull()

    def show_hand(self) -> None:
        """A method for displaying information about the dealer's hand in the console."""
        print("Dealer's Hand:")
        self.hand.show_hand()

    def restart(self) -> None:
        """A method that returns the dealer's state to the beginning of the game."""
        self.hand = Hand()
        self._decks = [Deck() for _ in range(self._num_decks)]

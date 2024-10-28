from project.game.src.objects import Deck, Hand, Card
import random
from project.game.src.strategies import Basic, Strategy


class Player:
    def __init__(self, strategy: Strategy = Basic(), chips: int = 100) -> None:
        self.strategy = strategy
        self.chips = chips


class Dealer:
    def __init__(self, num_deck: int = 1) -> None:
        self.num_deck = num_deck
        self.hand = Hand()
        self._decks = [Deck() for _ in range(num_deck)]

    def give_card(self) -> Card:
        id_deck = random.randint(0, self.num_deck - 1)
        return self._decks[id_deck].pull()

    def show_hand(self) -> None:
        print("Рука дилера:")
        self.hand.show_hand()

    def restart(self) -> None:
        self.hand = Hand()
        self._decks = [Deck() for _ in range(self.num_deck)]

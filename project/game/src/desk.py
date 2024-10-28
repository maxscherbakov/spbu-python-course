from project.game.src.persons import Player, Dealer
from project.game.src.objects import Hand


class Desk:
    """
    The game table.
    The class contains information about the players, their cards and
    the dealer, as well as methods responsible for events in the game.

    Methods:
    -------
    `dealer_give_card(target_hand: Hand) -> None`:
        Issues a card from the dealer's deck to the target hand.

    `place_first_bets() -> None`:
        Players place their first bets in the amount specified in the strategy.

    `split(player: Player, id_hand: int) -> None`:
        The method is called if the player has chosen split.

    `check_bet(id_player: int, bet: int) -> bool`:
        Checks if the player has enough chips to bet.

    `next() -> None`:
        Sets the starting parameters for the table.

    """

    def __init__(self, players: list[Player]) -> None:
        """Initializing a Desk object."""
        self.players = players
        self.dealer = Dealer()
        self.hands: dict[Player, list[Hand]] = {}

    def dealer_give_card(self, target_hand: Hand) -> None:
        """
        Issues a card from the dealer's deck to the target hand.

        Args:
            target_hand (Hand): the hand to add the card to.
        """
        card = self.dealer.give_card()
        target_hand.add_card(card)

    def place_first_bets(self) -> None:
        """Players place their first bets in the amount specified in the strategy."""
        for id_player, player in enumerate(self.players):
            bet = player.strategy.first_bet
            self.check_bet(id_player, bet)
            player.chips -= bet
            self.hands[player][0].bet = bet

    def split(self, player: Player, id_hand: int) -> None:
        """
        The method is called if the player has chosen split.

        Args:
            player (Player): the player who chose the split.
            id_hand (int): the number of the hand for which the split is selected.
        """
        hand = self.hands[player][id_hand]
        bet = hand.bet

        split_hand_1 = Hand()
        split_hand_1.hand["history"] = ["split"]
        split_hand_1.bet = bet
        split_hand_1.add_card(hand.get_card(0))
        self.dealer_give_card(split_hand_1)

        split_hand_2 = Hand()
        split_hand_2.hand["history"] = ["split"]
        split_hand_2.bet = bet
        split_hand_2.add_card(hand.get_card(1))
        self.dealer_give_card(split_hand_2)

        self.hands[player][id_hand] = split_hand_1
        self.hands[player].append(split_hand_2)

    def check_bet(self, id_player: int, bet: int) -> bool:
        """Checks if the player has enough chips to bet."""
        player = self.players[id_player]
        if bet > player.chips:
            return False
        return True

    def next(self) -> None:
        """Sets the starting parameters for the table."""
        self.dealer.restart()
        for player in self.players:
            self.hands[player] = [Hand()]

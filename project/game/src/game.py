from project.game.src.objects import HandStates, Card, Hand
from project.game.src.persons import Player
from project.game.src.strategies import Action
from project.game.src.desk import Desk
from enum import Enum


def show_hand_player(hand: Hand, id_player: int) -> None:
    print(f"Player {id_player + 1}'s hand:")
    hand.show_hand()


class GameStates(Enum):
    """Enum to indicate the state of the game."""

    START = "The round has begun"
    PLACE_BETS = "Bets have been placed"
    DEALER_START = "The dealer took a closed and an open card"
    TOOK_CARDS = "The players took the cards"
    DEALER_SECOND_CARD = "The dealer opens the second card"
    DEALER_PLAY = "The dealer takes the cards"
    RESULTS = "The results of the game are summarized"
    END = "The round is over"


class Game:
    """
    The controller class for the game table.
    It contains information about the players,
    the current state of the game and the game table.

    Methods:
    -------
    `show_state() -> None`:
        The method of displaying information depending on the current state of the game.

    `start_game() -> None`:
        Sets the initial parameters before starting the game.

    `place_bets() -> None`:
        The players place their first bets.

    `dealer_start() -> None`:
        The dealer starts the game.

    `take_cards() -> None`:
        The players take the cards according to the strategy.

    `dealer_second_card() -> None`:
        The dealer opens the second card.

    `dealer_play() -> None`:
        The dealer takes the missing cards.

    `round_results() -> None`:
        The results of the game are summarized.

    `end_round() -> None`:
        Completes the round.

    `play_with_player(id_player: int, dealer_card: Card) -> bool`:
        Player takes the cards depending on the strategy.

    `get_state() -> GameStates`:
        Returns the game state.

    `play_steps(num_steps: int = 8) -> None`:
        Performs the first n steps of the game.
    """

    def __init__(
        self, players: list[Player], dealer_num_deck: int = 1
    ) -> None:
        """Initializing a Game object"""
        self._desk = Desk(players, dealer_num_deck)
        self._num_round = 0
        self._round_state = GameStates.START

    def show_state(self) -> None:
        """The method of displaying information depending on the current state of the game."""
        print(self._round_state.value)
        match self._round_state:
            case GameStates.START:
                print("Round:", self._num_round)
            case GameStates.PLACE_BETS:
                for id_player, player in enumerate(self._desk.players):
                    self._desk.hands[player][0].show_bet(id_player)
            case GameStates.TOOK_CARDS:
                for id_player, player in enumerate(self._desk.players):
                    if (
                        self._desk.hands[player][0].get_state()
                        is HandStates.OUT
                    ):
                        continue
                    for hand in self._desk.hands[player]:
                        show_hand_player(hand, id_player)
                        hand.show_history()
                    print()
            case GameStates.RESULTS:
                for id_player, player in enumerate(self._desk.players):
                    if (
                        self._desk.hands[player][0].get_state()
                        is HandStates.OUT
                    ):
                        continue
                    print(f"The result of player {id_player + 1}")
                    for hand in self._desk.hands[player]:
                        show_hand_player(hand, id_player)
                        hand.show_history()
                        hand.show_state()
                    print()
            case GameStates.DEALER_START:
                print("The dealer's first card:")
                print(self._desk.dealer.hand.get_card(0))
            case GameStates.DEALER_PLAY:
                self._desk.dealer.show_hand()
            case GameStates.DEALER_SECOND_CARD:
                self._desk.dealer.show_hand()
        print("\n")

    def start_game(self) -> None:
        """Sets the initial parameters before starting the game."""
        self._round_state = GameStates.START
        self._num_round += 1
        self._desk.next()

    def place_bets(self) -> None:
        """The players place their first bets."""
        self._round_state = GameStates.PLACE_BETS
        self._desk.place_first_bets()

    def dealer_start(self) -> None:
        """The dealer took a closed and an open card."""
        self._round_state = GameStates.DEALER_START
        self._desk.dealer_give_card(self._desk.dealer.hand)
        self._desk.dealer_give_card(self._desk.dealer.hand)

    def take_cards(self) -> None:
        """The players take the cards according to the strategy."""
        self._round_state = GameStates.TOOK_CARDS
        dealer_card = self._desk.dealer.hand.get_card(0)
        for id_player, player in enumerate(self._desk.players):
            player_hand = self._desk.hands[player][0]
            if not player_hand.in_playing:
                continue
            self._desk.dealer_give_card(self._desk.hands[player][0])
            self._desk.dealer_give_card(self._desk.hands[player][0])

            if player_hand.check_blackjack():
                player_hand._state = HandStates.BLACKJACK
            if (
                player_hand.get_state() is HandStates.BLACKJACK
                and not self._desk.dealer.hand.get_card(0).name
                in {
                    "10",
                    "J",
                    "Q",
                    "K",
                    "A",
                }
            ):
                player.diff_chips(int(player_hand.get_bet() * 2.5))
                player_hand.game_over()
                continue
            elif (
                player_hand.get_state() is HandStates.BLACKJACK
                and self._desk.dealer.hand.get_card(0).name == "A"
            ):
                if player.strategy.even_money:
                    player_hand.even_money()
                    player.diff_chips(int(player_hand.get_bet() * 2))
                    player_hand.game_over()
                    continue

            while self.play_with_player(id_player, dealer_card):
                pass

    def dealer_second_card(self) -> None:
        """The dealer opens the second card."""
        self._round_state = GameStates.DEALER_SECOND_CARD
        for (id_player, player) in enumerate(self._desk.players):
            for id_hand, hand in enumerate(self._desk.hands[player]):
                if not hand.in_playing:
                    continue

                if (
                    hand.get_state() is HandStates.BLACKJACK
                    and not self._desk.dealer.hand.get_state()
                    is HandStates.BLACKJACK
                ):
                    player.diff_chips(int(hand.get_bet() * 2.5))
                    hand.game_over()
                elif (
                    not hand.get_state() is HandStates.BLACKJACK
                    and self._desk.dealer.hand.get_state()
                    is HandStates.BLACKJACK
                ):
                    hand._state = HandStates.LOSE
                    hand.game_over()

    def dealer_play(self) -> None:
        """The dealer takes the missing cards."""
        self._round_state = GameStates.DEALER_PLAY
        while True:
            dealer_score = self._desk.dealer.hand.get_score()
            if dealer_score == -1 or dealer_score >= 17:
                break
            self._desk.dealer_give_card(self._desk.dealer.hand)

    def round_results(self) -> None:
        """The results of the game are summarized."""
        self._round_state = GameStates.RESULTS
        dealer_score = self._desk.dealer.hand.get_score()
        for (id_player, player) in enumerate(self._desk.players):
            for id_hand, hand in enumerate(self._desk.hands[player]):
                if not hand.in_playing:
                    continue

                hand_score = hand.get_score()

                if hand_score > dealer_score:
                    hand._state = HandStates.WIN
                    player.diff_chips(hand.get_bet() * 2)
                    hand.game_over()

                elif hand_score == dealer_score:
                    hand._state = HandStates.DRAWN_GAME
                    player.diff_chips(hand.get_bet())
                    hand.game_over()
                else:
                    hand._state = HandStates.LOSE
                    hand.game_over()

    def end_round(self) -> None:
        """Completes the round."""
        self._round_state = GameStates.END

    def play_with_player(self, id_player: int, dealer_card: Card) -> bool:
        """
        Player takes the cards depending on the strategy.

        Args:
            id_player (int): the index of the player in the list of players.
            dealer_card (Card): dealer's open card.

        Returns:
            result (bool): a flag indicating that the player has not finished the game.
        """
        target_player = self._desk.players[id_player]
        for id_hand, hand in enumerate(self._desk.hands[target_player]):
            if not hand.in_playing or hand.get_history()[-1] == "pass":
                continue
            while True:
                score = hand.get_score()
                if score == -1:
                    hand._state = HandStates.LOSE
                    hand.game_over()
                    break
                elif score == 21:
                    break

                action = target_player.strategy.play(hand, dealer_card)
                match action:
                    case Action.PASS:
                        hand.action_pass()
                        break

                    case Action.TAKE:
                        self._desk.dealer_give_card(hand)

                    case Action.SPLIT:
                        if not target_player.check_bet(hand.get_bet()):
                            hand.action_pass()
                            break
                        target_player.diff_chips(-hand.get_bet())
                        self._desk.split(target_player, id_hand)
                        return True

                    case Action.DOUBLE:
                        if not target_player.check_bet(hand.get_bet()):
                            self._desk.dealer_give_card(hand)
                            continue
                        target_player.diff_chips(-hand.get_bet())
                        hand.double_down()
                        self._desk.dealer_give_card(hand)

                    case Action.TRIPLING:
                        if not hand.double_bet:
                            raise ValueError(
                                "Before tripling the bets, you need to double them."
                            )
                        if not target_player.check_bet(hand.get_bet() // 2):
                            self._desk.dealer_give_card(hand)
                            continue
                        target_player.diff_chips(-hand.get_bet() // 2)
                        hand.tripling_bet()

                    case Action.SURRENDER:
                        target_player.diff_chips(hand.get_bet() // 2)
                        hand._state = HandStates.LOSE
                        hand.game_over()
                        break
        return False

    def get_state(self) -> GameStates:
        """Returns the game state."""
        return self._round_state

    def play_steps(self, num_steps: int = 8) -> None:
        """Performs the first number steps of the game."""
        if not num_steps:
            return

        self.start_game()
        num_steps -= 1
        if not num_steps:
            return

        self.place_bets()
        num_steps -= 1
        if not num_steps:
            return

        self.dealer_start()
        num_steps -= 1
        if not num_steps:
            return

        self.take_cards()
        num_steps -= 1
        if not num_steps:
            return

        self.dealer_second_card()
        num_steps -= 1
        if not num_steps:
            return

        self.dealer_play()
        num_steps -= 1
        if not num_steps:
            return

        self.round_results()
        num_steps -= 1
        if not num_steps:
            return

        self.end_round()

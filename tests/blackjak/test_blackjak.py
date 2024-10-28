from project.game.src.persons import Player
from project.game.src.objects import Card, Hand, HandStates
from project.game.src.game import Game, GameStates

import pytest

from project.game.src.strategies import Optimal1, Aggressive, Optimal2

A = Card("suit", "A")
K = Card("suit", "K")
Q = Card("suit", "Q")
J = Card("suit", "J")
ten = Card("suit", "10")
nine = Card("suit", "9")
eight = Card("suit", "8")
seven = Card("suit", "7")
six = Card("suit", "6")
five = Card("suit", "5")
four = Card("suit", "4")


@pytest.mark.parametrize(
    "players, nums_steps",
    [
        (
            [
                Player(strategy=Optimal1()),
                Player(strategy=Aggressive()),
                Player(strategy=Optimal2()),
                Player(),
            ],
            list(range(1, 9)),
        )
    ],
)
def test_game_states(players: list[Player], nums_steps: list[int]) -> None:
    states = []
    for num_step in nums_steps:
        game = Game(players)
        game.play_steps(num_step)
        states.append(game.round_state)

    assert states == [
        GameStates.START,
        GameStates.PLACE_BETS,
        GameStates.DEALER_START,
        GameStates.TOOK_CARDS,
        GameStates.DEALER_SECOND_CARD,
        GameStates.DEALER_PLAY,
        GameStates.RESULTS,
        GameStates.END,
    ]


@pytest.mark.parametrize(
    "cards1, cards2, expect_scores1, expect_scores2",
    [
        ([A, K], [J, six], {11, 21}, {16}),
        ([nine, ten], [A, A], {19}, {2, 12, 22}),
    ],
)
def test_players_hands(
    cards1: list[Card],
    cards2: list[Card],
    expect_scores1: int,
    expect_scores2: int,
) -> None:
    player_hand1 = Hand()
    player_hand2 = Hand()
    for card in cards1:
        player_hand1.add_card(card)

    assert player_hand1.get_scores() == expect_scores1

    for card in cards2:
        player_hand2.add_card(card)

    assert player_hand2.get_scores() == expect_scores2

    # Test hand data-descriptor is working correctly
    assert player_hand1.get_cards() != player_hand2.get_cards()


def test_players_chips() -> None:
    players = [
        Player(strategy=Optimal1()),
        Player(strategy=Aggressive()),
        Player(strategy=Optimal2()),
        Player(),
    ]
    game = Game(players)
    game.play_steps()

    for player in players:
        delta_chips = 0.0
        for hand in game.desk.hands[player]:
            first_bet = player.strategy.first_bet
            if hand.state is HandStates.LOSE:
                if hand.tripled_bet:
                    delta_chips -= first_bet * 3
                elif hand.double_bet:
                    delta_chips -= first_bet * 2
                else:
                    delta_chips -= first_bet
            elif hand.state is HandStates.WIN:
                if hand.tripled_bet:
                    delta_chips += first_bet * 3
                elif hand.double_bet:
                    delta_chips += first_bet * 2
                else:
                    delta_chips += first_bet
            elif hand.state is HandStates.BLACKJACK:
                dealer_hand = game.desk.dealer.hand
                first_card = dealer_hand.get_card(0)
                if (
                    dealer_hand.state is HandStates.BLACKJACK
                    and player.strategy.even_money
                    and first_card.name == "A"
                ):
                    delta_chips += first_bet
                elif not game.desk.dealer.hand.state is HandStates.BLACKJACK:
                    delta_chips += 1.5 * first_bet
        assert player.chips == 100 + int(delta_chips)

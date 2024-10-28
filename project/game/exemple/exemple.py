from project.game.src.persons import Player
from project.game.src.strategies import Aggressive, Optimal1, Optimal2
from project.game.src.game import Game


def play_round(game: Game) -> None:
    game.start_game()
    game.show_state()

    game.place_bets()
    game.show_state()

    game.dealer_start()
    game.show_state()

    game.take_cards()
    game.show_state()

    game.dealer_second_card()
    game.show_state()

    game.dealer_play()
    game.show_state()

    game.round_results()
    game.show_state()

    game.end_round()
    game.show_state()


players = [
    Player(strategy=Optimal1()),
    Player(strategy=Optimal2()),
    Player(strategy=Aggressive()),
]
blackjack = Game(players)
play_round(blackjack)
play_round(blackjack)

from enum import Enum
from project.game.src.objects import Hand
from project.game.src.objects import Card


class Action(Enum):
    """Enumeration for actions taken by the player."""

    PASS = 1
    TAKE = 2
    SPLIT = 3
    DOUBLE = 4
    TRIPLING = 5
    SURRENDER = 6


class Strategy:
    """
    Parent class for strategies

    Methods:
    ______
    'play(player_hand: Hand, dealer_card: Card) -> Action':
        The method responsible for taking action in a specific situation.
    """

    first_bet = 10
    even_money = False

    def play(self, player_hand: Hand, dealer_card: Card) -> Action:
        """
        The method responsible for taking action in a specific situation.

        Args:
            player_hand (Hand): the hand of the player making the decision.
            dealer_card (Card): the dealer's card that the players see.

        Results:
            return (Action): the action taken by the player.
        """
        raise NotImplementedError("Subclass must implement play method")


class Basic(Strategy):
    def __init__(self) -> None:
        self.even_money = True

    def play(self, player_hand: Hand, dealer_card: Card) -> Action:
        score = player_hand.get_score()
        if score < 17:
            return Action.TAKE
        return Action.PASS


class Optimal1(Strategy):
    def play(self, player_hand: Hand, dealer_card: Card) -> Action:
        score = player_hand.get_score()
        cards = player_hand.get_cards()
        dealer_card_name = dealer_card.name

        split_res = check_split(cards, dealer_card.name)
        if not split_res is None:
            return split_res

        double_res = check_double(score, dealer_card_name)
        if not double_res is None and not player_hand.double_bet:
            return double_res

        if "A" in set(card.name for card in cards) and len(cards) == 2:
            soft_hands = check_soft_hands(score - 10, dealer_card_name)
            if not soft_hands is None:
                return soft_hands

        steady_hand = check_steady_hands(score, dealer_card_name)
        if not steady_hand is None:
            return steady_hand

        if score >= 17:
            return Action.PASS
        return Action.TAKE


class Aggressive(Strategy):
    def __init__(self) -> None:
        self.first_bet = 20

    def play(self, player_hand: Hand, dealer_card: Card) -> Action:
        score = player_hand.get_score()
        dealer_card_name = dealer_card.name

        if score <= 6:
            return Action.DOUBLE

        double_res = check_double(score, dealer_card_name)
        if not double_res is None and player_hand.double_bet:
            return Action.TRIPLING

        if score > 19:
            return Action.PASS
        return Action.TAKE


class Optimal2(Strategy):
    def play(self, player_hand: Hand, dealer_card: Card) -> Action:
        score = player_hand.get_score()
        cards = player_hand.get_cards()
        dealer_card_name = dealer_card.name

        split_res = check_split(cards, dealer_card_name)
        if not split_res is None:
            return split_res

        if not dealer_card_name in {"10", "J", "Q", "K", "A"}:
            if score in {11, 10}:
                return Action.DOUBLE
            elif score <= 16:
                return Action.TAKE
        elif score <= 16:
            return Action.TAKE

        if score >= 17:
            return Action.PASS
        return Action.TAKE


def check_split(cards: list[Card], dealer_card_name: str) -> Action | None:
    """
    The function checks whether it is worth doing a split.

    Args:
        cards (list[Card]): the cards are in the player's hand.
        dealer_card_name (str): the dealer's open card.

    Returns:
        result (Action | None): the action taken.
    """
    if len(cards) != 2:
        return None
    if cards[1].name == cards[0].name:
        match cards[0].name:
            case "A" | "8":
                if dealer_card_name != "A":
                    return Action.SPLIT
                return Action.TAKE
            case "5":
                return Action.DOUBLE

            case "4":
                if dealer_card_name in {"2", "3", "4", "5", "6"}:
                    return Action.SPLIT
            case "9":
                if dealer_card_name in {"7", "10", "11"}:
                    return Action.PASS
                return Action.SPLIT
            case "6":
                if dealer_card_name in {"2", "3", "4", "5", "6"}:
                    return Action.SPLIT
                return Action.TAKE
            case "2" | "3" | "7":
                if dealer_card_name in {"2", "3", "4", "5", "6", "7"}:
                    return Action.SPLIT
                return Action.TAKE
    return None


def check_double(score: int, dealer_card_name: str) -> Action | None:
    """
    A function that checks whether it is worth doubling the bet.

    Args:
        score (int): the player's current score.
        dealer_card_name (str): the dealer's open card.

    Returns:
        result (Action | None): the action taken.
    """
    match score:
        case 9:
            if dealer_card_name in {"2", "3", "4", "5", "6"}:
                return Action.DOUBLE
            return Action.TAKE
        case 10 | 11:
            if dealer_card_name != "A":
                if score == 11 or dealer_card_name in {"10", "J", "Q", "K"}:
                    return Action.DOUBLE
            return Action.TAKE
    return None


def check_soft_hands(score: int, dealer_card_name: str) -> Action | None:
    """
    The decision-making function for a soft hand.

    Args:
        score (int): the player's current score.
        dealer_card_name (str): the dealer's open card.

    Returns:
        result (Action | None): the action taken.
    """
    match score:
        case 3 | 4 | 5 | 6 | 7:
            if dealer_card_name in {"2", "3", "4", "5", "6"}:
                return Action.DOUBLE
            return Action.TAKE
        case 8:
            if dealer_card_name in {"9", "10", "J", "Q", "K", "A"}:
                return Action.TAKE
            return Action.PASS
        case 9 | 10 | 11:
            return Action.PASS
    return None


def check_steady_hands(score: int, dealer_card_name: str) -> Action | None:
    """
    The decision-making function for a steady hand.

    Args:
        score (int): the player's current score.
        dealer_card_name (str): the dealer's open card.

    Returns:
        result (Action | None): the action taken.
    """
    match score:
        case 4 | 5 | 6 | 7 | 8:
            return Action.TAKE

        case 12 | 13 | 14 | 15 | 16:
            if dealer_card_name in {"2", "3", "4", "5", "6"}:
                return Action.PASS
            return Action.TAKE

        case 17 | 18 | 19 | 20 | 21:
            return Action.PASS
    return None

"""Player model for the poker table."""

from __future__ import annotations

from dataclasses import dataclass, field

from cards import Card

@dataclass
class Player:
    name: str
    # TODO: Task 1 - add chips, is_human, hole_cards, current_bet, and folded
    chips: int
    is_human: bool = False 
    hole_cards: list[Card] = field(default_factory=list)
    current_bet: int = 0
    folded: bool = False

    def reset_for_hand(self) -> None:
        # TODO: Task 2 - reset the player's state for a new hand
        self.hole_cards.clear()
        self.current_bet = 0
        self.folded = False
        pass

    def receive(self, cards: list[Card]) -> None:
        # TODO: Task 3 - add the received cards to the player's hole cards
        self.hole_cards.extend(cards)
        pass

    def bet(self, amount: int) -> int:
        # TODO: Task 4 - check if the player has enough chips to bet the specified amount, 
        # and if so, deduct the amount from the player's chips and add it to the current bet
        if amount < 0:
            raise ValueError
        
        wager = min(amount, self.chips)

        self.chips -= wager
        self.current_bet += wager

        return wager

    @property
    def active(self) -> bool:
        # TODO: Task 5 - return True if the player is still active in the hand
        return not self.folded and self.chips > 0

    def all_in(self) -> None:
        wager = self.chips
        self.chips -= wager
        self.current_bet += wager

    total_winnings: int = 0
    hands_played: int = 0
    hands_won: int = 0

    def record_hand_played(self) -> None:
        """Increment the number of hands played."""
        self.hands_played += 1

    def record_win(self, amount: int) -> None:
        """
        Record a win, award chips, and update statistics.
        """
        self.chips += amount
        self.total_winnings += amount
        self.hands_won += 1

    @property
    def win_rate(self) -> float:
        """
        Return the player's win rate as a percentage.
        """
        if self.hands_played == 0:
            return 0.0
        return (self.hands_won / self.hands_played) * 100

    def __repr__(self) -> str:
        return (
            f"Player(name={self.name}, chips={self.chips}, "
            f"hands_won={self.hands_won}, "
            f"hands_played={self.hands_played}, "
            f"total_winnings={self.total_winnings})"
        )

# table.py
"""Shared table state for a Hold'em hand."""

from __future__ import annotations

from dataclasses import dataclass, field

from cards import Card

@dataclass
# TODO: Task 1 - implement the Table class 
class Table:
    community_cards: list[Card] = field(default_factory=list)
    pot: int = 0

    def reset(self) -> None:
        self.community_cards.clear()
        self.pot = 0
    # TODO: Task 2 - create and implement the method reset(self) -> None 
    def add_to_pot(self, amount: int) -> None:
        if amount < 0:
            raise ValueError
        self.pot += amount
    # TODO: Task 3 - create and implement the method add_to_pot(self, amount: int) -> None
    pass

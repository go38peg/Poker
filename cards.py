# cards.py
"""Card and deck primitives for Texas Hold'em."""


from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from random import shuffle


class Suit(IntEnum):
    CLUBS = 0
    # TODO: Task 1 - continue here
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3
    @property
    def symbol(self) -> str:
        return {
            Suit.CLUBS: "C",
            Suit.DIAMONDS: "D",
            Suit.HEARTS: "H",
            Suit.SPADES: "S"
            # TODO: Task 1 - map each Suit to its one-letter symbol
        }[self]


class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    # TODO: Task 2 - continue until ACE = 14

    @property
    def label(self) -> str:
        return {
            Rank.TWO: "2",
            Rank.THREE: "3",
            Rank.FOUR: "4",
            Rank.FIVE: "5",
            Rank.SIX: "6",
            Rank.SEVEN: "7",
            Rank.EIGHT: "8",
            Rank.NINE: "9",
            Rank.TEN: "T",
            Rank.JACK: "J",
            Rank.QUEEN: "Q",
            Rank.KING: "K",
            Rank.ACE: "A",
            # TODO: Task 2 - continue the mapping
        }[self]

@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit
    # TODO: Task 3 - continue here

    def __str__(self) -> str:
        # TODO: Task 3 - return a string representation of the card, e.g. "AH" for Ace of Hearts
        return f"{self.rank.label}{self.suit.symbol}"

class Deck:
    
    def __init__(self) -> None:
        self._cards = []
        for rank in Rank: 
          for suit in Suit: 
            self._cards.append(Card(rank, suit))
            # create every Card(rank, suit) combination
            
            # TODO: Task 4 - initialize the deck with all 52 cards
        shuffle(self._cards)

    def draw(self, count: int = 1) -> list[Card]:
        if count < 1:
            raise ValueError("count must be at least 1")
        if count > len(self._cards):
            raise ValueError("count must be at most number of remaining cards")
        return [self._cards.pop() for _ in range(count)]

    def remaining(self) -> int:
        return len(self._cards)

    #def reset(self) -> None:
    #    shuffle(self._cards) # remaining 50 cards are shuffled again (we are not sure about what is asked)

    def reset(self) -> None:
        self._cards = [
            Card(rank, suit)
            for rank in Rank
            for suit in Suit
        ]
        shuffle(self._cards) # if the whole deck should be reset to all 52 cards and shuffled again

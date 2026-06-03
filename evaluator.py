"""Five-card hand evaluator used to rank Texas Hold'em showdowns."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations
from typing import Tuple 

from cards import Card


class HandCategory(IntEnum):
    # TODO: Task 1 - define the hand categories in order from lowest to highest
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 4
    FLUSH = 5
    FULL_HOUSE = 6
    FOUR_OF_A_KIND = 7
    STRAIGHT_FLUSH = 8

@dataclass(frozen=True, order=True)
class HandRank:
    # TODO: Task 2 - define the HandRank dataclass with the category and tiebreakers
    category: HandCategory
    tiebreakers: Tuple[int, ...]

    # TODO: Task 2 - return a version of the category
    def get_category(self) -> str:
        return self.category.name.replace("_", " ").title()

class HandEvaluator:
    # TODO: Task 3 - implement the best_rank method to evaluate the best possible hand from a list of cards
    def best_rank(self, cards: list[Card]) -> HandRank:
        if len(cards) < 5:
            raise ValueError
        possible_hands = combinations(cards, 5)
        all_ranks = [self._rank_five(list(combo)) for combo in possible_hands]
        return max(all_ranks)

    # Indented these two methods inside HandEvaluator so 'self' works correctly
    def _rank_five(self, cards: list[Card]) -> HandRank:
        # TODO: Task 4 – implement the logic to rank a five-card hand according to poker rules
        ranks = sorted([card.rank for card in cards], reverse=True)
        counts = Counter(ranks)
        groups = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        is_flush = len(set(card.suit for card in cards)) == 1
        
        # Call the Task 5 helper method here!
        straight_high = self._straight_high(ranks)

        # TODO: Task 6 – implement the ranking logic
        # NOTE: this is a hard task – ranking logic implemented in problem #6
        if is_flush and straight_high:
            return HandRank(HandCategory.STRAIGHT_FLUSH, (straight_high,))
        if groups[0][1] == 4:
            return HandRank(HandCategory.FOUR_OF_A_KIND, (groups[0][0], groups[1][0]))
        if groups[0][1] == 3 and groups[1][1] == 2:
            return HandRank(HandCategory.FULL_HOUSE, (groups[0][0], groups[1][0]))
        if is_flush:
            return HandRank(HandCategory.FLUSH, tuple(ranks))
        if straight_high:
            return HandRank(HandCategory.STRAIGHT, (straight_high,))
        if groups[0][1] == 3:
            return HandRank(HandCategory.THREE_OF_A_KIND, (groups[0][0], groups[1][0], groups[2][0]))
        if groups[0][1] == 2 and groups[1][1] == 2:
            return HandRank(HandCategory.TWO_PAIR, (groups[0][0], groups[1][0], groups[2][0]))
        if groups[0][1] == 2:
            return HandRank(HandCategory.ONE_PAIR, (groups[0][0], groups[1][0], groups[2][0], groups[3][0]))
        return HandRank(HandCategory.HIGH_CARD, tuple(ranks))

    def _straight_high(self, ranks: list[int]) -> int | None:
        # TODO: Task 5 – implement the logic to determine if the hand contains a straight,
        # and if so, return the high card of the straight
        if len(set(ranks)) == 5 and (ranks[0] - ranks[4] == 4):
            return ranks[0]
        elif ranks == [14, 5, 4, 3, 2]:
            return 5
        else:
            return None

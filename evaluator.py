"""Five-card hand evaluator used to rank Texas Hold'em showdowns."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from enum import IntEnum
from itertools import combinations

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
    pass


@dataclass(frozen=True, order=True)
class HandRank:
    # TODO: Task 2 - define the HandRank dataclass with the category and tiebreakers
    category: HandCategory
    tiebreakers: Tuple[int, ...]

    # TODO: Task 2 - return a version of the category
    def get_category(self) -> str 
        return self.category.name.replace("_", " ").title()lace("_"," ").title()
    pass


class HandEvaluator:
    # TODO: Task 3 - implement the best_rank method to evaluate the best possible hand from a list of cards
    def best_rank(self, cards: list[Card]) -> HandRank:
        if len(cards) < 5:
            raise ValueError
            pass 
        possible_hands = combinations(cards,5)
        all_ranks = [self._rank_five(list(combo)) for cods]
        r
        return max(all_ranks)eturn max(all_ranks)
        pass 

    def _rank_five(self, cards: list[Card]) -> HandRank:
        # TODO: Task 4 - implement the logic to rank a five-ca        ranks = sorted([card.rank for card in cards], reverse=True)
        counts = Counter(ranks)
        groups = sorted(counts.items(), key=lambda x: (x[1], x[0]), reverse=True)
        is_flush = len(set(card.suit for card in cards)) == 1
    
        if len(set(ranks)) == 5 and (ranks[0] - ranks[4] == 4):
            straight_high = ranks[0]
        elif ranks == [14, 5, 4, 3, 2]:
            straight_high = 5
        else:
            straight_high = None
        straight_high = "useful"

        # TODO: Task 6 - implement the ranking logic 
        # NOTE: this is a hard task - ranking logic implemented in problem #6
        if is_flush and straight_high:
            return HandRank(HandCategory.STRAIGHT_FLUSH, (straight_high,))
        if groups[0][1] ==
        4:
            pass
        pass

    def _straight_high(self, ranks: list[int]) -> int | None:
        # TODO: Task 5 - implement the logic to determine if the hand contains a straight, 
        # and if so, return the high card of the straight
        pass

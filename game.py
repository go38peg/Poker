"""Main Texas Hold'em game loop."""

from __future__ import annotations

from cards import Deck
from evaluator import HandEvaluator
from player import Player
from table import Table
from ui import ConsoleUI
# The assignment said that leading dots infront of import source are supposed to indicate that all imports come from the same package, 
# but the dots were not included in the template on github.


class TexasHoldemGame:
    def __init__(self, players: list[Player], small_blind: int = 5, big_blind: int = 10) -> None:
        # TODO: Task 1 - check that there are at least 2 players, and if so, 
        # initialize the game state with the players, blinds, table, hand evaluator, and UI
        if len(players) < 2:
            raise ValueError("At least 2 players are required")
        
        self.players = players
        self.small_blind = small_blind
        self.big_blind = big_blind

        self.table = Table()
        self.evaluator = HandEvaluator()
        self.ui = ConsoleUI()

        pass


    def play_hand(self) -> None:
        # TODO: Task 2 - implement the main game loop for a single hand of Texas Hold'em, following the 
        # standard sequence of actions (create new Deck, reset table, reset all players, deal two cards to each player, 
        # post blinds, deal (flop, turn, river), run betting rounds, and showdown)
        # NOTE: many of these actions are custom methods
        
        #  # Creates a fresh shuffled deck for this hand
        deck = Deck()

        # Clears the table state from the previous hand
        self.table.reset()

         # Resets every player for the new hand
        for player in self.players:
            player.reset_for_hand()

        # Deals two private (hole) cards
        for player in self.players:
            player.receive(deck.draw(2))

        # The first two players pay the blinds, this creates the initial pot
        self._post_blinds()

        # First betting round (before any community cards are shown)
        self._betting_round("Pre-Flop")

        self._deal_community(deck, 3, "Flop") # Deals the flop
        self._betting_round("Flop") # Second betting round

        self._deal_community(deck, 1, "Turn") # Deals the turn
        self._betting_round("Turn") # Third betting round

        self._deal_community(deck, 1, "River") # Deals the river
        self._betting_round("River") # Fourth and final betting round

        self._showdown() # Determines the winner and awards the pot
        pass

    def _post_blinds(self) -> None:
        # TODO: Task 3 - have the first two players post the small and big blinds, 
        # respectively, add those amounts to the pot, 
        # and display the message as "[name] posts [small]; [name] posts [big]"
        
        # First player posts the small blind
        small_player = self.players[0]
        small_wager = small_player.bet(self.small_blind)
        self.table.add_to_pot(small_wager)

        # Second player posts the big blind
        big_player = self.players[1]
        big_wager = big_player.bet(self.big_blind)
        self.table.add_to_pot(big_wager)

        # Displays the required message
        self.ui.show_message(
            f"{small_player.name} posts {small_wager}; "
            f"{big_player.name} posts {big_wager}"
        )
        pass

    def _show_human_cards(self) -> None:
        # TODO: Task 4 - display the hole cards of all human players, e.g. "Alice: AH KH"
        
        # Checks every player at the table
        for player in self.players:

            # Only shows cards for human players
            if player.is_human:

                # Displays name followed by hole cards
                self.ui.show_message(
                    f"{player.name}: {self.ui.format_cards(player.hole_cards)}"
                )
        pass

    def _deal_community(self, deck: Deck, count: int, street: str) -> None:
        # TODO: Task 5 - stop if one player remains, deal the specified number of community 
        # cards from the deck, add them to the table, and display the message as "\n-- [Street] --"
        # HINT: use the extend method of the list to add the new cards to the existing community cards
        
        # Stops if only one player remains
        if self._only_one_player_left():
            return
        
        # Deals the specified number of community cards from the deck and adds them to the table
        self.table.community_cards.extend(deck.draw(count))

        # Displays the current street name
        self.ui.show_message(f"\n-- {street} --")
        pass

    def _betting_round(self, street: str) -> None:
        # TODO: Task 6 - implement the betting round for the specified street, where each 
        # active player can choose to fold, call, or raise -> ensure that each action works
        # NOTE: this is a big task

        # Highest amount any player has committed this round
        current_bet = max(player.current_bet for player in self.players)
        
        for player in self.players:
            if player.folded:
                continue # Skips folded players
        
            # Amount needed to match the highest bet
            call_amount = current_bet - player.current_bet
        
            # Asks the player what they want to do
            action = self.ui.ask_action(player, call_amount)

            # Fold
            if action == "fold":
                player.folded = True

            # Call or check
            elif action in ("call", "check"):
                wager = player.bet(call_amount)
                self.table.add_to_pot(wager)

            # Raise
            elif action == "raise":
                raise_amount = self.ui.ask_raise_amount(
                    1, # min raise is 1 more than the current bet
                    player.chips # max raise is all the player's remaining chips
                )

                wager = player.bet(call_amount + raise_amount)
                self.table.add_to_pot(wager)

                current_bet = player.current_bet

        # Round is over, resets bets
        for player in self.players:
            player.current_bet = 0

        pass

    def _bot_action(self, player: Player, call_amount: int) -> str:
        # TODO: Task 7 - implement a simple bot strategy based on the 
        # call amount relative to the player's chips
        
        # Folds if calling would cost more than half of the bot's remaining chips
        if call_amount > player.chips / 2:
            return "fold"
        
        # Otherwise, calls
        return "call"

    def _showdown(self) -> None:
        # TODO: Task 8 - if only one player remains, they win the pot; 
        # otherwise, evaluate the hands of all active players
        # NOTE: this is a big task

        # Players who haven't folded are still active
        active_players = [player for player in self.players if not player.folded]
        
        # Automatic win if everyone else folded
        if len(active_players) == 1:
            winner = active_players[0]

            winner.chips += self.table.pot

            self.ui.show_message(
                f"{winner.name} wins {self.table.pot} chips"
            )
            return

        # Evaluates each active player's hand
        player_ranks = []

        for player in active_players:
            cards = (player.hole_cards + self.table.community_cards)

            rank = self.evaluator.best_rank(cards)

            player_ranks.append((player, rank))

        # Finds the best hand
        best_rank = max(rank for _, rank in player_ranks)

        # Finds all players who share that hand rank
        winners = [
            player
            for player, rank in player_ranks
            if rank == best_rank
        ]

         # Splits the pot among winners
        share = self.table.pot // len(winners) #remainder is ignored for simplicity

        for winner in winners:
            winner.chips += share

        # Displays results
        winner_names = ", ".join(
            winner.name for winner in winners
        )

        self.ui.show_message(
            f"{winner_names} win(s) {share} chips each"
        )

        self.ui.show_message(
            f"Winning hand: {best_rank.get_category()}"
        )

    def _only_one_player_left(self) -> bool:
        # TODO: Task 9 - return True if only one player is still active and False otherwise

        # Finds all players who are still active
        active_players = [
            player for player in self.players
            if not player.folded
        ]

        # True if exactly one active player remains
        return len(active_players) == 1

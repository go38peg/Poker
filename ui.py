"""Console input/output helpers."""

from __future__ import annotations

from cards import Card
from player import Player


class ConsoleUI: 
    def show_table(self, community_cards: list[Card], pot: int) -> None:
        # TODO: Task 1 - display the current state of the table, including the community cards and the pot size.
        # If there are no community cards, indicate that the board is empty.
        print(f"Board: {'(empty)' if not community_cards else ' '.join(str(card) for card in community_cards)}")
        print(f"Pot: {pot}")

    def show_player(self, player: Player) -> None:
        # TODO: Task 2 - display the player's name, hole cards, and chip count in a clear format.
        print(f"Player: {player.name}")
        print(f"Cards: {self.format_cards(player.hole_cards)}")
        print(f"Chips: {player.chips}")
        pass
    
    def ask_action(self, player: Player, call_amount: int) -> str:
        # TODO: Task 3 - prompt the player to choose an action (call/check, raise, or fold).
        # TODO: Task 3 - match the player's input to the corresponding action, 
        # and return a string indicating the chosen action.
        while True:
            if call_amount > 0:
                action = input(
                    f"{player.name}, choose an action "
                    "(c/call, r/raise, f/fold): "
                ).strip().lower()

                if action in {"c", "call"}:
                    return "call"
            else:
                action = input(
                    f"{player.name}, choose an action "
                    "(c/check, r/raise, f/fold): "
                ).strip().lower()

                if action in {"c", "check"}:
                    return "check"

            if action in {"r", "raise"}:
                return "raise"

            if action in {"f", "fold"}:
                return "fold"

            print("Invalid action. Please enter call/check, raise, or fold.")
            pass 

    def ask_raise_amount(self, minimum: int, maximum: int) -> int:
        # TODO: Task 4 - prompt the player to enter a raise amount, 
        # ensuring that it is a valid integer within the specified range.
        while True:
            raw = input(f"Enter raise amount ({minimum}-{maximum}): ").strip()

            try:
                amount = int(raw)
            except ValueError:
                print("Please enter a valid integer.")
                continue

            if minimum <= amount <= maximum:
                return amount

            print(f"Amount must be between {minimum} and {maximum}.")
            pass

    def show_message(self, message: str) -> None:
        # TODO: Task 5 - display a message to the player
        print(message)
        pass
    
    def format_cards(self, cards: list[Card]) -> str:
        # TODO: Task 6 - convert a list of Card objects into a string representation
        pass
        return " ".join(str(card) for card in cards)

    #feature: leaderboard system
    def show_leaderboard(self, players: list[Player]) -> None:
        print("\n===== LEADERBOARD =====")

        ranked_players = sorted(
            players,
            key=lambda p: p.total_winnings,
            reverse = True
        )

        for position, player in enumerate(ranked_players, start=1):
            print(
                f"{position}. "
                f"{player.name} | "
                f"Wins: {player.hands_won} | "
                f"Played: {player.hands_played} | "
                f"Win Rate: {player.win_rate:.1f}% | " 
                f"Total Winnings: {player.total_winnings}" 
            )
            
        print("=======================\n")

"""Run the CLI Texas Hold'em starter game."""

from game import TexasHoldemGame
from player import Player


def main() -> None:
    players = [
        Player("You", chips=1_000, is_human=True),
        Player("Ada Bot", chips=1_000),
        Player("Grace Bot", chips=1_000),
    ]
    game = TexasHoldemGame(players)

    for _ in range(5):
        game.play_hand()

    game.show_leaderboard()


if __name__ == "__main__":
    main()


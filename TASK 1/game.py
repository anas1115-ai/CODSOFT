"""
game.py — Tic-Tac-Toe: Human vs AI
=====================================
Entry point.  Handles the game loop, user input,
score tracking, and clean terminal output.

Run with:
    python game.py               # Alpha-Beta Pruning (default)
    python game.py --no-pruning  # Plain Minimax (slower, same result)

Author : Your Name
Date   : 2026-04-28
Python : 3.10+
"""

from __future__ import annotations

import argparse
import sys
import time

from board import Board
from ai    import TicTacToeAI


# ---------------------------------------------------------------------------
# Terminal colour helpers (works on Linux / macOS / Windows 10+)
# ---------------------------------------------------------------------------

class Color:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    CYAN   = "\033[96m"
    DIM    = "\033[2m"

def c(text: str, *codes: str) -> str:
    """Wrap text in ANSI escape codes."""
    return "".join(codes) + text + Color.RESET


# ---------------------------------------------------------------------------
# Input helpers
# ---------------------------------------------------------------------------

def parse_move(user_input: str) -> tuple[int, int] | None:
    """
    Accept moves like 'A1', 'b2', 'C 3', '1 A', etc.
    Returns (row, col) with 0-based indices, or None if unparsable.
    """
    token = user_input.strip().upper().replace(" ", "")
    if len(token) != 2:
        return None

    # 'A1' style
    if token[0] in "ABC" and token[1] in "123":
        row = "ABC".index(token[0])
        col = int(token[1]) - 1
        return row, col

    # '1A' style (reversed)
    if token[0] in "123" and token[1] in "ABC":
        col = int(token[0]) - 1
        row = "ABC".index(token[1])
        return row, col

    return None


def ask_yes_no(prompt: str) -> bool:
    """Ask a yes/no question, keep asking until we get a clear answer."""
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("  Please type y or n.")


def choose_mark() -> str:
    """Let the human choose X or O."""
    while True:
        choice = input(c("\n  Do you want to play as X or O? ", Color.CYAN)).strip().upper()
        if choice in ("X", "O"):
            return choice
        print("  Please enter X or O.")


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

BANNER = r"""
  ████████╗██╗ ██████╗    ████████╗ █████╗  ██████╗    ████████╗ ██████╗ ███████╗
     ██╔══╝██║██╔════╝       ██╔══╝██╔══██╗██╔════╝       ██╔══╝██╔═══██╗██╔════╝
     ██║   ██║██║            ██║   ███████║██║            ██║   ██║   ██║█████╗  
     ██║   ██║██║            ██║   ██╔══██║██║            ██║   ██║   ██║██╔══╝  
     ██║   ██║╚██████╗       ██║   ██║  ██║╚██████╗       ██║   ╚██████╔╝███████╗
     ╚═╝   ╚═╝ ╚═════╝       ╚═╝   ╚═╝  ╚═╝ ╚═════╝       ╚═╝    ╚═════╝ ╚══════╝
                               [ Human  vs  AI ]
"""

def print_banner():
    print(c(BANNER, Color.CYAN, Color.BOLD))

def print_board(board: Board):
    print()
    print(str(board))
    print()

def print_scores(human_wins: int, ai_wins: int, draws: int):
    print(
        c(f"  You: {human_wins}", Color.GREEN) + "  |  " +
        c(f"  AI: {ai_wins}", Color.RED)  + "  |  " +
        c(f" Draws: {draws}", Color.DIM)
    )
    print()


# ---------------------------------------------------------------------------
# Single game
# ---------------------------------------------------------------------------

def play_game(
    board: Board,
    ai: TicTacToeAI,
    human_mark: str,
    ai_mark: str,
) -> str:
    """
    Play one full game.
    Returns 'human', 'ai', or 'draw'.
    """
    board.reset()
    current_mark = "X"        # X always goes first

    while not board.is_game_over():

        print_board(board)

        if current_mark == human_mark:
            # ── Human turn ──────────────────────────────────────────────
            print(c(f"  Your turn ({human_mark}). ", Color.YELLOW) +
                  c("Enter a cell (e.g. A1, B2, C3): ", Color.DIM))

            while True:
                raw = input("  > ").strip()
                if raw.lower() in ("q", "quit", "exit"):
                    print(c("\n  Game abandoned.\n", Color.DIM))
                    sys.exit(0)

                move = parse_move(raw)
                if move is None:
                    print(c("  ✗  Bad format. Try something like A1 or C3.", Color.RED))
                    continue

                row, col = move
                if not board.is_valid_move(row, col):
                    print(c("  ✗  That cell is already taken!", Color.RED))
                    continue

                board.make_move(row, col, human_mark)
                break

        else:
            # ── AI turn ─────────────────────────────────────────────────
            print(c(f"  AI is thinking ({ai_mark})…", Color.CYAN))
            time.sleep(0.4)          # Tiny pause so it feels natural

            row, col = ai.best_move(board, ai_mark)
            board.make_move(row, col, ai_mark)

            label = board.cell_label(row, col)
            print(c(f"  AI plays {label}  "
                    f"(evaluated {ai.nodes_evaluated} nodes)", Color.DIM))

        current_mark = "O" if current_mark == "X" else "X"

    # ── Game over ────────────────────────────────────────────────────────
    print_board(board)

    winner = board.winner()
    if winner == human_mark:
        print(c("  🎉  You win!  Congratulations!", Color.GREEN, Color.BOLD))
        return "human"
    elif winner == ai_mark:
        print(c("  🤖  AI wins!  Better luck next time.", Color.RED, Color.BOLD))
        return "ai"
    else:
        print(c("  🤝  It's a draw!  Well played.", Color.YELLOW, Color.BOLD))
        return "draw"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Tic-Tac-Toe: play against an unbeatable AI."
    )
    parser.add_argument(
        "--no-pruning",
        action="store_true",
        help="Use plain Minimax instead of Alpha-Beta Pruning (slower).",
    )
    args = parser.parse_args()

    print_banner()

    use_pruning = not args.no_pruning
    algo_name   = "Minimax + Alpha-Beta Pruning" if use_pruning else "Plain Minimax"
    print(c(f"  Algorithm : {algo_name}\n", Color.DIM))

    ai = TicTacToeAI(use_pruning=use_pruning)

    human_wins = 0
    ai_wins    = 0
    draws      = 0

    while True:
        human_mark = choose_mark()
        ai_mark    = "O" if human_mark == "X" else "X"

        print(c(f"\n  You are {human_mark}. AI is {ai_mark}.", Color.BOLD))
        print(c("  (X always goes first)\n", Color.DIM))

        board  = Board()
        result = play_game(board, ai, human_mark, ai_mark)

        if result == "human":
            human_wins += 1
        elif result == "ai":
            ai_wins += 1
        else:
            draws += 1

        print()
        print_scores(human_wins, ai_wins, draws)

        if not ask_yes_no(c("  Play again? (y/n): ", Color.CYAN)):
            print(c("\n  Thanks for playing!  Goodbye 👋\n", Color.BOLD))
            break


if __name__ == "__main__":
    main()

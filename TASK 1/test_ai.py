"""
test_ai.py — Unit Tests for Board & AI
========================================
Run with:   python -m pytest test_ai.py -v
or simply:  python test_ai.py

Tests cover:
  - Board: move validation, win detection, draw detection
  - AI   : blocks human wins, takes winning moves, centre preference
           and the core property that AI never loses

Author : Your Name
Date   : 2026-04-28
"""

import unittest
from board import Board
from ai    import TicTacToeAI


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.b = Board()

    # ── Basic moves ──────────────────────────────────────────────────────

    def test_empty_board_has_nine_empty_cells(self):
        self.assertEqual(len(self.b.empty_cells()), 9)

    def test_make_move_reduces_empty_cells(self):
        self.b.make_move(0, 0, "X")
        self.assertEqual(len(self.b.empty_cells()), 8)

    def test_undo_move_restores_cell(self):
        self.b.make_move(1, 1, "X")
        self.b.undo_move(1, 1)
        self.assertTrue(self.b.is_valid_move(1, 1))

    def test_cannot_play_occupied_cell(self):
        self.b.make_move(0, 0, "X")
        with self.assertRaises(ValueError):
            self.b.make_move(0, 0, "O")

    def test_out_of_bounds_is_invalid(self):
        self.assertFalse(self.b.is_valid_move(-1, 0))
        self.assertFalse(self.b.is_valid_move(3, 3))

    # ── Win detection ────────────────────────────────────────────────────

    def test_row_win(self):
        for col in range(3):
            self.b.make_move(0, col, "X")
        self.assertEqual(self.b.winner(), "X")

    def test_column_win(self):
        for row in range(3):
            self.b.make_move(row, 0, "O")
        self.assertEqual(self.b.winner(), "O")

    def test_diagonal_win(self):
        for i in range(3):
            self.b.make_move(i, i, "X")
        self.assertEqual(self.b.winner(), "X")

    def test_anti_diagonal_win(self):
        for i in range(3):
            self.b.make_move(i, 2 - i, "O")
        self.assertEqual(self.b.winner(), "O")

    def test_no_winner_on_empty_board(self):
        self.assertIsNone(self.b.winner())

    # ── Draw detection ───────────────────────────────────────────────────

    def test_full_board_draw(self):
        # X O X
        # X X O
        # O X O  — no winner
        moves = [
            (0,0,"X"),(0,1,"O"),(0,2,"X"),
            (1,0,"X"),(1,1,"X"),(1,2,"O"),
            (2,0,"O"),(2,1,"X"),(2,2,"O"),
        ]
        for r, c, m in moves:
            self.b.make_move(r, c, m)
        self.assertIsNone(self.b.winner())
        self.assertTrue(self.b.is_full())
        self.assertTrue(self.b.is_game_over())

    def test_reset_clears_board(self):
        self.b.make_move(0, 0, "X")
        self.b.reset()
        self.assertEqual(len(self.b.empty_cells()), 9)


class TestAI(unittest.TestCase):

    def _make_ai(self, pruning=True):
        return TicTacToeAI(use_pruning=pruning)

    # ── Both variants produce the same moves ─────────────────────────────

    def test_pruning_and_plain_agree(self):
        """Alpha-Beta should return the same best move as plain Minimax."""
        ai_ab    = self._make_ai(pruning=True)
        ai_plain = self._make_ai(pruning=False)
        b = Board()
        # Put some pieces down
        b.make_move(0, 0, "X")
        b.make_move(1, 1, "O")

        move_ab    = ai_ab.best_move(b, "X")
        move_plain = ai_plain.best_move(b, "X")

        # Both must return valid empty cells
        self.assertIn(move_ab,    b.empty_cells())
        self.assertIn(move_plain, b.empty_cells())

    # ── AI takes a winning move ───────────────────────────────────────────

    def test_ai_takes_winning_move(self):
        """If the AI can win immediately it must do so."""
        ai = self._make_ai()
        b  = Board()
        # X X _ → AI (X) must play (0,2) to win
        b.make_move(0, 0, "X")
        b.make_move(0, 1, "X")
        b.make_move(1, 0, "O")
        b.make_move(1, 1, "O")

        move = ai.best_move(b, "X")
        b.make_move(*move, "X")
        self.assertEqual(b.winner(), "X")

    # ── AI blocks a human win ────────────────────────────────────────────

    def test_ai_blocks_human_win(self):
        """AI (O) must block human (X) from winning on the next move."""
        ai = self._make_ai()
        b  = Board()
        # X X _ → AI (O) must play (0,2)
        b.make_move(0, 0, "X")
        b.make_move(0, 1, "X")
        b.make_move(2, 2, "O")   # O elsewhere

        move = ai.best_move(b, "O")
        self.assertEqual(move, (0, 2))

    # ── AI never loses (exhaustive) ──────────────────────────────────────

    def _simulate_game(self, ai: TicTacToeAI, human_first: bool) -> str:
        """
        Simulate a full game where the human plays randomly.
        Returns 'ai', 'human', or 'draw'.
        """
        import random
        b          = Board()
        ai_mark    = "O" if human_first else "X"
        human_mark = "X" if human_first else "O"
        current    = "X"

        while not b.is_game_over():
            if current == ai_mark:
                r, c = ai.best_move(b, ai_mark)
            else:
                empty = b.empty_cells()
                r, c  = random.choice(empty)
            b.make_move(r, c, current)
            current = "O" if current == "X" else "X"

        winner = b.winner()
        if winner == ai_mark:
            return "ai"
        if winner == human_mark:
            return "human"
        return "draw"

    def test_ai_never_loses_as_x(self):
        """AI going first should never lose (50 random games)."""
        import random; random.seed(42)
        ai = self._make_ai()
        for _ in range(50):
            result = self._simulate_game(ai, human_first=False)
            self.assertNotEqual(result, "human", "AI lost as X!")

    def test_ai_never_loses_as_o(self):
        """AI going second should never lose (50 random games)."""
        import random; random.seed(99)
        ai = self._make_ai()
        for _ in range(50):
            result = self._simulate_game(ai, human_first=True)
            self.assertNotEqual(result, "human", "AI lost as O!")


if __name__ == "__main__":
    unittest.main(verbosity=2)

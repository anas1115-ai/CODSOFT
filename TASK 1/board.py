"""
board.py — Tic-Tac-Toe Board
=============================
Manages the 3×3 grid, move validation, win detection,
and pretty-printing.  Kept intentionally separate from
the AI so each module has one clear job.

Author : Your Name
Date   : 2026-04-28
Python : 3.10+
"""

from __future__ import annotations


# Win lines: every row, column, and diagonal
_WIN_LINES: list[list[tuple[int, int]]] = [
    # Rows
    [(0, 0), (0, 1), (0, 2)],
    [(1, 0), (1, 1), (1, 2)],
    [(2, 0), (2, 1), (2, 2)],
    # Columns
    [(0, 0), (1, 0), (2, 0)],
    [(0, 1), (1, 1), (2, 1)],
    [(0, 2), (1, 2), (2, 2)],
    # Diagonals
    [(0, 0), (1, 1), (2, 2)],
    [(0, 2), (1, 1), (2, 0)],
]


class Board:
    """
    Represents the 3×3 Tic-Tac-Toe board.

    Cells are stored as a 3×3 list of strings:
        ""   → empty
        "X"  → player X
        "O"  → player O

    Example usage
    -------------
    >>> b = Board()
    >>> b.make_move(1, 1, "X")   # centre
    >>> b.make_move(0, 0, "O")   # top-left
    >>> print(b)
    """

    EMPTY = ""

    def __init__(self):
        self.grid: list[list[str]] = [
            [self.EMPTY] * 3 for _ in range(3)
        ]

    # ------------------------------------------------------------------
    # Move management
    # ------------------------------------------------------------------

    def make_move(self, row: int, col: int, mark: str) -> None:
        """Place `mark` at (row, col).  Raises if the cell is taken."""
        if self.grid[row][col] != self.EMPTY:
            raise ValueError(f"Cell ({row}, {col}) is already occupied.")
        self.grid[row][col] = mark

    def undo_move(self, row: int, col: int) -> None:
        """Clear a cell (used by Minimax to back-track)."""
        self.grid[row][col] = self.EMPTY

    def is_valid_move(self, row: int, col: int) -> bool:
        """Return True if (row, col) is inside the grid and empty."""
        if not (0 <= row <= 2 and 0 <= col <= 2):
            return False
        return self.grid[row][col] == self.EMPTY

    # ------------------------------------------------------------------
    # State queries
    # ------------------------------------------------------------------

    def empty_cells(self) -> list[tuple[int, int]]:
        """Return a list of (row, col) tuples that are currently empty."""
        return [
            (r, c)
            for r in range(3)
            for c in range(3)
            if self.grid[r][c] == self.EMPTY
        ]

    def is_full(self) -> bool:
        """Return True when every cell is occupied."""
        return len(self.empty_cells()) == 0

    def winner(self) -> str | None:
        """
        Return the mark of the winner ("X" or "O"),
        or None if there is no winner yet.
        """
        for line in _WIN_LINES:
            marks = [self.grid[r][c] for r, c in line]
            if marks[0] != self.EMPTY and marks[0] == marks[1] == marks[2]:
                return marks[0]
        return None

    def winning_line(self) -> list[tuple[int, int]] | None:
        """Return the winning line cells, or None if no winner."""
        for line in _WIN_LINES:
            marks = [self.grid[r][c] for r, c in line]
            if marks[0] != self.EMPTY and marks[0] == marks[1] == marks[2]:
                return line
        return None

    def is_game_over(self) -> bool:
        """Return True if someone has won OR the board is full."""
        return self.winner() is not None or self.is_full()

    def reset(self) -> None:
        """Clear the board for a new game."""
        self.grid = [[self.EMPTY] * 3 for _ in range(3)]

    # ------------------------------------------------------------------
    # Display
    # ------------------------------------------------------------------

    def __str__(self) -> str:
        """
        Render the board like this:

            1   2   3
          ┌───┬───┬───┐
        A │ X │   │ O │
          ├───┼───┼───┤
        B │   │ X │   │
          ├───┼───┼───┤
        C │   │   │ O │
          └───┴───┴───┘
        """
        rows_labels = ["A", "B", "C"]
        col_header  = "    1   2   3"
        top         = "  ┌───┬───┬───┐"
        mid         = "  ├───┼───┼───┤"
        bot         = "  └───┴───┴───┘"

        lines = [col_header, top]
        for i, (label, row) in enumerate(zip(rows_labels, self.grid)):
            cells = " │ ".join(cell if cell else " " for cell in row)
            lines.append(f"{label} │ {cells} │")
            lines.append(mid if i < 2 else bot)

        return "\n".join(lines)

    def cell_label(self, row: int, col: int) -> str:
        """Human-readable label like 'A2' for (0, 1)."""
        return f"{'ABC'[row]}{col + 1}"

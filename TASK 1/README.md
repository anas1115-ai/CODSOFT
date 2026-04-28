# ♟ Tic-Tac-Toe AI

> An unbeatable Tic-Tac-Toe agent built with **Minimax + Alpha-Beta Pruning**.  
> Play it in your terminal — if you can find a way to win, you've broken mathematics.

![Python](https://img.shields.io/badge/Python-3.10%2B-3572A5?style=flat-square&logo=python&logoColor=white)
![Algorithm](https://img.shields.io/badge/Algorithm-Minimax%20%2B%20Alpha--Beta-green?style=flat-square)
![Tests](https://img.shields.io/badge/Tests-Passing-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)

---

## 📸 Preview

```
    1   2   3
  ┌───┬───┬───┐
A │ X │   │ O │
  ├───┼───┼───┤
B │   │ X │   │
  ├───┼───┼───┤
C │   │   │ O │
  └───┴───┴───┘

  AI is thinking (O)…
  AI plays C1  (evaluated 12 nodes)
```

---

## 🧠 How It Works

### Minimax
The AI builds a complete game tree from the current position, scores every
terminal state (+10 win / -10 loss / 0 draw), and back-propagates the best
guaranteed score up to the root.

```
            current position
           /        |        \
        A1          A2         A3
       /  \        /  \       /  \
     B1   B2    B1   B3    B1   B2
     ...  ...   ...  ...   ...  ...
```

### Alpha-Beta Pruning ✂️
Cuts branches that can **never** influence the final decision.
On a 3×3 board, pruning reduces node evaluations from ~255,000 to ~2,000.
Same result — far faster.

| Mode | Max nodes evaluated |
|------|-------------------|
| Plain Minimax | ~255 168 |
| Alpha-Beta Pruning | ~2 000 |

---

## 📁 File Structure

```
tictactoe-ai/
├── game.py        # Entry point — game loop, I/O, scoring
├── ai.py          # Minimax engine with Alpha-Beta Pruning
├── board.py       # Board state, move validation, win detection
├── test_ai.py     # Unit tests (board + AI correctness)
└── README.md
```

---

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/yourname/tictactoe-ai.git
cd tictactoe-ai

# No dependencies needed — pure Python stdlib
python game.py

# Disable Alpha-Beta Pruning (slower, educational)
python game.py --no-pruning

# Run tests
python -m pytest test_ai.py -v
# or
python test_ai.py
```

---

## 🎮 How to Play

- You will be asked to choose **X** or **O**.  X always goes first.
- Enter a move using **row letter + column number**: `A1`, `B2`, `C3`, etc.
- Type `quit` or `exit` at any time to leave.

```
  Cells reference:

    1   2   3
  ┌───┬───┬───┐
A │A1 │A2 │A3 │
  ├───┼───┼───┤
B │B1 │B2 │B3 │
  ├───┼───┼───┤
C │C1 │C2 │C3 │
  └───┴───┴───┘
```

---

## 🧪 Tests

```bash
python -m pytest test_ai.py -v
```

Key test cases:
- ✅ AI takes an immediate winning move
- ✅ AI blocks the human from winning
- ✅ AI **never loses** across 50 random games as X
- ✅ AI **never loses** across 50 random games as O
- ✅ Alpha-Beta and plain Minimax agree on moves
- ✅ Board: win/draw/reset detection

---

## 📚 Concepts Covered

| Concept | Where |
|---------|-------|
| Game tree search | `ai.py → _minimax()` |
| Alpha-Beta Pruning | `ai.py → _minimax_ab()` |
| Terminal state scoring | `ai.py → WIN/LOSS/DRAW scores` |
| Depth penalty (prefer fast wins) | `WIN_SCORE - depth` |
| Separation of concerns | `board.py` vs `ai.py` vs `game.py` |
| Unit testing | `test_ai.py` |

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

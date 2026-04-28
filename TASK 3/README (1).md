# 🎬 Movie Recommendation System

A fully-featured recommendation engine implementing **Collaborative Filtering**, **Content-Based Filtering**, and a **Hybrid approach** — built in pure Python with NumPy.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Collaborative Filtering** | User-based with Pearson correlation similarity |
| **Content-Based Filtering** | TF-IDF style genre/tag feature vectors + cosine similarity |
| **Hybrid Recommender** | Weighted blend, auto-adjusts for cold-start users |
| **25 Movies** | Curated dataset with genres, tags, and release years |
| **5 Demo Users** | Pre-loaded user profiles with realistic ratings |
| **Interactive CLI** | Full menu-driven interface |
| **Test Suite** | 25+ unit & integration tests with pytest |

---

## 🗂 Project Structure

```
recommendation-system/
├── src/
│   └── recommender.py      # Core engine (Item, User, CF, CB, Hybrid)
├── data/
│   └── movies.py           # 25-movie dataset + 5 demo users
├── tests/
│   └── test_recommender.py # Full test suite
├── docs/
│   └── architecture.md     # System design details
├── main.py                 # Interactive CLI entry point
├── demo.py                 # Quick demo (no input required)
├── requirements.txt
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
pip install numpy pytest
```

### 2. Run the demo
```bash
python demo.py
```

### 3. Run the interactive CLI
```bash
python main.py
```

### 4. Run tests
```bash
python -m pytest tests/ -v
```

---

## 🧠 How It Works

### Collaborative Filtering
Finds users with similar taste using **Pearson correlation** on shared ratings, then predicts ratings via a weighted average of neighbors' deviation from their mean.

```
predicted(u, i) = avg(u) + Σ[sim(u,v) × (r(v,i) - avg(v))] / Σ|sim(u,v)|
```

### Content-Based Filtering
Builds a **user preference profile** as a weighted average of rated item vectors. Item features are one-hot encoded genres + tags. Similarity is measured via cosine distance.

```
profile(u) = weighted_avg(item_vectors, weights=ratings)
score(u, i) = cosine_similarity(profile(u), item_vector(i))
```

### Hybrid Blend
```
hybrid_score = cf_weight × (cf_score / 5.0) + cb_weight × cb_score
```
- Default: `cf_weight=0.55`, `cb_weight=0.45`
- Auto-fallback: if user has < 3 ratings, shifts to `cf=0.10, cb=0.90`

---

## 📊 Example Output

```
🎯  Top Recommendations for Alice
────────────────────────────────────────────────────────────
   1. Spirited Away                     score=0.847  (Animation, Fantasy)
   2. Up                                score=0.821  (Animation, Drama)
   3. Finding Nemo                      score=0.798  (Animation, Adventure)
   4. Parasite                          score=0.612  (Drama, Thriller)
   5. Whiplash                          score=0.589  (Drama, Music)
```

---

## 🧪 Test Coverage

```
tests/test_recommender.py::TestItem::test_feature_vector_length   PASSED
tests/test_recommender.py::TestItem::test_feature_vector_binary   PASSED
tests/test_recommender.py::TestUser::test_rating_valid            PASSED
tests/test_recommender.py::TestUser::test_rating_out_of_range     PASSED
tests/test_recommender.py::TestSimilarity::test_cosine_identical  PASSED
... (25 tests total)
```

---

## 🔧 Extending the System

### Add your own items
```python
from src.recommender import Item
my_movie = Item("m99", "My Movie", ["Action", "Sci-Fi"], ["robots", "future"], 2024)
```

### Add a new user and get recommendations
```python
from src.recommender import User, HybridRecommender
from data.movies import MOVIES, build_demo_users

user = User("u_me", "Me")
user.rate("m03", 5)   # The Dark Knight
user.rate("m07", 4)   # The Matrix

all_users = build_demo_users() + [user]
rec = HybridRecommender()
rec.fit(all_users, MOVIES)
print(rec.recommend(user, n=5))
```

---

## 📄 License

MIT License — free to use and modify.

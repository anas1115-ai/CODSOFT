"""
Recommendation System - Core Engine
Supports: Collaborative Filtering, Content-Based Filtering, Hybrid
"""

import numpy as np
from collections import defaultdict
from typing import List, Dict, Tuple, Optional
import math


# ─────────────────────────────────────────────
#  DATA STRUCTURES
# ─────────────────────────────────────────────

class Item:
    def __init__(self, item_id: str, title: str, genres: List[str],
                 tags: List[str] = None, year: int = None):
        self.item_id   = item_id
        self.title     = title
        self.genres    = genres
        self.tags      = tags or []
        self.year      = year

    def feature_vector(self, all_genres: List[str], all_tags: List[str]) -> np.ndarray:
        genre_vec = [1 if g in self.genres else 0 for g in all_genres]
        tag_vec   = [1 if t in self.tags   else 0 for t in all_tags]
        return np.array(genre_vec + tag_vec, dtype=float)

    def __repr__(self):
        return f"Item({self.item_id!r}, {self.title!r})"


class User:
    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name    = name
        self.ratings: Dict[str, float] = {}   # item_id -> rating (1-5)

    def rate(self, item_id: str, rating: float):
        if not 1.0 <= rating <= 5.0:
            raise ValueError("Rating must be between 1 and 5")
        self.ratings[item_id] = rating

    def avg_rating(self) -> float:
        if not self.ratings:
            return 0.0
        return sum(self.ratings.values()) / len(self.ratings)

    def __repr__(self):
        return f"User({self.user_id!r}, {self.name!r})"


# ─────────────────────────────────────────────
#  SIMILARITY HELPERS
# ─────────────────────────────────────────────

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    norm_a, norm_b = np.linalg.norm(a), np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def pearson_correlation(ratings_a: Dict[str, float],
                        ratings_b: Dict[str, float]) -> float:
    common = set(ratings_a) & set(ratings_b)
    n = len(common)
    if n < 2:
        return 0.0

    va = [ratings_a[i] for i in common]
    vb = [ratings_b[i] for i in common]

    mean_a, mean_b = sum(va) / n, sum(vb) / n
    da = [x - mean_a for x in va]
    db = [x - mean_b for x in vb]

    num   = sum(x * y for x, y in zip(da, db))
    denom = math.sqrt(sum(x**2 for x in da) * sum(y**2 for y in db))
    return num / denom if denom != 0 else 0.0


# ─────────────────────────────────────────────
#  COLLABORATIVE FILTERING
# ─────────────────────────────────────────────

class CollaborativeFilter:
    """User-based collaborative filtering with Pearson correlation."""

    def __init__(self, k_neighbors: int = 5):
        self.k = k_neighbors

    def _neighbors(self, target: User, all_users: List[User]) -> List[Tuple[float, User]]:
        sims = []
        for u in all_users:
            if u.user_id == target.user_id:
                continue
            sim = pearson_correlation(target.ratings, u.ratings)
            if sim > 0:
                sims.append((sim, u))
        sims.sort(key=lambda x: x[0], reverse=True)
        return sims[:self.k]

    def predict_rating(self, target: User, item_id: str,
                       all_users: List[User]) -> float:
        neighbors = self._neighbors(target, all_users)
        num = denom = 0.0
        for sim, neighbor in neighbors:
            if item_id in neighbor.ratings:
                num   += sim * (neighbor.ratings[item_id] - neighbor.avg_rating())
                denom += abs(sim)
        if denom == 0:
            return target.avg_rating()
        return target.avg_rating() + num / denom

    def recommend(self, target: User, all_users: List[User],
                  all_items: List[Item], n: int = 10) -> List[Tuple[str, float]]:
        unrated = [it for it in all_items if it.item_id not in target.ratings]
        scores  = [(it.item_id, self.predict_rating(target, it.item_id, all_users))
                   for it in unrated]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]


# ─────────────────────────────────────────────
#  CONTENT-BASED FILTERING
# ─────────────────────────────────────────────

class ContentFilter:
    """Content-based filtering using TF-IDF style feature vectors."""

    def __init__(self):
        self.all_genres: List[str] = []
        self.all_tags:   List[str] = []

    def fit(self, items: List[Item]):
        genres, tags = set(), set()
        for it in items:
            genres.update(it.genres)
            tags.update(it.tags)
        self.all_genres = sorted(genres)
        self.all_tags   = sorted(tags)

    def _item_vec(self, item: Item) -> np.ndarray:
        return item.feature_vector(self.all_genres, self.all_tags)

    def _user_profile(self, user: User,
                      item_map: Dict[str, Item]) -> np.ndarray:
        if not user.ratings:
            return np.zeros(len(self.all_genres) + len(self.all_tags))
        vecs, weights = [], []
        for item_id, rating in user.ratings.items():
            if item_id in item_map:
                vecs.append(self._item_vec(item_map[item_id]))
                weights.append(rating)
        arr = np.array(vecs)
        w   = np.array(weights)
        return np.average(arr, axis=0, weights=w)

    def recommend(self, user: User, all_items: List[Item],
                  n: int = 10) -> List[Tuple[str, float]]:
        item_map = {it.item_id: it for it in all_items}
        profile  = self._user_profile(user, item_map)
        unrated  = [it for it in all_items if it.item_id not in user.ratings]
        scores   = [(it.item_id, cosine_similarity(profile, self._item_vec(it)))
                    for it in unrated]
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]


# ─────────────────────────────────────────────
#  HYBRID RECOMMENDER
# ─────────────────────────────────────────────

class HybridRecommender:
    """
    Weighted blend of collaborative + content-based filtering.
    Falls back gracefully when a user has few ratings.
    """

    def __init__(self, cf_weight: float = 0.5, cb_weight: float = 0.5,
                 k_neighbors: int = 5):
        if not math.isclose(cf_weight + cb_weight, 1.0, abs_tol=1e-6):
            raise ValueError("cf_weight + cb_weight must equal 1.0")
        self.cf = CollaborativeFilter(k_neighbors)
        self.cb = ContentFilter()
        self.cf_weight = cf_weight
        self.cb_weight = cb_weight
        self._items: List[Item] = []
        self._users: List[User] = []

    def fit(self, users: List[User], items: List[Item]):
        self._items = items
        self._users = users
        self.cb.fit(items)

    def recommend(self, user: User, n: int = 10) -> List[Dict]:
        # Adjust weights if user has very few ratings
        n_rated  = len(user.ratings)
        cf_w     = self.cf_weight if n_rated >= 3 else 0.1
        cb_w     = 1.0 - cf_w

        cf_scores = dict(self.cf.recommend(user, self._users, self._items, n * 2))
        cb_scores = dict(self.cb.recommend(user, self._items, n * 2))

        all_ids = set(cf_scores) | set(cb_scores)
        blended = {}
        for iid in all_ids:
            blended[iid] = (cf_w * cf_scores.get(iid, 0.0) / 5.0 +
                            cb_w * cb_scores.get(iid, 0.0))

        item_map = {it.item_id: it for it in self._items}
        results  = sorted(blended.items(), key=lambda x: x[1], reverse=True)[:n]

        return [
            {
                "item_id": iid,
                "title":   item_map[iid].title,
                "genres":  item_map[iid].genres,
                "score":   round(score, 4),
                "cf_score": round(cf_scores.get(iid, 0.0), 4),
                "cb_score": round(cb_scores.get(iid, 0.0), 4),
            }
            for iid, score in results if iid in item_map
        ]

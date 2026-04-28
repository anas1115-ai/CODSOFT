# System Architecture

## Overview

```
┌──────────────────────────────────────────────────────────┐
│                    HybridRecommender                      │
│                                                          │
│   ┌────────────────────┐    ┌────────────────────────┐   │
│   │ CollaborativeFilter│    │    ContentFilter        │   │
│   │                    │    │                         │   │
│   │  Pearson Similarity│    │  Cosine Similarity      │   │
│   │  User-User matrix  │    │  Genre + Tag vectors    │   │
│   └────────────────────┘    └────────────────────────┘   │
│            ↓  cf_weight               ↓  cb_weight        │
│            └──────────┬───────────────┘                   │
│                       ↓                                   │
│               Weighted Blend Score                        │
└──────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### Cold-Start Handling
When a user has fewer than 3 ratings, the system shifts weights to favour
content-based filtering (CB = 90%) since collaborative filtering requires
shared ratings with other users to be effective.

### Rating Normalisation
Collaborative filtering normalises ratings by subtracting each user's mean
before computing weighted sums. This removes personal rating scale bias
(e.g., a user who gives 3/5 as their "best" vs one who gives 5/5).

### Feature Vectors
Items are encoded as binary vectors over the union of all genres and tags.
The user profile is a weighted average where higher-rated items contribute
more to the taste profile.

## Complexity

| Operation | Time |
|---|---|
| CF recommend | O(U × R) where U=users, R=common ratings |
| CB recommend | O(I × F) where I=items, F=features |
| Hybrid blend | O(I log I) for sorting |

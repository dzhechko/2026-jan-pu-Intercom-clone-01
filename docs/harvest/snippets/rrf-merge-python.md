# Snippet: Reciprocal Rank Fusion Merge (Python)

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Merges two ranked result lists using the Reciprocal Rank Fusion (RRF) algorithm. Each document receives a score of `1 / (k + rank + 1)` from each list it appears in, and scores are summed across lists. The merged list is sorted by total RRF score in descending order. Works with any items that have a unique identifier.

## Dependencies

None (Python standard library only).

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `k` | `60` | Smoothing constant. Higher values reduce the impact of high-ranking items. The value 60 is the standard from the original RRF paper. |

## Code

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class RankedItem:
    """A search result with an ID, content, and a score."""
    id: str
    content: str
    score: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


def rrf_merge(
    list_a: list[RankedItem],
    list_b: list[RankedItem],
    k: int = 60,
) -> list[RankedItem]:
    """Merge two ranked result lists using Reciprocal Rank Fusion.

    Args:
        list_a: First ranked list (e.g., vector search results).
        list_b: Second ranked list (e.g., keyword search results).
        k: RRF smoothing constant (default 60).

    Returns:
        Merged list sorted by RRF score (descending).
    """
    scores: dict[str, float] = {}
    items: dict[str, RankedItem] = {}

    for rank, item in enumerate(list_a):
        scores[item.id] = scores.get(item.id, 0.0) + 1.0 / (k + rank + 1)
        items[item.id] = item

    for rank, item in enumerate(list_b):
        scores[item.id] = scores.get(item.id, 0.0) + 1.0 / (k + rank + 1)
        if item.id not in items:
            items[item.id] = item

    sorted_ids = sorted(scores, key=lambda x: scores[x], reverse=True)

    result = []
    for item_id in sorted_ids:
        item = items[item_id]
        item.score = scores[item_id]
        result.append(item)

    return result
```

## Usage Example

```python
vector_results = [
    RankedItem(id="doc-1", content="Introduction to databases"),
    RankedItem(id="doc-3", content="PostgreSQL performance tuning"),
    RankedItem(id="doc-5", content="Index optimization strategies"),
]

keyword_results = [
    RankedItem(id="doc-3", content="PostgreSQL performance tuning"),
    RankedItem(id="doc-2", content="SQL query best practices"),
    RankedItem(id="doc-1", content="Introduction to databases"),
]

merged = rrf_merge(vector_results, keyword_results)
# doc-3 ranks highest (appears in both lists at good positions)
# doc-1 also benefits from appearing in both lists
```

## Notes

- The `RankedItem` dataclass can be replaced with any object that has a unique `id` attribute. Adapt the field access as needed.
- The algorithm extends naturally to more than two lists: add another loop for each additional list.
- If one list is empty, the function degrades gracefully to single-list ranking with RRF scores.
- The `k=60` default is from the original paper by Cormack, Clarke, and Buettcher (2009). Empirically, values between 40 and 80 perform similarly across most datasets.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |

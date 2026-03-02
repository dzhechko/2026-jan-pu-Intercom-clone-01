# Snippet: Confidence Estimation from RAG Results (Python)

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Estimates a confidence score (0.0 to 1.0) from RAG retrieval results. Combines a weighted average of document similarity scores, a bonus for having multiple relevant references, and a configurable baseline. Useful for deciding whether an LLM response is trustworthy enough to deliver or should be escalated to a human.

## Dependencies

None (Python standard library only).

## Code

```python
def estimate_confidence(
    similarity_scores: list[float],
    baseline: float = 0.1,
    similarity_weight: float = 0.7,
    reference_bonus_weight: float = 0.2,
    min_references_for_bonus: int = 2,
    max_references_for_bonus: int = 5,
) -> float:
    """Estimate confidence from RAG retrieval similarity scores.

    Args:
        similarity_scores: List of similarity scores from retrieved documents (0.0-1.0 each).
        baseline: Minimum confidence even with no results.
        similarity_weight: Weight for the average similarity component.
        reference_bonus_weight: Weight for the reference count bonus component.
        min_references_for_bonus: Minimum number of results to start earning the bonus.
        max_references_for_bonus: Number of results at which the bonus is fully earned.

    Returns:
        Confidence score clamped to [0.0, 1.0].
    """
    if not similarity_scores:
        return baseline

    # Component 1: Weighted average of similarity scores
    avg_similarity = sum(similarity_scores) / len(similarity_scores)

    # Component 2: Bonus for having multiple relevant references
    n_refs = len(similarity_scores)
    if n_refs >= max_references_for_bonus:
        reference_bonus = 1.0
    elif n_refs >= min_references_for_bonus:
        reference_bonus = (n_refs - min_references_for_bonus) / (
            max_references_for_bonus - min_references_for_bonus
        )
    else:
        reference_bonus = 0.0

    # Combine components
    confidence = (
        baseline
        + similarity_weight * avg_similarity
        + reference_bonus_weight * reference_bonus
    )

    return max(0.0, min(1.0, confidence))
```

## Usage Example

```python
# High confidence: multiple relevant documents with good similarity
scores = [0.92, 0.88, 0.85, 0.81, 0.79]
confidence = estimate_confidence(scores)
print(f"Confidence: {confidence:.2f}")  # ~0.95

# Low confidence: few documents, mediocre similarity
scores = [0.55]
confidence = estimate_confidence(scores)
print(f"Confidence: {confidence:.2f}")  # ~0.49

# No results at all
confidence = estimate_confidence([])
print(f"Confidence: {confidence:.2f}")  # 0.10 (baseline only)

# Decision logic
ESCALATION_THRESHOLD = 0.6
if confidence < ESCALATION_THRESHOLD:
    print("Escalating to human review")
else:
    print("Confidence sufficient for automated response")
```

## Notes

- The default weights (`baseline=0.1`, `similarity_weight=0.7`, `reference_bonus_weight=0.2`) sum to 1.0, so the theoretical maximum confidence is 1.0 when both components are perfect. Adjust weights based on your domain.
- The `reference_bonus` rewards having multiple corroborating sources. A single high-similarity result scores lower than multiple moderately-similar results, reflecting the principle that corroboration increases trust.
- The `baseline` ensures that confidence is never exactly zero, which can be useful for downstream systems that interpret zero as "no data" rather than "low confidence."
- Similarity scores should be pre-filtered by a minimum threshold before being passed to this function. Including very low-similarity results (below 0.5) will drag down the average.
- This is a heuristic estimator, not a calibrated probability. Use it for relative comparison and threshold-based decisions, not as a true probability of correctness.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |

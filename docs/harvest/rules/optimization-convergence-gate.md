# Rule: Stop Optimization When Delta Falls Below Threshold

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

In any iterative optimization loop, enforce explicit convergence and safety gates:

1. **Minimum delta gate**: Accept an iteration ONLY if `new_score - previous_score > 0.5` (on a 10-point scale). Improvements at or below 0.5 are noise, not signal.
2. **Convergence detection**: If 3 consecutive iterations produce delta <= 0.5, declare convergence and stop the loop. Further iterations will not produce meaningful improvement.
3. **Regression rollback**: If the score DECREASES by more than 1.0 point in any iteration, immediately rollback to the previous best version. Log the regression with full context.
4. **Runaway prevention**: If more than 10 iterations occur without reaching convergence or an acceptable score, abort the loop entirely and escalate to human review.
5. **Content diff requirement**: When delta > 0.5, verify that substantive content actually changed (not just superficial rewording that games the scoring rubric).

## Why

Without explicit stopping conditions, optimization loops run indefinitely. LLM-driven optimization is especially prone to this because:
- The optimizer can always produce a "different" output, creating the illusion of progress
- Scores may fluctuate randomly around a plateau, with occasional spikes that reset iteration counters
- Each iteration costs money (model inference) and time
- Late iterations often degrade quality through overfitting to the evaluation rubric

Runaway optimization wastes resources, produces diminishing returns, and can actually decrease quality as the artifact overfits to scoring criteria rather than genuine quality.

## Example (what goes wrong)

An optimization loop without convergence gates:

```
Iteration 1:  Score 6.2  (delta: +6.2)  ← genuine improvement
Iteration 2:  Score 7.1  (delta: +0.9)  ← genuine improvement
Iteration 3:  Score 7.3  (delta: +0.2)  ← noise
Iteration 4:  Score 7.5  (delta: +0.2)  ← noise
Iteration 5:  Score 7.2  (delta: -0.3)  ← regression
Iteration 6:  Score 7.4  (delta: +0.2)  ← recovering to plateau
Iteration 7:  Score 7.6  (delta: +0.2)  ← noise
...
Iteration 25: Score 7.3  (delta: -0.1)  ← still going, 20 wasted iterations
```

The loop should have stopped at Iteration 4 (three consecutive deltas <= 0.5). Instead, it ran for 25 iterations, consuming 23 unnecessary model calls and producing no meaningful improvement over the Iteration 2 result.

Phantom improvement variant: Score jumps from 7.3 to 8.1, but the content diff reveals only cosmetic changes (reworded sentences, reordered paragraphs). The artifact gamed the rubric without genuine improvement.

## Correct Approach

```
Iteration 1:  Score 6.2  (delta: +6.2)  → ACCEPT (delta > 0.5)
Iteration 2:  Score 7.1  (delta: +0.9)  → ACCEPT (delta > 0.5)
Iteration 3:  Score 7.3  (delta: +0.2)  → REJECT (delta <= 0.5, streak: 1)
Iteration 4:  Score 7.5  (delta: +0.2)  → REJECT (delta <= 0.5, streak: 2)
Iteration 5:  Score 7.4  (delta: -0.1)  → REJECT (delta <= 0.5, streak: 3)
                                         → CONVERGED. Stop. Best version: Iteration 2 (7.1)
                                           or Iteration 4 (7.5) if marginal gains are kept.
```

If instead at Iteration 3 the score dropped to 5.8 (delta: -1.3):
```
Iteration 3:  Score 5.8  (delta: -1.3)  → REGRESSION > 1.0
                                         → ROLLBACK to Iteration 2 (7.1)
                                         → Log: "Regression of 1.3 points. Rolled back."
```

Implementation checklist:
- [ ] Delta threshold defined (default: 0.5 on 10-point scale)
- [ ] Convergence streak limit defined (default: 3 consecutive)
- [ ] Regression threshold defined (default: 1.0 point decrease)
- [ ] Maximum iteration count defined (default: 10)
- [ ] Content diff check on accepted iterations (detect phantom improvement)
- [ ] All rejections, rollbacks, and convergence events logged with scores

## Scope

Any iterative optimization pipeline:
- Prompt optimization loops
- Content refinement pipelines
- Hyperparameter tuning
- Automated A/B testing iterations
- Quality improvement cycles for generated artifacts

Scale the thresholds to match the scoring system (e.g., on a 100-point scale, use delta > 5 instead of > 0.5).

## Expiry

Review after 12 months. The specific threshold values (0.5, 3 consecutive, 1.0 regression) may need calibration for different domains, but the principle of explicit convergence gates is durable.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Derived from observation of runaway optimization loops consuming 20+ iterations with no meaningful improvement beyond iteration 2-3. |

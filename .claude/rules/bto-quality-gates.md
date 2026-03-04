# BTO Quality Gate Rules

## What is BTO
BTO (Build-Test-Optimize) is a pipeline for generating, evaluating, and iteratively
improving skills, prompts, or any structured artifact via agent-driven evaluation loops.
These rules apply to ANY evaluation system, not just Keysarium.

## Layer Architecture and Model Budget

| Layer | Role | Model | Trigger |
|-------|------|-------|---------|
| Layer 0 | Structural pre-check (format, completeness) | haiku | Always |
| Layer 1 | Shallow semantic check (relevance, coherence) | haiku | After Layer 0 passes |
| Layer 2 | Deep evaluation (quality, domain fit) | sonnet (judge panel) | After Layer 1 passes |
| Layer 3 | Creative synthesis / optimization crossover | opus | On top-N candidates only |

Never promote an artifact to a higher layer if the lower layer gate fails.

## Cost Optimization Table

| Task | Model | Rationale |
|------|-------|-----------|
| Layer 0 structural checks | haiku | High-frequency, pattern-matching only |
| Layer 1 semantic baseline | haiku | Fast coherence scan, no deep reasoning needed |
| Judge 1 — Domain Expert | sonnet | Domain knowledge + nuanced scoring |
| Judge 2 — Critic | sonnet | Adversarial analysis, pattern detection |
| Judge 3 — Completeness Auditor | sonnet | Structured coverage check |
| Meta-judge (escalation) | sonnet | Disagreement resolution |
| Crossover / creative synthesis | opus | Novel combination of best candidates |
| Mutation workers (standard) | sonnet | Requires reasoning about improvement direction |
| Variant fast-eval (ranking pass) | haiku | Volume scoring before full panel |

Escalate to a higher-cost model only when the lower-cost model has failed or is insufficient.

## Layer 0 Mandatory Checks
Every generated skill or artifact MUST pass ALL of these before entering judge panel:

- [ ] Required sections present (structure check)
- [ ] No empty placeholders (`[TODO]`, `[TBD]`, `<INSERT>`)
- [ ] Length within bounds (not below minimum, not above maximum)
- [ ] Encoding valid (no broken unicode, no binary artifacts)
- [ ] Self-reference loop absent (artifact does not cite itself as source)

If any check fails → reject immediately, log reason, do NOT send to judges.
Layer 0 may auto-retry up to 3 times before escalating to human review.

## Judge Panel Rules

- Panel MUST have an odd number of judges: 3 (standard) or 5 (high-stakes)
- Each judge operates in strict isolation: reads the same artifact, writes to a separate evaluation file
- Judges do NOT see each other's scores before submitting
- Final score = weighted average (weights defined per panel configuration)
- Standard weights: Domain Expert 0.4 / Critic 0.3 / Completeness Auditor 0.3
- Disagreement threshold: if max_score - min_score > 3 points → escalate to meta-judge

## Optimization Delta Gate

- An optimization iteration is accepted ONLY if: `new_score - prev_score > 0.5`
- If delta <= 0.5 for 3 consecutive iterations → declare convergence and stop
- If score DECREASES by > 1.0 → rollback to previous best and log regression
- Improvement must be measurable on the same rubric used in the previous iteration

## Human Checkpoint Rules

- NEVER auto-approve any artifact for delivery without a human checkpoint
- Checkpoint is required after: Layer 2 evaluation, final optimization round, before packaging
- Checkpoint format follows the standard checkpoint-protocol.md
- Exception: Layer 0 rejections may be auto-retried up to 3 times before human escalation

## BTO-Specific Anti-Patterns

| Anti-Pattern | Detection Signal | Required Fix |
|-------------|-----------------|--------------|
| Score inflation | All judges score > 8.5 on first attempt | Add calibration prompt to critics |
| Overfitting to rubric | Artifact optimizes wording to match rubric literally | Blind evaluation: hide rubric from generator |
| Conformity collapse | Judges converge to identical scores after 1 round | Enforce isolation, re-randomize judge order |
| Runaway optimization | > 10 iterations without convergence | Abort, log, human review |
| Phantom improvement | Delta > 0.5 but no substantive content change | Diff-check content, not just score |
| Judge-generator collusion | Same model used for both generation and evaluation | BLOCK — generator and judge models must differ |
| Missing rejection log | Failed artifacts silently discarded | Every rejection MUST be logged with reason |

## Auto-Detection
Self-check generated artifacts and evaluation results against the anti-patterns above.
If detected, flag with a WARNING label and halt the BTO loop pending human review.

## Reusability Note
These rules are artifact-type agnostic. Apply them to:
- Skill generation pipelines
- Prompt optimization loops
- Presentation scoring systems
- Any multi-judge evaluation workflow

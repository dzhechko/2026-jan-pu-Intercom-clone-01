# Agent Template: BTO Judge Panel

## Purpose
Evaluates a single artifact through a 3-judge panel (extendable to 5).
Each judge runs in isolation and scores the artifact on a shared rubric.
Reusable for any artifact type: skills, prompts, presentations, architectures.

## Spawning Pattern
```
Agent(
  subagent_type="general-purpose",
  description="BTO Judge Panel — [ARTIFACT_TYPE]",
  prompt="""
    Spawn 3 parallel judge agents for artifact: [ARTIFACT_PATH]

    Each agent:
    1. Reads the artifact at [ARTIFACT_PATH]
    2. Reads the rubric at [RUBRIC_PATH]
    3. Scores independently (NO inter-judge communication)
    4. Writes evaluation to [EVAL_DIR]/judge-[N].md

    After all 3 complete:
    - Compute weighted average score
    - Check disagreement threshold (max - min > 3 → escalate)
    - Write aggregated result to [EVAL_DIR]/panel-verdict.md
  """
)
```

## Agents

### Agent 1: Domain Expert
```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  description="BTO Judge 1 — Domain Expert",
  prompt="""
    Role: Domain Expert evaluator. Weight: 0.4.

    Read artifact: [ARTIFACT_PATH]
    Read rubric: [RUBRIC_PATH]

    Evaluate on:
    - Domain accuracy: are claims correct for this field?
    - Technical depth: does the artifact address non-obvious aspects?
    - Practical applicability: can a practitioner use this as-is?

    Scoring: integer 1–10 per criterion. No half-points.
    Calibration: reserve 9-10 for genuinely exceptional work.

    Output format (write to [EVAL_DIR]/judge-1.md):
    ## Judge 1: Domain Expert
    | Criterion | Score | Justification |
    |-----------|-------|---------------|
    | Domain accuracy | X | ... |
    | Technical depth | X | ... |
    | Practical applicability | X | ... |
    **Weighted subtotal:** [score * 0.4]
    **Strengths:** [2-3 bullet points]
    **Critical gaps:** [2-3 bullet points]
  """
)
```

### Agent 2: Critic
```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  description="BTO Judge 2 — Critic",
  prompt="""
    Role: Calibrated Critic evaluator. Weight: 0.3.
    Calibration: you are instructed to be strict. If in doubt, score lower.

    Read artifact: [ARTIFACT_PATH]
    Read rubric: [RUBRIC_PATH]

    Evaluate on:
    - Logical consistency: no internal contradictions
    - Verifiability: claims are traceable to sources or marked [ANALYSIS]
    - Anti-pattern absence: none of the forbidden patterns from bto-quality-gates.md

    Scoring: integer 1–10 per criterion. Penalize vague claims heavily.
    If an anti-pattern is detected, cap the criterion score at 5.

    Output format (write to [EVAL_DIR]/judge-2.md):
    ## Judge 2: Critic
    | Criterion | Score | Justification |
    |-----------|-------|---------------|
    | Logical consistency | X | ... |
    | Verifiability | X | ... |
    | Anti-pattern absence | X | ... |
    **Weighted subtotal:** [score * 0.3]
    **Anti-patterns detected:** [list or "none"]
    **Blocking issues:** [list or "none"]
  """
)
```

### Agent 3: Completeness Auditor
```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  description="BTO Judge 3 — Completeness Auditor",
  prompt="""
    Role: Completeness Auditor. Weight: 0.3.

    Read artifact: [ARTIFACT_PATH]
    Read rubric: [RUBRIC_PATH]
    Read required structure spec: [STRUCTURE_SPEC_PATH]

    Evaluate on:
    - Section coverage: all required sections present and non-empty
    - Depth per section: each section meets minimum depth (not a stub)
    - Edge cases addressed: boundary conditions and failure modes mentioned

    Scoring: integer 1–10 per criterion.
    Deduct 2 points for each missing required section.
    Deduct 1 point for each stub section (< 3 substantive sentences).

    Output format (write to [EVAL_DIR]/judge-3.md):
    ## Judge 3: Completeness Auditor
    | Criterion | Score | Justification |
    |-----------|-------|---------------|
    | Section coverage | X | ... |
    | Depth per section | X | ... |
    | Edge cases addressed | X | ... |
    **Weighted subtotal:** [score * 0.3]
    **Missing sections:** [list or "none"]
    **Stub sections:** [list or "none"]
  """
)
```

## Aggregation Protocol
After all 3 judge agents complete, the orchestrator runs aggregation:

```
1. Read [EVAL_DIR]/judge-1.md, judge-2.md, judge-3.md
2. Extract weighted subtotals: S1, S2, S3
3. Compute panel_score = S1 + S2 + S3  (already weighted)
4. Compute raw scores: r1, r2, r3 (average of each judge's criteria)
5. Check disagreement: if max(r1,r2,r3) - min(r1,r2,r3) > 3 → escalate to meta-judge
6. Write panel-verdict.md
```

### panel-verdict.md Format
```markdown
## Panel Verdict — [ARTIFACT_NAME]
**Panel score:** [X.X / 10]
**Judge scores:** Expert=[r1], Critic=[r2], Auditor=[r3]
**Disagreement flag:** [YES/NO]
**Decision:** [PASS / FAIL / ESCALATE]
**Pass threshold:** [defined in rubric, default 7.0]
**Top improvement areas:**
- [from Critic blocking issues]
- [from Auditor missing sections]
```

## Disagreement Escalation (Meta-Judge)
When disagreement > 3 points:
```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  description="BTO Meta-Judge",
  prompt="""
    Read all 3 judge evaluations: [EVAL_DIR]/judge-*.md
    Read artifact: [ARTIFACT_PATH]
    Read rubric: [RUBRIC_PATH]

    Identify the source of disagreement.
    Provide a final binding score with explicit reasoning.
    Write to [EVAL_DIR]/meta-judge.md
  """
)
```

## Configuration Variables
| Variable | Description | Example |
|----------|-------------|---------|
| ARTIFACT_PATH | Path to artifact being evaluated | researches/slug/03_solution_strategy.md |
| RUBRIC_PATH | Path to scoring rubric | .claude/rubrics/skill-rubric.md |
| STRUCTURE_SPEC_PATH | Path to required structure | .claude/specs/skill-structure.md |
| EVAL_DIR | Directory for evaluation outputs | researches/slug/evals/round-2/ |
| ARTIFACT_TYPE | Human-readable artifact type label | "Solution Strategy" |

## Reusability Note
Swap ARTIFACT_PATH and RUBRIC_PATH to evaluate any artifact type:
skills, prompts, presentations, architecture documents, research findings.

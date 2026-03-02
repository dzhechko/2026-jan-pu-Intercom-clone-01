---
description: Autonomous project build loop. Bootstraps project and implements features
  one by one until MVP (default) or all features are done.
  $ARGUMENTS: "mvp" (default) | "all" — scope of features to implement
---

# /run $ARGUMENTS

## Purpose

End-to-end autonomous project build: bootstrap → implement features in loop → done.
Combines `/start`, `/next`, and `/go` into a single continuous pipeline.

## Step 0: Parse Scope

```
IF $ARGUMENTS is empty OR $ARGUMENTS == "mvp":
    scope = "mvp"
    → Implement only features with status `next` or `in_progress`
    → Stop when no more `next` features remain (skip `planned`)

IF $ARGUMENTS == "all":
    scope = "all"
    → Implement ALL features regardless of status
    → Stop only when every feature is `done`
```

## Step 1: Bootstrap Project

1. Check if project is already bootstrapped:
   - IF `docker-compose.yml` exists AND key source dirs exist → skip to Step 2
   - ELSE → run `/start`
2. Verify bootstrap succeeded:
   - Project structure exists
   - Docker services running (if applicable)
   - Basic health checks pass
3. Commit and push: `git push origin HEAD`

## Step 2: Feature Implementation Loop

**CRITICAL: Every feature MUST go through `/go` — never skip to direct implementation.**
`/go` provides mandatory complexity scoring that determines the correct pipeline.
Skipping `/go` caused 5 features to be built without validation or review (see Insight 001).

```
pipeline_log = []   # Track pipeline decisions for final report

LOOP:
    1. Run `/next` to get current sprint status and next feature

    2. IF scope == "mvp":
         - Get next feature with status `next` or `in_progress`
         - IF no such feature exists → EXIT LOOP (MVP complete)
       IF scope == "all":
         - Get next feature that is NOT `done`
         - IF all features are `done` → EXIT LOOP (all complete)

    3. MANDATORY: Run `/go <feature-name>` to implement the feature
       - /go MUST output its COMPLEXITY SCORING block (see /go Step 2)
       - /go selects /plan, /feature, or /feature-ent based on score
       - /go handles commits and pushes
       - IF /go's scoring block is missing → STOP and re-run /go

    4. Log pipeline decision:
       ```
       [N/total] <feature-name>
         Score: <N> → Pipeline: /plan | /feature | /feature-ent
         Status: done | blocked
       ```
       pipeline_log.append({feature, score, pipeline, status})

    5. Verify implementation:
       - Run project tests: `pytest tests/ -v`
       - IF tests fail → fix before continuing
       - IF fix fails after 3 attempts → mark as `blocked`, push, continue

    6. Update progress:
       - Feature marked as `done` in roadmap (handled by /go)
       - Log progress to stdout

    7. CONTINUE LOOP
```

## Step 3: Finalize

After loop completes:

1. Run full test suite: `pytest tests/ -v`
2. Update README.md with current state
3. Final commit: `git add -A && git commit -m "milestone: <scope> complete"`
4. Push and tag:
   ```bash
   git push origin HEAD
   IF scope == "mvp":
       git tag v0.1.0-mvp && git push origin v0.1.0-mvp
   IF scope == "all":
       git tag v1.0.0 && git push origin v1.0.0
   ```
5. Generate summary report (using pipeline_log from Step 2):

```
/run <scope> — COMPLETE

Summary:
   Features implemented: <count>/<total>
   Total commits: <count>
   Total files: <count>
   Test results: <passed>/<total>

Pipeline decisions (from /go scoring):
   <feature-1>  score: <N> → /plan
   <feature-2>  score: <N> → /feature
   <feature-3>  score: <N> → /feature-ent
   <feature-4>  score: <N> → /feature (BLOCKED after 3 attempts)
   ...

Tagged: v0.1.0-mvp | v1.0.0

IF any features blocked:
   Blocked features: <count>
   Review blocked features manually before next release.

IF scope == "mvp" AND planned features remain:
   Remaining planned features: <count>
   To continue: /run all
```

## Error Recovery

- Each feature is committed independently → partial progress is saved
- If a feature fails repeatedly (3 attempts), skip it and mark as `blocked`
- If `/start` fails, stop and report — project bootstrap is critical
- On any failure: always push current state to remote first

## Parallelization

- `/go` handles per-feature parallelization internally
- Features are implemented sequentially (one at a time) to avoid conflicts
- Within each feature, /go maximizes internal parallelism

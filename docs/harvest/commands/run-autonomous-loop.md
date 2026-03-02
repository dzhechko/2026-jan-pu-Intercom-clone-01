# Command: /run

## Maturity: Alpha v1.0

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

---

## When to Use

- When a backlog of well-specified features needs to be implemented in sequence or batch
- When running an automated build session overnight or during off-hours
- When a set of independent features can be processed without human intervention between each one
- For bootstrap scenarios where many small features need to be scaffolded rapidly

## When NOT to Use

- For features that require human design decisions or clarification mid-implementation
- When features have complex interdependencies that require manual ordering
- For production-critical features that need human review at each step
- When the project's test infrastructure is unreliable (flaky tests will cause false blocks)
- For a single feature (use `/go` or the appropriate pipeline directly)

## Prerequisites

- A feature backlog defined as a structured list (file, array, or backlog tool output)
- A complexity scoring and routing mechanism (e.g., `/go` command) configured and working
- A test suite that provides reliable pass/fail signals
- Git configured for automated commits
- Sufficient context and specifications for each feature to be implemented without human input

## Command Specification

### Purpose

Autonomously iterate through a feature backlog, scoring, routing, implementing, testing, and committing each feature in sequence. The loop includes error recovery, pipeline decision logging, and a final summary report. This is the "hands-off build session" command.

### Invocation

```
/run [backlog-source]
```

Where `[backlog-source]` can be:
- A file path containing the feature list (e.g., `docs/backlog.md`, `backlog.json`)
- A keyword referencing a configured backlog source
- Omitted to use the default backlog location

### Backlog Format

The backlog is an ordered list of features, each with at minimum a name and description:

```json
[
  {
    "id": "F-001",
    "name": "feature-name",
    "description": "What the feature does and acceptance criteria",
    "priority": 1,
    "dependencies": []
  }
]
```

Markdown format is also supported:

```markdown
## Feature Backlog

- [ ] F-001: Feature Name — Description and acceptance criteria
- [ ] F-002: Another Feature — Description and acceptance criteria
```

Features with unresolved dependencies (referencing other features not yet completed) are skipped until their dependencies are met.

### Loop Execution

For each feature in the backlog:

```
1. Read feature specification
2. Check dependencies (skip if unmet, revisit later)
3. Score complexity → route to pipeline (/go)
4. Execute routed pipeline:
   a. Plan implementation
   b. Implement changes
   c. Run tests
   d. Run review (if pipeline includes it)
   e. Commit changes
5. Record result in pipeline log
6. Mark feature as completed in backlog
7. Move to next feature
```

### Error Recovery

Each feature has a configurable retry budget (default: 3 attempts). Error handling follows this escalation:

| Attempt | Action |
|---------|--------|
| 1st failure | Log error, analyze failure, retry with adjusted approach |
| 2nd failure | Log error, attempt alternative implementation strategy |
| 3rd failure | Mark feature as `blocked`, log full error context, skip to next feature |

Failure types and their handling:

| Failure Type | Recovery Strategy |
|-------------|-------------------|
| Test failure | Analyze failing test, fix implementation, retry |
| Lint/format error | Auto-fix if possible, retry |
| Build error | Analyze error output, fix code, retry |
| Review failure (score below threshold) | Address review findings, retry |
| Timeout | Increase timeout on retry, then skip |
| Unrecoverable error | Mark blocked immediately, do not retry |

When a feature is marked `blocked`, the loop continues with the next feature. Blocked features are collected in the final report.

### Pipeline Decision Log

Every loop iteration appends an entry to the pipeline log:

```json
{
  "timestamp": "2026-03-02T14:30:00Z",
  "feature_id": "F-001",
  "feature_name": "feature-name",
  "complexity_score": 4.2,
  "tier": "standard",
  "pipeline": "/feature",
  "attempts": 1,
  "status": "completed",
  "commit_sha": "abc1234",
  "duration_seconds": 180,
  "errors": []
}
```

For blocked features:

```json
{
  "timestamp": "2026-03-02T14:35:00Z",
  "feature_id": "F-003",
  "feature_name": "problematic-feature",
  "complexity_score": 6.8,
  "tier": "standard",
  "pipeline": "/feature",
  "attempts": 3,
  "status": "blocked",
  "commit_sha": null,
  "duration_seconds": 540,
  "errors": ["Attempt 1: test_auth failed...", "Attempt 2: ...", "Attempt 3: ..."]
}
```

### Final Report

After processing all features (or when the loop is halted), the command produces a summary report:

```markdown
# Autonomous Build Report

## Session Summary
- **Started**: 2026-03-02 14:00:00
- **Completed**: 2026-03-02 16:30:00
- **Duration**: 2h 30m
- **Features Processed**: 12
- **Completed**: 10
- **Blocked**: 2
- **Skipped (unmet dependencies)**: 0

## Pipeline Routing Distribution
| Pipeline | Count | Avg Duration |
|----------|-------|-------------|
| /plan | 4 | 45s |
| /feature | 6 | 180s |
| /feature-ent | 0 | - |

## Per-Feature Results
| ID | Feature | Pipeline | Status | Attempts | Duration | Commit |
|----|---------|----------|--------|----------|----------|--------|
| F-001 | feature-name | /feature | completed | 1 | 120s | abc1234 |
| F-002 | another-feature | /plan | completed | 1 | 30s | def5678 |
| F-003 | problematic-feature | /feature | blocked | 3 | 540s | - |

## Blocked Features
### F-003: problematic-feature
- **Reason**: Test failures in auth module after 3 attempts
- **Last Error**: `AssertionError: expected 200, got 401`
- **Recommendation**: Manual investigation required

## Next Steps
- Review blocked features and resolve manually
- Run `/run --resume` to continue from where the session left off
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `max_retries` | `3` | Maximum attempts per feature before marking as blocked |
| `backlog_path` | `docs/backlog.md` | Default backlog file location |
| `pipeline_log_path` | `docs/pipeline_log.jsonl` | Path for pipeline decision log |
| `report_path` | `docs/build-report.md` | Path for the final session report |
| `timeout_per_feature` | `600` | Maximum seconds per feature (across all attempts) |
| `auto_commit` | `true` | Whether to auto-commit after each successful feature |
| `stop_on_block` | `false` | Whether to halt the entire loop when a feature is blocked |
| `dependency_resolution` | `skip-and-revisit` | How to handle unmet dependencies: `skip-and-revisit`, `skip-permanently`, `halt` |

## Variants

| Variant | Description |
|---------|-------------|
| `/run` | Process entire backlog from default location |
| `/run [file]` | Process backlog from specified file |
| `/run --resume` | Continue from last session, skipping already-completed features |
| `/run --dry-run` | Score and route all features but do not execute pipelines; output planned routing |
| `/run --limit N` | Process at most N features, then stop |
| `/run --filter [tag]` | Only process features matching the given tag or label |
| `/run --report-only` | Generate a report from existing pipeline log without running any features |

## Gotchas

- **Cascading failures**: If an early feature breaks shared infrastructure (e.g., corrupts a config file), subsequent features may fail for unrelated reasons. The loop does not detect environmental contamination between features. Consider running each feature in a clean branch or with state isolation.
- **Test reliability**: The loop depends on tests to validate each feature. Flaky tests will cause features to be marked as blocked when they are actually correct. Stabilize the test suite before running autonomous loops.
- **Commit granularity**: Each feature produces one commit. If a feature is large and the implementation touches many files, the commit may be too coarse for effective `git bisect`. Consider breaking large features into smaller backlog items.
- **Resource consumption**: Long autonomous sessions consume significant compute (LLM calls, Docker builds, test runs). Monitor resource usage and set appropriate timeouts.
- **Dependency ordering**: The default `skip-and-revisit` strategy can loop indefinitely if there is a circular dependency in the backlog. The loop detects cycles after 2 full passes with no progress and halts with an error.
- **Partial state on halt**: If the loop is interrupted mid-feature (e.g., process kill, timeout), the working directory may contain uncommitted changes. The `--resume` variant checks for dirty state and prompts for resolution before continuing.
- **Backlog mutation**: Do not modify the backlog file while the loop is running. The loop reads the backlog at startup and tracks progress in the pipeline log. Mid-run backlog changes are ignored.
- **Override propagation**: The loop uses `/go` for routing, which means override settings (e.g., `--force`) are not supported per-feature in the backlog. All features are routed by their scores.

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-02 | Initial extraction. Backlog iteration, complexity-based routing, retry/skip error recovery, session reporting. |

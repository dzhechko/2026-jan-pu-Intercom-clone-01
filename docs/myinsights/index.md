# Development Insights Index

## Pipeline & Workflow

- [001: /run → /go → /feature pipeline gaps](001-run-go-feature-pipeline-gaps.md)
  Critical: /run bypasses /go scoring and /feature lifecycle phases entirely. 6 root causes identified.

- [003: /feature needs mandatory artifact checklist](003-feature-lifecycle-artifact-checklist.md)
  High: Without mandatory outputs per phase, LLM skips validation and review entirely.

- [004: /feature command doesn't match its own template](004-feature-command-vs-template-mismatch.md)
  Critical: command was ad-hoc simplified instead of generated from feature-lifecycle.md template.
  Rule was correct, command was not. Root cause: /replicate Phase 3 generation gap.

- [005: /plan and /feature write to same directory](005-plan-vs-feature-path-conflict.md)
  High: /plan wrote flat files to docs/features/ which conflicts with /feature's per-feature directories.
  Fixed: /plan now writes to docs/plans/. No template exists for /plan — needs one.

- [008: Pipeline discipline enforcement — /go, /run, /feature hardened](008-pipeline-discipline-enforcement.md)
  Critical: Closes all 6 root causes from INS-001 + INS-003. Mandatory scoring block, pipeline_log,
  25 artifact checklist items, Phase Tracking template. Pattern: checklists > prose for LLM enforcement.

- [009: /go scoring audit — all 15 features retrospective](009-go-scoring-audit-all-features.md)
  Medium: Validated updated scoring matrix on all features. 5 agent features changed from /plan to /feature
  after removing unfair "agent is config" signal. Confirms Insight 001 cause #5 was real.

- [006: Audit results — /go, /next, /run, /plan, /feature-ent](006-command-audit-go-next-run-plan-feature-ent.md)
  Mixed: /next 100%, /go 95%, /run 90% match. /plan has path conflict (FIXED). /feature-ent correctly absent.

- [007: Audit results — /start, /test, /deploy, /review, /docs, /myinsights](007-command-audit-start-test-deploy-review-docs-myinsights.md)
  Critical: /myinsights ~15% match (wrong storage path, missing INS-NNN system, no archive/status).
  High: /start ~40% match (missing parallelism, flags, anti-hallucination).
  Medium: /docs ~70% match (missing section templates). /test, /deploy, /review OK.

## Feature Implementation

- [002: Phase 4 REVIEW catches real issues](002-feature-review-phase-value.md)
  Medium: 7 issues found across 5 features when lifecycle is properly followed (vs 0 when skipped).

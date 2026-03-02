# Development Insights Index

## Pipeline & Workflow

- [001: /run → /go → /feature pipeline gaps](001-run-go-feature-pipeline-gaps.md)
  Critical: /run bypasses /go scoring and /feature lifecycle phases entirely. 6 root causes identified.

- [003: /feature needs mandatory artifact checklist](003-feature-lifecycle-artifact-checklist.md)
  High: Without mandatory outputs per phase, LLM skips validation and review entirely.

- [004: /feature command doesn't match its own template](004-feature-command-vs-template-mismatch.md)
  Critical: command was ad-hoc simplified instead of generated from feature-lifecycle.md template.
  Rule was correct, command was not. Root cause: /replicate Phase 3 generation gap.

## Feature Implementation

- [002: Phase 4 REVIEW catches real issues](002-feature-review-phase-value.md)
  Medium: 7 issues found across 5 features when lifecycle is properly followed (vs 0 when skipped).

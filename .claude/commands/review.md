---
description: Code review workflow using brutal-honesty-review and parallel review agents.
  Reviews staged changes or specified files for quality, security, and architecture issues.
  $ARGUMENTS: optional — file paths, "staged" (default), or "last-commit"
---

# /review $ARGUMENTS

## Purpose

Rigorous code review combining automated checks with multi-agent quality analysis.

## Step 1: Determine Scope

```
IF $ARGUMENTS is empty OR $ARGUMENTS == "staged":
    scope = git diff --staged (staged changes)
IF $ARGUMENTS == "last-commit":
    scope = git diff HEAD~1 (last commit changes)
ELSE:
    scope = specified file paths
```

## Step 2: Automated Checks

Run in parallel:
1. `ruff check .` — linting
2. `ruff format --check .` — formatting
3. `bandit -r src/ -ll` — security scan
4. `pytest tests/unit/ -q` — quick unit tests

Report any failures before proceeding to agent review.

## Step 3: Multi-Agent Review

Read the brutal-honesty-review skill from `.claude/skills/brutal-honesty-review/SKILL.md`

Use swarm of review agents:

| Agent | Focus | Weight |
|-------|-------|--------|
| code-quality | Clean code, patterns, naming, DRY | 0.25 |
| architecture | Consistency with project architecture, multi-tenant isolation | 0.25 |
| security | Input validation, auth, SQL injection, XSS, secrets in code | 0.25 |
| performance | Async patterns, N+1 queries, connection pooling | 0.15 |
| testing | Missing tests, edge cases, mock quality | 0.10 |

## Step 4: Report

```
Code Review: <scope>

Automated Checks:
   ruff check:    PASS/FAIL
   ruff format:   PASS/FAIL
   bandit:        PASS/FAIL
   unit tests:    PASS/FAIL (<N> tests)

Agent Review:
   CRITICAL: <count> issues (must fix)
   MAJOR:    <count> issues (should fix)
   MINOR:    <count> issues (nice to fix)
   INFO:     <count> suggestions

Details:
   [issue-by-issue breakdown with file:line references]

Verdict: APPROVE / REQUEST CHANGES / BLOCK
```

## Step 5: Fix Critical Issues

If CRITICAL issues found:
1. Fix each critical issue
2. Re-run affected automated checks
3. Commit fixes: `fix: address review findings`
4. Re-run review on fixes only

## Notes

- Never approve code with CRITICAL issues
- Security findings are always treated as CRITICAL
- Multi-tenant isolation violations are always CRITICAL
- Provide specific file:line references for every finding

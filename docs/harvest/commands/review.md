# Command: /review

## Maturity: Alpha v1.0

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

---

## When to Use

- Before merging a feature branch into the main branch
- After completing a significant implementation milestone
- When refactoring core modules and needing confidence in the change
- When onboarding a new contributor whose code needs thorough review
- As a pre-deployment quality gate in the CI/CD pipeline

## When NOT to Use

- For trivial changes (typo fixes, config value updates, dependency bumps with no code change)
- When only documentation files are modified (use a lighter review process)
- During rapid prototyping where code quality is intentionally deferred
- When the codebase has no linter or test infrastructure configured (set those up first)

## Prerequisites

- A configured linter for the project's primary language(s) (e.g., `ruff`, `eslint`, `clippy`)
- A security scanner available in the environment (e.g., `bandit`, `semgrep`, `npm audit`)
- A test suite that can be invoked from the command line
- Agent definitions for the review panel (can use defaults if not customized)

## Command Specification

### Purpose

Execute a structured, multi-pass code review that combines automated tooling (linter, security scanner, test runner) with independent agent-based evaluation across multiple quality dimensions. Produces a single aggregate score with a pass/fail determination.

### Invocation

```
/review [scope]
```

Where `[scope]` is optional and can be:
- A file path or glob pattern (e.g., `src/api/**/*.py`)
- A branch name to diff against main
- Omitted to review all staged/uncommitted changes

### Review Pipeline

```
Phase 1: Automated Checks (parallel)
  ├── Linter (language-appropriate)
  ├── Security Scanner
  ├── Test Runner (affected tests only)
  └── Build Verification (if applicable)

Phase 2: Agent Review Panel (parallel, isolated)
  ├── Code Quality Agent
  ├── Architecture Agent
  ├── Security Agent
  ├── Performance Agent
  └── Testing Agent

Phase 3: Score Aggregation
  └── Weighted average → pass/fail decision
```

### Phase 1: Automated Checks

Each automated check runs independently and produces a binary pass/fail plus a findings list:

| Check | Tool (configurable) | Fail Condition |
|-------|---------------------|----------------|
| Lint | Project linter | Any error-level finding |
| Security | Project security scanner | Any high/critical finding |
| Tests | Project test runner | Any test failure |
| Build | Project build command | Non-zero exit code |

If any automated check fails, the review halts and reports findings. Agent review is not invoked until all automated checks pass (to avoid wasting compute on code that has obvious issues).

### Phase 2: Agent Review Panel

Five review agents evaluate the code independently. Each agent receives the same diff/changeset and produces:
- A score from 1 to 10
- A list of findings (issues, suggestions, commendations)
- A severity classification per finding (critical, major, minor, suggestion)

| Agent | Focus Area | Evaluates |
|-------|-----------|-----------|
| Code Quality | Readability, naming, complexity, DRY | Style consistency, cyclomatic complexity, naming conventions, dead code |
| Architecture | Design patterns, separation of concerns | Module boundaries, dependency direction, abstraction levels, coupling |
| Security | Vulnerability, data handling, auth | Input validation, secret exposure, injection risks, auth bypass |
| Performance | Efficiency, resource usage | N+1 queries, unnecessary allocations, missing indexes, algorithm complexity |
| Testing | Test coverage, test quality | Coverage gaps, assertion quality, edge case coverage, mock appropriateness |

**Isolation requirement**: Each agent operates independently and does not see other agents' scores or findings before submitting its own evaluation. This prevents conformity bias.

### Phase 3: Score Aggregation

```
final_score = sum(agent_score * agent_weight) / sum(weights)
```

Default weights:

| Agent | Weight |
|-------|--------|
| Code Quality | 0.20 |
| Architecture | 0.25 |
| Security | 0.25 |
| Performance | 0.15 |
| Testing | 0.15 |

**Pass/fail threshold**: configurable, default `7.0` out of 10.

**Disagreement escalation**: If the maximum score minus the minimum score across agents exceeds 3.0 points, a meta-review is triggered to reconcile the divergence and produce a consensus assessment.

### Output Format

```markdown
# Code Review Report

## Automated Checks
- [PASS/FAIL] Lint: N findings
- [PASS/FAIL] Security: N findings
- [PASS/FAIL] Tests: N passed, N failed
- [PASS/FAIL] Build: success/failure

## Agent Scores
| Agent | Score | Critical | Major | Minor | Suggestions |
|-------|-------|----------|-------|-------|-------------|
| Code Quality | X.X | N | N | N | N |
| Architecture | X.X | N | N | N | N |
| Security | X.X | N | N | N | N |
| Performance | X.X | N | N | N | N |
| Testing | X.X | N | N | N | N |

## Aggregate Score: X.X / 10.0 — [PASS/FAIL]

## Findings
[Grouped by severity, then by agent]

## Recommendations
[Prioritized list of changes needed before merge]
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `pass_threshold` | `7.0` | Minimum aggregate score to pass |
| `disagreement_threshold` | `3.0` | Score spread that triggers meta-review |
| `weights` | See table above | Per-agent scoring weights |
| `skip_agents` | `[]` | List of agent names to exclude from review |
| `auto_checks` | `["lint", "security", "tests", "build"]` | Automated checks to run |
| `fail_on_critical` | `true` | Whether any critical finding auto-fails the review regardless of score |

## Variants

| Variant | Description |
|---------|-------------|
| `/review --quick` | Run automated checks only, skip agent panel |
| `/review --security-only` | Run only the security scanner and security agent |
| `/review --agents-only` | Skip automated checks, run agent panel directly |
| `/review --report [path]` | Write review report to a file instead of stdout |
| `/review --fix` | After review, attempt to auto-fix findings that have deterministic resolutions |

## Gotchas

- **Score inflation**: If all agents consistently score above 8.5 on first review, the agent prompts may need calibration. Add adversarial instructions to the critic agent.
- **Automated check flakiness**: Flaky tests will block the review pipeline. Quarantine known-flaky tests before running `/review`.
- **Large diffs**: Reviews of 1000+ line diffs produce lower-quality agent feedback. Break large changes into smaller, reviewable units.
- **Weight tuning**: Default weights are general-purpose. Security-critical projects should increase the security agent weight; UI-heavy projects may increase code quality weight.
- **Agent model selection**: Review agents should use a capable model (not the cheapest tier). Cheap models produce shallow reviews that miss architectural issues.
- **False sense of security**: A passing score does not guarantee bug-free code. The review is an additional quality signal, not a replacement for manual review on critical paths.

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-02 | Initial extraction. Five-agent panel, automated pre-checks, weighted scoring. |

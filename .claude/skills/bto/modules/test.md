# TEST Module — Multi-Agent Evaluation Protocol

## Purpose

Evaluate any Claude Code artifact (skill, command, rule, agent template) using layered evaluation: deterministic pre-checks, single-judge quick eval, and full 3-judge panel.

## Input

- **Path:** Path to artifact file or directory
- **Level:** layer0 | layer1 | layer2 | full (default: full)
- **Artifact type:** auto-detected from path/content

## Type Detection

| Path Pattern | Detected Type |
|-------------|--------------|
| `.claude/skills/*/SKILL.md` | skill |
| `.claude/skills/*/` (directory) | skill |
| `.claude/commands/*.md` | command |
| `.claude/rules/*.md` | rule |
| `.claude/agents/*.md` | agent |
| `researches/**/*.md` | research artifact |

---

## Layer 0: Deterministic Pre-checks

**Cost:** Zero (no LLM calls)
**Speed:** Instant
**Purpose:** Catch structural issues before expensive LLM evaluation

### Universal Checks (all types)

```
CHECK-U1: File exists and is non-empty
CHECK-U2: File is valid UTF-8 text
CHECK-U3: Has at least one markdown heading (#)
CHECK-U4: No consecutive empty lines (> 2)
CHECK-U5: File size within bounds (see per-type limits)
```

### Skill Checks

```
CHECK-S1: SKILL.md exists in skill directory
CHECK-S2: Has "# Title" as first heading
CHECK-S3: Has "## Overview" or "## Purpose" section
CHECK-S4: Has "## Anti-Patterns" section
CHECK-S5: All files in modules/ referenced in SKILL.md
CHECK-S6: All files in references/ referenced in SKILL.md
CHECK-S7: No empty sections (heading → next heading with no content)
CHECK-S8: Size: 1KB < SKILL.md < 50KB
CHECK-S9: Total directory size < 200KB
CHECK-S10: At least one file in references/ OR examples/
```

### Command Checks

```
CHECK-C1: Contains "$ARGUMENTS" or parameter reference
CHECK-C2: Has checkpoint banner or protocol
CHECK-C3: Has skill loading instruction (Read *.SKILL.md)
CHECK-C4: Size: 500B < file < 20KB
CHECK-C5: Has "## Usage" or "## Protocol" section
```

### Rule Checks

```
CHECK-R1: Has table or structured list of patterns
CHECK-R2: Each pattern has detection signal and fix
CHECK-R3: Size: 200B < file < 10KB
CHECK-R4: Has "Auto-Detection" or similar section
```

### Agent Template Checks

```
CHECK-A1: Specifies model (haiku/sonnet/opus)
CHECK-A2: Specifies isolation scope
CHECK-A3: Has prompt template or instructions
CHECK-A4: Size: 200B < file < 10KB
```

### Layer 0 Scoring

- Each check: PASS (1) or FAIL (0)
- Score = passed / total
- **Gate: score ≥ 0.80 to proceed to Layer 1+**
- If score < 0.80: return report with specific failures, skip LLM evaluation

### Layer 0 Output

```
═══════════════════════════════════════════════════════
📋 LAYER 0: Deterministic Pre-checks
Artifact: <path>
Type: <detected type>

Results: X/Y passed (Z%)

✅ CHECK-S1: SKILL.md exists
✅ CHECK-S2: Has title heading
❌ CHECK-S7: Empty section found at line 45
...

Gate: PASS ✅ / FAIL ❌
═══════════════════════════════════════════════════════
```

---

## Layer 1: Single LLM Judge (Quick)

**Cost:** Low (1 haiku call)
**Speed:** ~10 seconds
**Purpose:** Fast quality signal for iteration or batch evaluation

### Model Selection

- Default: **haiku** (cost-optimized)
- For critical artifacts: **sonnet**

### Judge Prompt

```
You are evaluating a Claude Code {artifact_type}.

## Artifact Content
{content}

## Evaluation Dimensions

Rate each dimension 1-10:

1. CLARITY (Are instructions unambiguous? Can an LLM follow them precisely?)
2. COMPLETENESS (Are all necessary sections present? No missing pieces?)
3. ACTIONABILITY (Can Claude produce concrete output from these instructions?)
4. QUALITY (Well-structured? Professional? Good formatting?)
5. ANTI-PATTERNS (Avoids known pitfalls? Has failure mode coverage?)

## Required Output Format

SCORES:
- CLARITY: X/10 — [one-line justification]
- COMPLETENESS: X/10 — [one-line justification]
- ACTIONABILITY: X/10 — [one-line justification]
- QUALITY: X/10 — [one-line justification]
- ANTI-PATTERNS: X/10 — [one-line justification]

AVERAGE: X.X/10

TOP 3 IMPROVEMENTS:
1. [specific, actionable suggestion]
2. [specific, actionable suggestion]
3. [specific, actionable suggestion]

VERDICT: PASS (≥7.0) / NEEDS WORK (5.0-6.9) / FAIL (<5.0)
```

### Layer 1 Gate

- Average ≥ 7.0: PASS
- Average 5.0-6.9: NEEDS WORK (can proceed to Layer 2 for detailed feedback)
- Average < 5.0: FAIL (fix before proceeding)

---

## Layer 2: Full Judge Panel (3 Agents)

**Cost:** Moderate (3 sonnet calls)
**Speed:** ~30 seconds (parallel)
**Purpose:** Comprehensive, multi-perspective evaluation

### Architecture

Spawn 3 agents in parallel using Agent tool:

```
Agent 1: "BTO Judge — Domain Expert"    model: sonnet
Agent 2: "BTO Judge — Critic"            model: sonnet
Agent 3: "BTO Judge — Completeness"      model: sonnet
```

**Isolation:** Each agent reads the same artifact independently. No cross-communication.

### Judge 1: Domain Expert

Focus: Is the content technically sound and appropriate for the domain?

```
You are a Domain Expert evaluator for Claude Code artifacts.

Evaluate this {artifact_type} for technical quality:

{content}

Score 1-10 on each dimension:
1. METHODOLOGY — Is the approach well-designed? Sound structure?
2. DEPTH — Sufficient detail for the task? Not too shallow?
3. CORRECTNESS — Are all claims and instructions valid?
4. USABILITY — Can a user/agent effectively use this?
5. ROBUSTNESS — Handles edge cases and failure modes?

For each dimension provide:
- Score (1-10)
- 2-3 sentence justification
- One specific improvement suggestion

OVERALL_SCORE: weighted average
CONFIDENCE: HIGH/MEDIUM/LOW
KEY_STRENGTHS: [top 2]
KEY_WEAKNESSES: [top 2]
```

### Judge 2: Critic

Focus: Find weaknesses, gaps, and anti-patterns.

```
You are a Critical Evaluator. Your job is to find problems.

Evaluate this {artifact_type} adversarially:

{content}

Score 1-10 on each dimension (be strict — average should be ~5-6):
1. METHODOLOGY — Any logical flaws or unjustified assumptions?
2. DEPTH — What's missing? What's under-specified?
3. CORRECTNESS — Any instructions that could mislead or produce wrong output?
4. USABILITY — What would confuse a user? Where would someone get stuck?
5. ROBUSTNESS — What breaks this? What edge cases are unhandled?

For each dimension provide:
- Score (1-10) — err on the side of strict
- 2-3 sentence justification focusing on PROBLEMS
- One specific failure scenario

OVERALL_SCORE: weighted average
CRITICAL_ISSUES: [list of blocking problems]
IMPROVEMENT_PRIORITY: [ordered list of what to fix first]
```

### Judge 3: Completeness Auditor

Focus: Structural completeness and cross-reference integrity.

```
You are a Completeness Auditor for Claude Code artifacts.

Audit this {artifact_type} for structural completeness:

{content}

Score 1-10 on each dimension:
1. METHODOLOGY — Does the structure follow established patterns?
2. DEPTH — Is every section adequately populated?
3. CORRECTNESS — Do all cross-references resolve? Are all claims supported?
4. USABILITY — Is the information well-organized and findable?
5. ROBUSTNESS — Are failure modes documented? Are anti-patterns listed?

For each dimension provide:
- Score (1-10)
- 2-3 sentence justification
- Missing element (if any)

OVERALL_SCORE: weighted average
MISSING_SECTIONS: [list]
BROKEN_REFERENCES: [list]
COVERAGE_GAPS: [list]
```

### Score Aggregation

After all 3 judges return:

**Weights:**
- Domain Expert: 0.40
- Critic: 0.30
- Completeness Auditor: 0.30

**Per-dimension:**
```
dimension_score = expert[dim] * 0.4 + critic[dim] * 0.3 + auditor[dim] * 0.3
```

**Overall:**
```
overall = mean(all dimension_scores)
```

**Disagreement Detection:**
For each dimension, if `max(scores) - min(scores) > 3` → FLAG for meta-judge.

---

## Meta-Judge: Disagreement Resolution

**Trigger:** Any flagged dimension from Layer 2.

**Model:** default (opus)

**Prompt:**
```
Three judges evaluated a Claude Code artifact and disagreed significantly
on the following dimension(s): {flagged_dimensions}

Judge 1 (Domain Expert): {score} — {justification}
Judge 2 (Critic): {score} — {justification}
Judge 3 (Completeness): {score} — {justification}

Reconcile these scores. Provide:
1. Your reconciled score (1-10) with reasoning
2. Which judge(s) had the most valid perspective and why
3. Whether this needs human review (YES/NO)
```

---

## Output: Evaluation Report

Format defined in `examples/sample-eval-report.md`.

Summary structure:
```
═══════════════════════════════════════════════════════
📊 BTO EVALUATION REPORT
Artifact: <path>
Type: <type>
Level: Layer 0 + Layer 1 + Layer 2

OVERALL SCORE: X.X / 10  [PASS / NEEDS WORK / FAIL]

Per-Dimension:
  METHODOLOGY:  X.X  ██████████░░
  DEPTH:        X.X  ████████░░░░
  CORRECTNESS:  X.X  █████████░░░
  USABILITY:    X.X  ██████████░░
  ROBUSTNESS:   X.X  ███████░░░░░

Flagged: [dimensions with >3 disagreement]

Top Improvements:
1. ...
2. ...
3. ...
═══════════════════════════════════════════════════════
```

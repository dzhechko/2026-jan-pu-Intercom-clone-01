# OPTIMIZE Module — Evolutionary Prompt Optimization Protocol

## Purpose

Improve Claude Code artifacts through evolutionary prompt optimization: generate variants, evaluate, select, mutate, repeat.

## Input

- **Path:** Path to artifact to optimize
- **Rounds:** Number of optimization rounds (default: 3, max: 5)
- **Budget:** max evaluations (default: 15)
- **Focus:** Optional dimension to prioritize (METHODOLOGY / DEPTH / CORRECTNESS / USABILITY / ROBUSTNESS)

## Prerequisites

- Artifact must pass Layer 0 checks (run TEST first)
- Baseline score established (Layer 2 evaluation)
- Only optimize if baseline < 8.0 (otherwise artifact is already good)

---

## Protocol

### Step 1: Baseline Evaluation

1. Run TEST module with level=layer2 on current artifact
2. Record:
   - Per-dimension scores
   - Overall score
   - Key weaknesses identified by judges
3. If overall ≥ 8.0 → report "Artifact already high quality" and suggest minor tweaks only
4. Identify **target dimensions**: dimensions scoring < 7.0

### Step 2: Variant Generation (Round 1)

Generate N=5 variants of the artifact. Each variant applies ONE mutation strategy.

**Mutation Assignment:**
- Variant 1: **Rephrase** — reword unclear instructions for precision
- Variant 2: **Restructure** — reorganize sections for better flow
- Variant 3: **Add Constraints** — add guardrails, edge cases, boundary conditions
- Variant 4: **Simplify** — remove redundancy, tighten language, reduce verbosity
- Variant 5: **Specialize** — add domain-specific context and examples

**Strategy-to-Weakness Mapping:**

| Weak Dimension | Primary Strategy | Secondary Strategy |
|---------------|-----------------|-------------------|
| METHODOLOGY | Restructure | Add Constraints |
| DEPTH | Specialize | Add Constraints |
| CORRECTNESS | Add Constraints | Rephrase |
| USABILITY | Rephrase | Restructure |
| ROBUSTNESS | Add Constraints | Specialize |

If a focus dimension is specified, generate 3 variants targeting that dimension's strategies and 2 variants with other strategies.

### Variant Generation Prompt

```
You are optimizing a Claude Code {artifact_type}.

## Current Artifact
{content}

## Baseline Evaluation
Overall: {score}/10
Weaknesses: {weaknesses}
Target dimensions: {target_dimensions}

## Mutation Strategy: {strategy_name}
{strategy_description}

## Task
Apply the {strategy_name} mutation to improve this artifact.
Focus on addressing these specific weaknesses: {target_weaknesses}

Rules:
- Preserve the original intent and scope
- Maintain all existing sections
- Do not change the artifact type or structure fundamentally
- Changes should be targeted and purposeful
- Output the COMPLETE modified artifact (not a diff)
```

### Step 3: Evaluate Variants (Round 1)

Run TEST module with level=layer1 (haiku — fast and cheap) on each variant.

**Parallel execution:** Spawn 5 agents (model: haiku), one per variant.

Record scores for all 5 variants.

### Step 4: Selection + Crossover

1. **Select:** Top 2 variants by overall score
2. **Crossover:** Combine best elements:
   - Take sections where Variant A scored higher from A
   - Take sections where Variant B scored higher from B
   - Generate 3 new variants from the crossover

**Crossover Prompt:**
```
You are creating an improved Claude Code artifact by combining the best
elements of two high-scoring variants.

## Variant A (Score: {score_a})
{variant_a}
Strengths: {strengths_a}

## Variant B (Score: {score_b})
{variant_b}
Strengths: {strengths_b}

## Task
Create a new variant that combines the strengths of both:
- From A, take: {specific_sections_a}
- From B, take: {specific_sections_b}
- Ensure coherence and consistency
- Output the COMPLETE artifact
```

### Step 5: Evaluate + Select (Rounds 2-3)

**Round 2:**
- Evaluate 3 crossover variants with Layer 1
- Select top 2
- Generate 3 new crossover variants

**Round 3 (Final):**
- Evaluate 3 final variants with **Layer 2** (full judge panel — thorough)
- Select the single best variant

### Step 6: Output

1. **Best variant** — the optimized artifact
2. **Before/After comparison:**
   ```
   ═══════════════════════════════════════════════════════
   🔧 BTO OPTIMIZATION REPORT
   Artifact: <path>
   Rounds: 3
   Total evaluations: 15

   BEFORE → AFTER:
     METHODOLOGY:  6.2 → 8.1  (+1.9) ⬆️
     DEPTH:        5.8 → 7.5  (+1.7) ⬆️
     CORRECTNESS:  7.0 → 8.3  (+1.3) ⬆️
     USABILITY:    6.5 → 8.0  (+1.5) ⬆️
     ROBUSTNESS:   5.5 → 7.8  (+2.3) ⬆️

     OVERALL:      6.2 → 7.9  (+1.7) ⬆️

   Winning Strategy: Restructure + Add Constraints (crossover)

   CHANGELOG:
   - Restructured protocol into clearer numbered steps
   - Added edge case handling for empty inputs
   - Expanded anti-patterns with 3 new entries
   - Simplified module loading instructions
   - Added concrete examples to each section
   ═══════════════════════════════════════════════════════
   ```

3. **Recommendation:**
   - If improvement > 1.0: "Apply changes"
   - If improvement 0.5-1.0: "Review changes, consider applying"
   - If improvement < 0.5: "Minimal improvement — original may be preferred"

---

## Cost Summary

| Operation | Count | Model | Est. Tokens |
|-----------|-------|-------|-------------|
| Baseline eval | 1 | sonnet ×3 | ~15K |
| Variant generation | 5 | opus | ~25K |
| Round 1 eval | 5 | haiku | ~10K |
| Crossover generation | 3 | opus | ~15K |
| Round 2 eval | 3 | haiku | ~6K |
| Crossover generation | 3 | opus | ~15K |
| Round 3 eval | 3 | sonnet ×3 | ~45K |
| **Total** | | | **~131K tokens** |

## Anti-Patterns

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| Overfitting to one metric | One dimension +3, others flat or down | Balance mutations across dimensions |
| Losing generality | Specialized variant breaks other use cases | Test with multiple example inputs |
| Infinite loop | > 5 rounds without improvement | Hard cap at configured rounds |
| Semantic drift | Optimized version changes intent | Compare purpose statement before/after |
| Premature optimization | Baseline ≥ 8.0 | Skip optimization, suggest minor tweaks |
| Score inflation | Haiku gives high scores to everything | Calibrate with sonnet baseline |

## Abort Conditions

Stop optimization immediately if:
1. Any round shows overall regression > 0.5 from baseline
2. Critical structural checks (Layer 0) fail on any variant
3. Artifact semantics change fundamentally
4. User requests stop

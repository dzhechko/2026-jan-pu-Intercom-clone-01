# Rule: Generate Documentation from Existing Code Using Parallel Agents

## Maturity: 🔴 Alpha

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

## Rule

When a codebase has accumulated significant documentation debt, use parallel LLM agents to generate documentation retroactively from existing source code. Each agent operates independently: reads a defined subset of source files and produces one or more documentation artifacts.

Key parameters:
- **Agent count (N)**: Number of parallel agents, typically matching the number of source modules or documentation categories
- **Scope per agent**: Each agent is assigned a specific subset of files (e.g., one module, one service, one API group)
- **Output per agent**: Each agent produces a fixed set of documentation files (e.g., module overview, API reference, configuration guide)
- **Isolation**: Agents do not communicate with each other during generation. Cross-references are resolved in a post-processing pass.

This approach is a remediation strategy, not a best practice. Upfront documentation written alongside code is always preferable.

## Why

Documentation debt compounds. Once a codebase reaches a certain size without documentation, the cost of writing docs for the entire codebase in a single pass becomes prohibitive. Developers avoid the task because it is overwhelming, and the debt grows further.

Parallel LLM agents can process the entire codebase simultaneously. The approach scales linearly: N agents processing M modules each produces N*M documentation files in roughly the time it takes one agent to process M files. Observed throughput: 14 agents producing 5 documents each generated 70 files in approximately 3 minutes.

The tradeoff is quality: retroactive documentation describes what the code IS, not what it was INTENDED to be. Design rationale, rejected alternatives, and historical context are lost. This makes retroactive docs less valuable than upfront docs, but far more valuable than no docs.

## Example (what goes wrong)

A team decides to write documentation for a 50-module codebase that has been developed over 6 months with no documentation:

```
Approach: Assign one developer to write all documentation
Timeline: "We'll do it next sprint"
Result: 3 months later, 2 modules documented, 48 remaining
         Developer context-switches to feature work
         Documentation effort abandoned
```

Alternatively, a single LLM agent is tasked with documenting the entire codebase sequentially:

```
Approach: One LLM agent processes all 50 modules
Timeline: Agent runs for 2 hours, context window fills, quality degrades
Result: First 15 modules well-documented, remaining 35 have
        shallow, repetitive documentation due to context fatigue
```

## Correct Approach

```
Step 1: Inventory
  - List all source modules/services (e.g., 14 modules)
  - Define documentation types per module (e.g., 5 types: overview, API, config, data model, error handling)
  - Total output: 14 x 5 = 70 documentation files

Step 2: Agent Assignment
  - Spawn 14 parallel agents
  - Each agent receives:
    - The source files for one module (read-only)
    - A documentation template for each of the 5 types
    - Project-level context (architecture overview, naming conventions)
  - Each agent produces 5 documentation files independently

Step 3: Parallel Execution
  - All 14 agents run concurrently
  - Expected time: ~3 minutes (limited by the slowest agent)
  - Expected output: 70 documentation files

Step 4: Post-Processing
  - Resolve cross-references between modules
  - Check for contradictions between agents' descriptions of shared interfaces
  - Generate a top-level index/table of contents
  - Human review of generated documentation for accuracy

Step 5: Acknowledge Limitations
  - Mark generated docs as "auto-generated from source code"
  - Flag sections where design rationale is missing
  - Create follow-up tasks to add rationale and context manually
```

Important caveats:
- Retroactive docs describe WHAT IS, not WHY. Design decisions, rejected alternatives, and historical context must be added manually.
- Quality depends on code readability. Poorly-named functions and missing comments produce poor documentation.
- Cross-module interactions may be missed when agents operate in isolation. The post-processing pass is essential.

## Scope

Any project with accumulated documentation debt:
- Legacy codebases with no documentation
- Rapid prototypes that evolved into production systems
- Projects after team turnover where institutional knowledge was lost
- Open source projects needing contributor documentation

Applicable to any programming language or framework. The parallel agent approach is language-agnostic; only the documentation templates need to be domain-specific.

Not a replacement for writing documentation alongside code. Use this as a one-time remediation, then establish practices to maintain documentation going forward.

## Expiry

Review after 12 months. The parallel agent approach depends on current LLM capabilities (context window size, code comprehension quality). As models improve, the agent-per-module granularity may shift (fewer, more capable agents covering more modules each).

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction. Demonstrated with 14 parallel agents generating 70 documentation files in ~3 minutes for a codebase with zero prior documentation. |

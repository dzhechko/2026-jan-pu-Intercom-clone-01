# BUILD Module — Artifact Generation Protocol

## Purpose

Generate production-quality Claude Code artifacts (skills, commands, rules, agent templates) from natural language requirements.

## Input

- **Description:** Natural language description of what the artifact should do
- **Type:** skill | command | rule | agent (auto-detected or explicit)
- **Mode:** QUICK | DEEP (default: QUICK)
- **References:** Optional paths to existing artifacts as examples

## Protocol

### Step 1: Type Detection

If type is not explicitly specified, detect from description:

| Signal | Detected Type |
|--------|--------------|
| "skill", "module", "capability", "protocol" | skill |
| "command", "slash command", "/something", "pipeline" | command |
| "rule", "constraint", "convention", "anti-pattern" | rule |
| "agent", "worker", "parallel", "swarm" | agent |

### Step 2: Requirements Gathering

**QUICK mode** — Extract from description directly:
1. Parse artifact name (kebab-case)
2. Extract key capabilities
3. Identify domain constraints
4. Proceed to generation

**DEEP mode** — Use `explore` skill:
1. Read `.claude/skills/explore/SKILL.md`
2. Follow explore protocol to clarify:
   - Exact scope and boundaries
   - Target users/consumers
   - Input/output format
   - Quality criteria
   - Edge cases
3. Produce requirements brief
4. Confirm with user before generation

### Step 3: Generation Templates

#### Skill Template

```
.claude/skills/<name>/
├── SKILL.md
│   ├── # <Name>
│   ├── ## Overview
│   ├── ## Quick Start
│   ├── ## Protocol
│   │   ├── Step 1: ...
│   │   ├── Step 2: ...
│   │   └── Step N: ...
│   ├── ## Output Format
│   ├── ## Anti-Patterns
│   └── ## Dependencies
├── modules/          (if multi-module)
│   └── <module>.md
├── references/       (always include at least one)
│   └── <ref>.md
└── examples/         (always include at least one)
    └── <example>.md
```

#### Command Template

```markdown
# /command-name — Short Description

## Usage
/command-name [arguments]

## Parameters
- $ARGUMENTS — Description

## Protocol

### Step 1: Setup
- Validate arguments
- Load required skills: Read `.claude/skills/<skill>/SKILL.md`

### Step 2: Execution
- Main logic here
- Use Agent tool for parallelism where applicable

### Step 3: Output
- Create artifact files
- Display checkpoint

## Checkpoint
═══════════════════════════════════════════════════════
⏸️ CHECKPOINT: [Command Name] Complete
...
═══════════════════════════════════════════════════════
```

#### Rule Template

```markdown
# Rule Name

## Patterns

| Pattern | Detection Signal | Required Fix |
|---------|-----------------|-------------|
| ... | ... | ... |

## Auto-Detection
When generating content, self-check against these patterns.
If detected, flag with ⚠️ and fix before proceeding.
```

#### Agent Template

```markdown
# Agent Name

## Purpose
What this agent does.

## Configuration
- Model: haiku | sonnet | opus
- Isolation: reads X, writes Y
- Max turns: N

## Prompt Template
```

### Step 4: Self-Review

After generation, validate against quality checklist:

1. **Structure check:**
   - Required sections present for artifact type
   - No empty sections
   - Proper markdown formatting

2. **Content check:**
   - No generic/placeholder content
   - Specific to the domain
   - Anti-patterns section populated
   - At least one concrete example

3. **Convention check:**
   - File naming: kebab-case
   - Directory naming: kebab-case
   - Heading hierarchy: proper nesting
   - References resolve to actual files

4. **Size check:**
   - SKILL.md: 2KB-30KB (ideal: 5KB-15KB)
   - Module: 1KB-15KB
   - Reference: 500B-10KB
   - Example: 500B-5KB

### Step 5: Output

1. Create all files in the target directory
2. Display summary:
   ```
   ✅ BUILD Complete
   Artifact: .claude/skills/<name>/
   Files created:
     - SKILL.md (X KB)
     - modules/<m>.md (X KB)
     - references/<r>.md (X KB)
     - examples/<e>.md (X KB)

   Next: Run /bto-test .claude/skills/<name>/ to evaluate
   ```

## Anti-Patterns

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| Generic skill | No domain-specific terms | Add domain context and constraints |
| Missing references | references/ empty | Add at least one reference file |
| No examples | examples/ empty | Add at least one few-shot example |
| Over-scoped | SKILL.md > 30KB | Split into modules |
| Under-specified | SKILL.md < 2KB | Expand with more detail |
| Copy-paste | Identical to another skill | Adapt uniquely |
| Missing anti-patterns | No anti-patterns section | Add common failure modes |
| No output format | Doesn't specify expected output | Add explicit output section |

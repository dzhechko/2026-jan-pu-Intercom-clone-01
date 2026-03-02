# Command: /myinsights

## Maturity: Alpha v1.0

## Used in: ai-consultant-cloud-ru

## Extracted: 2026-03-02

## Version: v1.0

---

## When to Use

- After resolving a non-trivial bug or unexpected behavior during development
- When discovering an undocumented quirk in a dependency, framework, or tool
- When a workaround is applied that future developers need to know about
- When a pattern emerges across multiple debugging sessions (recurring class of error)
- During post-incident review to capture root cause and resolution
- When onboarding reveals knowledge gaps that should be documented

## When NOT to Use

- For routine changes that follow established patterns (standard CRUD, config tweaks)
- For information already covered in official documentation of the tools in use
- For temporary debugging notes that have no long-term value
- When the insight is specific to a single throwaway experiment

## Prerequisites

- A `docs/myinsights/` directory at the project root (created automatically on first run)
- Write access to the project repository
- Familiarity with the naming convention `INS-NNN` for insight files

## Command Specification

### Purpose

Capture development learnings, error resolutions, and discovered patterns as structured, searchable insight files. Each insight is a self-contained knowledge unit with metadata for deduplication, status tracking, and retrieval.

### Invocation

```
/myinsights
```

The command runs interactively. It inspects recent work context (git diff, recent errors, conversation history) and proposes an insight to capture. The developer confirms, edits, or rejects.

### Insight File Format

Each insight is stored as a Markdown file in `docs/myinsights/` with the naming pattern `INS-NNN-short-slug.md`:

```markdown
# INS-NNN: [Title]

## Status: [active | workaround | obsolete]
## Hits: [N]
## Created: [YYYY-MM-DD]
## Last Hit: [YYYY-MM-DD]
## Tags: [tag1, tag2, ...]

## Error Signature
[Regex or literal string that identifies this error in logs/output]

## Problem
[Description of the problem encountered]

## Root Cause
[Why the problem occurs]

## Solution
[How to fix or work around the problem]

## Context
[When/where this is likely to occur — environment, versions, conditions]

## References
[Links to issues, docs, Stack Overflow, etc.]
```

### Core Features

1. **Error Signature Matching**: Each insight includes a regex or literal error signature. When the command runs, it scans recent output for matches against existing insights and surfaces them before creating duplicates.

2. **Duplicate Detection**: Before creating a new insight, the command searches existing insights by:
   - Error signature similarity (fuzzy match against the `Error Signature` field)
   - Title/tag overlap (keyword intersection above a configurable threshold)
   - If a match is found, the existing insight's `Hits` counter is incremented and `Last Hit` date is updated instead of creating a duplicate.

3. **Hit Counter**: Every time an existing insight is matched (via signature or manual reference), its `Hits` field increments. High-hit insights surface first in search results, indicating recurring problems.

4. **Status Tracking**:
   - `active` — The problem and solution are current and verified.
   - `workaround` — A temporary fix is in place; a proper solution is pending.
   - `obsolete` — The problem no longer applies (dependency updated, code removed, etc.).

5. **Index Generation**: After every write operation, the command regenerates `docs/myinsights/index.md` containing:
   - Table of all insights sorted by hits (descending)
   - Columns: ID, Title, Status, Hits, Tags, Created, Last Hit
   - Filter sections by status (active, workaround, obsolete)

### Workflow

```
1. /myinsights triggered
2. Scan recent context (git diff, error output, conversation)
3. Extract candidate insight (title, error signature, problem, solution)
4. Search existing insights for duplicates
   4a. If duplicate found → increment hit counter, update last-hit date, show existing insight
   4b. If no duplicate → assign next INS-NNN ID, create new file
5. Prompt developer to confirm/edit the insight
6. Write insight file to docs/myinsights/
7. Regenerate docs/myinsights/index.md
8. Commit insight file (optional, based on project workflow)
```

### Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `insights_dir` | `docs/myinsights/` | Directory for insight storage |
| `duplicate_threshold` | `0.7` | Similarity score above which an insight is considered duplicate |
| `auto_commit` | `false` | Whether to auto-commit new insights |
| `max_insights` | `999` | Maximum number of insights before archival prompt |

## Variants

| Variant | Description |
|---------|-------------|
| `/myinsights search [query]` | Search existing insights by keyword, tag, or error signature |
| `/myinsights status [INS-NNN] [new-status]` | Update the status of an existing insight |
| `/myinsights report` | Generate a summary report of insight statistics (total, by status, top hits) |
| `/myinsights prune` | Interactively review and archive obsolete insights |

## Gotchas

- **Over-capturing**: Not every bug fix is an insight. The command should be used for patterns and non-obvious resolutions, not routine fixes. If the insight index grows beyond ~100 entries without pruning, signal quality degrades.
- **Stale workarounds**: Insights with status `workaround` should be periodically reviewed. A workaround that outlives 3 months without resolution should trigger a review prompt.
- **Signature specificity**: Error signatures that are too broad (e.g., `Error`) will match everything and inflate hit counters meaninglessly. Signatures should be specific enough to uniquely identify the class of error.
- **Index drift**: If insight files are manually edited or deleted without running the command, the index may become stale. Always use `/myinsights prune` instead of manual deletion.
- **Merge conflicts**: In multi-developer teams, simultaneous insight creation can cause ID collisions. Use a locking mechanism or assign ID ranges per developer.

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| v1.0 | 2026-03-02 | Initial extraction. Core features: capture, dedup, hit counting, index generation. |

# /plan $ARGUMENTS — Implementation Planning

## Steps

1. **Analyze the feature/task** described in $ARGUMENTS
2. **Read relevant docs:**
   - `docs/Specification.md` for user stories and acceptance criteria
   - `docs/Pseudocode.md` for algorithms and data structures
   - `docs/Architecture.md` for component placement and tech stack
   - `docs/Refinement.md` for edge cases and testing requirements
3. **Create implementation plan:**
   - List files to create/modify
   - Define implementation order (dependencies first)
   - Identify tests to write
   - Estimate complexity (S/M/L)
4. **Write plan** to `docs/features/$FEATURE_NAME.md`
5. **Auto-commit:** `docs: plan for $FEATURE_NAME`

## Plan Template

```markdown
# Feature: [name]

## User Story
[from Specification.md]

## Files to Create/Modify
1. [file] — [what changes]

## Implementation Steps
1. [step] — [details]

## Tests
1. [test file] — [what it tests]

## Edge Cases
[from Refinement.md]

## Dependencies
[what must exist first]
```

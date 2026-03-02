# /myinsights — Capture Development Insights

## Usage

- `/myinsights` — view all captured insights
- `/myinsights add [topic]` — add a new insight
- `/myinsights search [query]` — search insights by keyword

## What to Capture

- Architecture decisions made during implementation
- Performance optimization discoveries
- Integration quirks (Telegram API, Cloud.ru API, Qdrant)
- Debugging techniques that worked
- Edge cases discovered during testing
- Russian locale / i18n lessons learned

## Insight Format

```markdown
### [Topic] — [Date]

**Context:** What were you working on?
**Insight:** What did you learn?
**Impact:** How does this affect future work?
**Related:** Links to code, docs, or issues
```

## Storage

Insights are saved to `docs/insights/` directory:
- `docs/insights/architecture.md` — design decisions
- `docs/insights/performance.md` — optimization findings
- `docs/insights/integrations.md` — API quirks and workarounds
- `docs/insights/debugging.md` — troubleshooting patterns

## Auto-Capture Triggers

Insights are automatically suggested when:
- A test fails and is fixed (debugging pattern)
- A performance metric changes significantly
- A new edge case is discovered
- An integration requires a workaround

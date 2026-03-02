# Git Workflow Rules

## Branch Strategy

- `main` — production-ready code
- `feature/[name]` — feature branches from main
- `fix/[name]` — bug fix branches
- `docs/[name]` — documentation changes

## Commit Messages

Format: `type: description`

Types:
- `feat:` — new feature
- `fix:` — bug fix
- `docs:` — documentation only
- `test:` — adding/updating tests
- `refactor:` — code restructuring without behavior change
- `chore:` — maintenance tasks (deps, config)
- `perf:` — performance improvement

Examples:
```
feat: architect agent RAG pipeline with hybrid search
fix: handle empty message in Telegram webhook
test: add unit tests for TCO calculator algorithm
docs: update API endpoint documentation
```

## Commit Discipline

- Commit after each logical unit of work
- Push to GitHub after each commit
- Never commit secrets, .env files, or credentials
- Always run `ruff check .` before committing
- Keep commits focused — one feature/fix per commit

## Pre-Commit Checks

```bash
ruff check .              # linting
ruff format --check .     # formatting
pytest tests/unit/ -q     # quick unit tests
bandit -r src/ -ll        # security scan
```

## PR Workflow

1. Create feature branch
2. Implement + test
3. Run full check suite
4. Create PR with description referencing user story
5. Code review (use code-reviewer agent)
6. Merge to main

# /feature $ARGUMENTS — Feature Lifecycle

## Overview

Full feature lifecycle: plan → implement → test → review.

## Steps

### 1. Plan

- Read the relevant user story from `docs/Specification.md`
- Check acceptance criteria (Gherkin scenarios)
- Reference `docs/Pseudocode.md` for algorithms
- Reference `docs/Architecture.md` for component placement
- Create implementation plan with file list

### 2. Implement

- Create/modify files according to plan
- Follow coding standards from CLAUDE.md
- Agents are config files (prompts/*.md), not code
- Use SQLAlchemy models (no raw SQL)
- Add Pydantic schemas for API endpoints

### 3. Test

- Write tests before or alongside implementation
- Reference `docs/Refinement.md` for edge cases
- Reference `docs/test-scenarios.md` for BDD scenarios
- Run: `pytest tests/ -v --cov=src`

### 4. Review

- Run linting: `ruff check . && ruff format --check .`
- Run security scan: `bandit -r src/ -ll`
- Check test coverage ≥ 80%
- Verify Docker build: `docker compose build`

### 5. Commit

- Stage relevant files
- Commit with descriptive message: `feat: [feature-name] — [description]`
- Push to remote

## Feature Suggestions (MVP Priority)

1. `architect-agent` — Architect Agent + RAG pipeline core
2. `tco-calculator` — Cost Calculator Agent + TCO algorithm
3. `compliance-agent` — Compliance Agent (152-ФЗ, ФСТЭК)
4. `telegram-bot` — Telegram bot webhook + message handling
5. `human-escalation` — Escalation flow + SA notification
6. `admin-dashboard` — React dashboard + metrics API

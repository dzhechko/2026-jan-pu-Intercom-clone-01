# Template: pyproject.toml for Python Projects

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

A `pyproject.toml` template for Python projects using modern tooling: ruff for linting and formatting (replaces black, isort, flake8), pytest with pytest-asyncio for async tests, coverage enforcement, and optional dependency groups for development and testing.

## Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `{{PROJECT_NAME}}` | Python package/project name (lowercase, hyphens) | `my-backend` |
| `{{PROJECT_DESCRIPTION}}` | One-line project description | `REST API for widget management` |
| `{{PYTHON_VERSION}}` | Minimum Python version | `3.12` |
| `{{COVERAGE_THRESHOLD}}` | Minimum test coverage percentage | `80` |
| `{{LINE_LENGTH}}` | Maximum line length for linting/formatting | `120` |
| `{{SOURCE_DIR}}` | Source directory for coverage measurement | `src` |
| `{{TEST_DIR}}` | Directory containing tests | `tests` |

## Template

```toml
[project]
name = "{{PROJECT_NAME}}"
version = "0.1.0"
description = "{{PROJECT_DESCRIPTION}}"
requires-python = ">={{PYTHON_VERSION}}"
dependencies = [
    # --- Web Framework ---
    "fastapi>=0.110.0",
    "uvicorn[standard]>=0.29.0",

    # --- Database ---
    "sqlalchemy[asyncio]>=2.0.29",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",

    # --- Validation & Config ---
    "pydantic>=2.7.0",
    "pydantic-settings>=2.2.0",

    # --- HTTP Client ---
    "httpx>=0.27.0",

    # --- Auth ---
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.9",

    # --- Caching ---
    "redis[hiredis]>=5.0.0",

    # --- Logging ---
    "structlog>=24.1.0",

    # --- Resilience ---
    "tenacity>=8.2.0",
]

[project.optional-dependencies]
dev = [
    # --- Testing ---
    "pytest>=8.1.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=5.0.0",
    "factory-boy>=3.3.0",
    "faker>=24.0.0",

    # --- Linting & Formatting ---
    "ruff>=0.4.0",

    # --- Security Scanning ---
    "bandit>=1.7.0",

    # --- Load Testing (optional) ---
    "locust>=2.28.0",
]

# --- Ruff (linting + formatting, replaces black/isort/flake8) ---
[tool.ruff]
line-length = {{LINE_LENGTH}}
target-version = "py{{PYTHON_VERSION | remove_dot}}"

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors
    "F",   # pyflakes
    "I",   # isort (import sorting)
    "N",   # pep8-naming
    "W",   # pycodestyle warnings
    "UP",  # pyupgrade (modern Python syntax)
]

[tool.ruff.lint.isort]
known-first-party = ["{{SOURCE_DIR}}"]

# --- Pytest ---
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["{{TEST_DIR}}"]
markers = [
    "slow: marks tests as slow (deselect with '-m \"not slow\"')",
    "integration: marks tests requiring external services",
]

# --- Coverage ---
[tool.coverage.run]
source = ["{{SOURCE_DIR}}"]

[tool.coverage.report]
fail_under = {{COVERAGE_THRESHOLD}}
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.",
]
```

## Usage

1. Copy this template into your project root as `pyproject.toml`.
2. Replace all `{{PLACEHOLDER}}` values. For `target-version`, remove the dot from the Python version (e.g., `3.12` becomes `py312`).
3. Adjust the `dependencies` list to match your project's actual requirements.
4. Install: `pip install -e ".[dev]"`
5. Run linting: `ruff check .`
6. Run formatting: `ruff format .`
7. Run tests: `pytest --cov`

## Notes

- Ruff replaces black (formatting), isort (import sorting), and flake8 (linting) with a single, fast tool written in Rust.
- The `asyncio_mode = "auto"` setting in pytest means you do not need to decorate every async test with `@pytest.mark.asyncio` -- it is applied automatically.
- The `exclude_lines` in coverage config prevents `TYPE_CHECKING` blocks and `__main__` guards from counting against your coverage score.
- The `known-first-party` setting in ruff's isort config ensures your project's imports are grouped correctly in import blocks.
- Add domain-specific dependencies (e.g., vector DB clients, LLM SDKs, messaging libraries) to the `dependencies` list as needed.
- For monorepos with multiple packages, consider using a workspace tool like `uv` or `hatch` instead of a single `pyproject.toml`.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |

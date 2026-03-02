# Snippet: Structured JSON Logging with structlog (Python)

## Maturity: Alpha v1.0
## Extracted: 2026-03-02
## Version: v1.0

---

## Description

Configures structured logging using the `structlog` library. Outputs JSON-formatted log lines to stdout with ISO timestamps, log level, and context variable support via `contextvars`. Includes a filtering bound logger for efficient log level gating and a convenience function for creating named loggers.

## Dependencies

- `structlog>=24.1.0`

## Code

```python
"""Structured logging configuration using structlog."""

import logging
import sys

import structlog


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structlog for JSON output with context variable support.

    Args:
        log_level: Minimum log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level.upper(), logging.INFO)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """Create a named logger instance.

    Args:
        name: Logger name, typically __name__ of the calling module.

    Returns:
        A bound structlog logger.
    """
    return structlog.get_logger(name)
```

## Usage Example

```python
# At application startup
setup_logging(log_level="INFO")

# In any module
logger = get_logger(__name__)

# Basic logging
logger.info("server_started", port=8000, workers=4)
# Output: {"event": "server_started", "port": 8000, "workers": 4, "log_level": "info", "timestamp": "2026-03-02T12:00:00Z"}

# With context variables (e.g., request-scoped data)
import structlog
structlog.contextvars.bind_contextvars(request_id="abc-123", user_id="user-42")
logger.info("request_processed", duration_ms=150)
# Output includes request_id and user_id automatically

# Exception logging
try:
    result = 1 / 0
except ZeroDivisionError:
    logger.exception("calculation_failed", input_value=0)
```

## Notes

- `merge_contextvars` pulls in any values bound with `structlog.contextvars.bind_contextvars()`, enabling request-scoped logging without passing loggers through every function call.
- `JSONRenderer` outputs one JSON object per log line, which is compatible with log aggregation tools (ELK, Datadog, CloudWatch).
- `make_filtering_bound_logger` filters at the binding level rather than after rendering, so debug-level log calls are essentially free when the minimum level is higher.
- `cache_logger_on_first_use=True` improves performance by caching the processor chain after the first log call.
- For development, replace `JSONRenderer()` with `structlog.dev.ConsoleRenderer()` for human-readable colored output.

## Changelog

| Date | Version | Change |
|------|---------|--------|
| 2026-03-02 | v1.0 | Initial extraction and decontextualization |

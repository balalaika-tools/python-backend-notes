# Core Python Concepts

Fundamental Python concepts every backend developer needs to understand.

---

## Contents

| File | Topic | Description |
|------|-------|-------------|
| [decorators.md](decorators.md) | Decorators | `@` syntax, `functools.wraps`, parameterized decorators |
| [exceptions.md](exceptions.md) | Exceptions | Propagation, `raise` variants, `raise from`, production patterns |
| [logging.md](logging.md) | Logging | `logging` module, per-module vs universal, rotation |
| [structlog_guide.md](structlog_guide.md) | Structured Logging | structlog, processors, FastAPI integration, contextvars |
| [configuration.md](configuration.md) | Configuration | pydantic-settings, `.env`, secrets, validation |

---

## Reading Order

1. **Decorators** — understand how functions wrap functions
2. **Exceptions** — understand error propagation and handling
3. **Logging** — understand stdlib logging first
4. **Structured Logging** — upgrade to structlog for production
5. **Configuration** — manage settings and secrets

---

## Prerequisites

- Basic Python (functions, classes, context managers)

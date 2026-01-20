# FastAPI Guides

Production-ready patterns and best practices for FastAPI applications.

---

## Contents

### Core Guides

- **[Dependency Injection](dependency_injection.md)** - FastAPI's built-in DI system

### External API Calls

- **[Safe and Scalable API Calls](Safe_and_Scallable_API_calls/README.md)** - Production guide for calling LLMs and external services

  | Part | Topic | Description |
  |------|-------|-------------|
  | [01](Safe_and_Scallable_API_calls/01_core_concepts.md) | Core Concepts | Mental model, the real concurrency limit |
  | [02](Safe_and_Scallable_API_calls/02_concurrency_and_timeouts.md) | Concurrency & Timeouts | Timeout layers, asyncio vs httpx |
  | [03](Safe_and_Scallable_API_calls/03_call_patterns.md) | Call Patterns | Gold standard pattern, retry logic |
  | [04](Safe_and_Scallable_API_calls/04_kubernetes.md) | Kubernetes | Multi-pod concerns, local vs global |
  | [05](Safe_and_Scallable_API_calls/05_production_architecture.md) | Production Architecture | Complete stack, execution order |
  | [06](Safe_and_Scallable_API_calls/06_advanced_patterns.md) | Advanced Patterns | Circuit breakers, priority queues |
  | [07](Safe_and_Scallable_API_calls/07_streaming_patterns.md) | Streaming Patterns | SSE, streaming timeouts |
  | [08](Safe_and_Scallable_API_calls/08_streaming_advanced.md) | Streaming Advanced | Multi-stream, aggregation |

---

## Prerequisites

Before reading the Safe API Calls guide, understand HTTPX:

**[HTTPX Guide](../httpx/README.md)** — connection pooling, timeouts, HTTP client internals

---

## Quick Reference

### Key Principles

1. **Client connection limits are mandatory** — only hard concurrency control
2. **`asyncio.timeout` ≠ request termination** — only client timeouts terminate sockets
3. **Rate limiting ≠ concurrency control** — different purposes
4. **Retries outside semaphore** — never sleep while holding resources
5. **Per-pod limits don't protect vendors** — use Redis for global limits

### Minimal Safe Pattern

```python
import asyncio
import httpx
from aiolimiter import AsyncLimiter

client = httpx.AsyncClient(
    limits=httpx.Limits(max_connections=50),
    timeout=httpx.Timeout(connect=5.0, read=30.0),
)

sem = asyncio.Semaphore(50)
rate = AsyncLimiter(60, 60)


async def call_api(payload: dict):
    async with asyncio.timeout(5):      # queue timeout
        async with rate:                 # throughput
            async with sem:              # concurrency
                async with asyncio.timeout(30):  # call timeout
                    response = await client.post(url, json=payload)
                    return response.json()
```

---

## Architecture Overview

```
API Gateway → ASGI Server → FastAPI → HTTP Client → Vendor
     ↓             ↓           ↓           ↓
  Flood       Admission    Business    Transport
 Protection    Control      Logic      Timeouts
```

Each layer has a non-overlapping responsibility.

---

## Reading Path

1. **First**: [HTTPX Guide](../httpx/README.md) — understand the HTTP client
2. **Then**: [Safe API Calls](Safe_and_Scallable_API_calls/README.md) — apply to production

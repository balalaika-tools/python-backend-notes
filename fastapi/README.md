# Production Guide: Safe and Scalable LLM & Agent Calls in FastAPI

A comprehensive, battle-tested guide for safely calling LLMs and external services from FastAPI under real production traffic.

---

## Overview

This guide covers everything from fundamental concepts to advanced distributed systems patterns for building resilient, scalable FastAPI services that make external API calls (LLMs, agents, tools, etc.).

**Goals**:
- Protect your system from overload
- Respect vendor rate limits and quotas
- Avoid retry storms and cascading failures
- Keep latency predictable
- Fail in controlled, graceful ways
- Scale safely with Kubernetes

---

## Guide Structure

### [Part 1: Fundamentals](./01_fundamentals.md)

**Core concepts and mental models**

- The four independent dimensions (Concurrency, Throughput, Latency, Failures)
- Core definitions (Rate, Latency, Concurrency, Timeouts)
- The fundamental bound: `max_concurrency ≈ rate × call_timeout`
- Global shared primitives (Semaphore, Rate limiter, HTTP client)
- Gold-standard call pattern
- Exception handling (`httpx` vs `asyncio` timeouts)
- Retry rules (what to retry, what not to retry)
- Semaphore + retry non-negotiable rule
- When you do NOT need a semaphore
- Common production mistakes

**Read this first** to understand the foundational principles.

---

### [Part 2: Production Implementation](./02_production_implementation.md)

**FastAPI integration and production patterns**

- Minimal FastAPI integration
- Complete production call pattern with logging
- Enhanced endpoints with request tracking
- What clients see (HTTP status codes and outcomes)
- Shielded cleanup (when and why)
- SDK retries (disable or account for)
- Health checks and readiness probes
- Observability (structured logging, metrics)
- Testing considerations
- Production checklist

**Read this** after Part 1 to implement production-ready endpoints.

---

### [Part 3: Kubernetes & Distributed Systems](./03_kubernetes_and_distributed_systems.md)

**Multi-pod concerns and distributed thinking**

- Why per-pod rate limiting does NOT protect vendors
- What "local fairness" actually means
- Handling bursty traffic with concrete numbers
- Correct layered handling (semaphore, queue timeout, rate limiter)
- How vendors are actually protected (global rate limiters)
- Production architecture for multi-pod systems
- How to choose values (semaphore, rate limiter, timeouts)
- Kubernetes autoscaling considerations
- Rolling deployments and rate limits
- Load balancer behavior

**Read this** when deploying to Kubernetes with multiple pods.

---

### [Part 4: Complete Production Architecture](./04_complete_production_architecture.md)

**Full stack from API Gateway to vendor calls**

- High-level architecture overview
- Layer 1: API Gateway / Ingress Controller (flood protection)
- Layer 2: Ingress Routing & Readiness (health-based routing)
- Layer 3: ASGI Server — Pod Admission Control (capacity protection)
- Layer 4: FastAPI — User-level fairness & business rules
- Layer 5: Outbound vendor protection (global rate limiting)
- Complete execution order (critical)
- Responsibility matrix (clear separation of concerns)
- Minimal, non-overengineered setup
- Deployment configuration examples

**Read this** to understand the complete system architecture.

---

### [Part 5: Advanced Topics](./05_advanced_topics.md)

**Pod-aware resilience patterns for sophisticated systems**

- Pod awareness mental model
- Circuit breakers (MUST be pod-aware, Redis-backed)
- Priority queues (pod-aware if you have backlog)
- Adaptive retry (pod-local by design)
- Load shedding (mostly pod-local)
- Pod-aware end-to-end call flow
- Complete implementation example
- When to add advanced patterns
- What lives where (local vs global state)

**Read this** for advanced resilience patterns in distributed systems.

---

## Quick Start

### 1. Basic Setup (Single Pod)

```python
import asyncio
from aiolimiter import AsyncLimiter
import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Global primitives (MUST be created at startup)
llm_sem = asyncio.Semaphore(50)
llm_rate = AsyncLimiter(60, 60)
client: httpx.AsyncClient = None


@app.on_event("startup")
async def startup():
    global client
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(connect=5.0, read=30.0, write=5.0, pool=5.0)
    )


async def call_llm(payload: dict):
    for attempt in range(3):
        try:
            async with asyncio.timeout(5):      # Queue timeout
                async with llm_rate:            # Rate limit
                    async with llm_sem:         # Semaphore
                        async with asyncio.timeout(30):  # Call timeout
                            response = await client.post(
                                "https://vendor/api",
                                json=payload,
                            )
                            response.raise_for_status()
                            return response.json()
        except Exception:
            if attempt < 2:
                await asyncio.sleep(2 ** attempt)
            else:
                raise


@app.post("/llm")
async def llm_endpoint(payload: dict):
    try:
        async with asyncio.timeout(60):  # SLA boundary
            return await call_llm(payload)
    except asyncio.TimeoutError:
        raise HTTPException(504, "Request timeout")
```

---

### 2. Multi-Pod Setup (Kubernetes)

Add Redis for global coordination:

```python
import redis.asyncio as redis

# Global vendor rate limiter (Redis-backed)
redis_client = redis.from_url("redis://redis:6379")


async def acquire_global_vendor_token() -> bool:
    """Global rate limiter shared across all pods"""
    # Implementation in Part 3
    ...


async def call_llm(payload: dict):
    async with asyncio.timeout(5):
        async with llm_rate:
            # GLOBAL vendor protection
            if not await acquire_global_vendor_token():
                raise HTTPException(429, "Vendor rate limit")
            
            async with llm_sem:
                async with asyncio.timeout(30):
                    return await client.post(...)
```

---

### 3. Production Setup (Full Architecture)

See Part 4 for complete architecture including:

- API Gateway rate limiting
- ASGI admission control
- Redis user rate limiting
- Redis vendor rate limiting
- Circuit breakers
- Health checks

---

## Key Principles

1. **Concurrency is global** (shared primitives at startup)
2. **Rate limiting waits** (unless you reject explicitly)
3. **Timeouts define ownership**, not just failures
4. **httpx timeouts ≠ asyncio timeouts** (handle separately)
5. **Retries amplify load** (be careful, use adaptive retry)
6. **Overload should fail fast** (don't retry queue timeouts)
7. **Never sleep while holding semaphores** (retry outside semaphore)
8. **Per-pod limits don't protect vendors** (use Redis for global limits)
9. **Each layer has a non-overlapping responsibility**
10. **Failure must be coordinated in distributed systems**

---

## What Makes This Guide Different

### Battle-Tested

- Based on real production experience
- Covers actual failure modes
- Explains *why*, not just *how*

### Complete

- From fundamentals to advanced patterns
- Single-pod to multi-pod Kubernetes
- Clear mental models and examples

### Correct

- Proper distinction between httpx and asyncio timeouts
- Correct retry placement (outside semaphore)
- Proper exception handling
- Clear local vs global state reasoning

### Practical

- Working code examples
- Concrete numbers and calculations
- Production checklist
- Deployment configurations

---

## Common Mistakes This Guide Prevents

❌ Semaphore inside retry decorator
❌ No queue timeout (unbounded queues)
❌ No HTTP client timeout
❌ Catching only `asyncio.TimeoutError`
❌ Rate limiter inside semaphore (wrong order)
❌ Per-request semaphores/rate limiters
❌ Per-pod rate limiters for vendor protection
❌ In-memory circuit breakers in multi-pod setups
❌ Sleeping while holding semaphores
❌ Retrying queue timeouts

---

## Dependencies

```bash
# Required
pip install fastapi uvicorn httpx aiolimiter

# For production (Redis-backed features)
pip install redis limits

# For structured logging
pip install structlog

# For async support
pip install asyncio
```

---

## Architecture at a Glance

```text
Internet
  ↓
API Gateway (flood protection, per-IP limits)
  ↓
Kubernetes Service (load balancer)
  ↓
Ingress (readiness-based routing)
  ↓
ASGI Server (admission control: --limit-concurrency 50)
  ↓
FastAPI
  ├─ Load shedding (local, early reject)
  ├─ User rate limiter (global, Redis)
  ├─ Queue timeout (local, 5s)
  ├─ Circuit breaker (global, Redis)
  ├─ Global vendor rate limiter (global, Redis)
  ├─ Local rate limiter (local, burst smoothing)
  ├─ Semaphore (local, capacity: 50)
  └─ Call timeout (local, 30s)
  ↓
HTTP Client (timeouts: connect, read, write, pool)
  ↓
Vendor API
```

---

## Reading Path

### For Beginners

1. Start with Part 1 (Fundamentals)
2. Read Part 2 (Production Implementation)
3. Implement basic setup
4. Test thoroughly

### For Production Deployment

1. Review Parts 1-2
2. **Read Part 3 carefully** (Kubernetes concerns)
3. **Read Part 4** (Complete architecture)
4. Implement layered architecture
5. Deploy with monitoring

### For Advanced Systems

1. Review Parts 1-4
2. **Read Part 5** (Advanced topics)
3. Implement circuit breakers
4. Add adaptive retry
5. Implement load shedding

---

## Testing Your Implementation

### Checklist

- [ ] Global primitives initialized at startup (not per-request)
- [ ] HTTP client has timeouts configured
- [ ] Queue timeout prevents unbounded waits
- [ ] Call timeout caps per-attempt latency
- [ ] Retry logic is outside semaphore scope
- [ ] Both `httpx.TimeoutException` and `asyncio.TimeoutError` handled
- [ ] Queue timeouts are NOT retried
- [ ] SLA boundary at endpoint level
- [ ] Health and readiness endpoints implemented
- [ ] Structured logging with request IDs
- [ ] (Multi-pod) Global vendor rate limiter via Redis
- [ ] (Multi-pod) Circuit breaker via Redis
- [ ] (Production) API Gateway limits configured
- [ ] (Production) ASGI admission control configured

---

## Contributing

This guide is based on production experience. If you find errors, have improvements, or want to share your experience, contributions are welcome.

---

## License

This guide is provided as-is for educational purposes.

---

## Credits

Compiled from real-world production experience building and scaling FastAPI services that make extensive use of LLM and external API calls.

**Last updated**: January 2026

---

## Quick Reference

| Concern                  | Mechanism                | Scope  | Part  |
| ------------------------ | ------------------------ | ------ | ----- |
| Throughput               | Rate limiter             | Local  | 1     |
| Concurrency              | Semaphore                | Local  | 1     |
| Latency                  | Timeouts                 | Local  | 1     |
| Admission control        | Queue timeout            | Local  | 1     |
| Pod capacity             | ASGI `limit-concurrency` | Local  | 4     |
| User fairness            | Redis rate limiter       | Global | 4     |
| Vendor protection        | Redis rate limiter       | Global | 3, 4  |
| Coordinated failure      | Redis circuit breaker    | Global | 5     |
| Priority handling        | Redis priority queue     | Global | 5     |
| Conditional retry        | Adaptive retry           | Local  | 5     |
| Overload protection      | Load shedding            | Local  | 5     |

---

**Start with [Part 1: Fundamentals →](./01_fundamentals.md)**

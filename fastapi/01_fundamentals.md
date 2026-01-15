# Part 1: Fundamentals — Safe LLM & Agent Calls

> **Core principle**: Every external call is a shared resource. Control it explicitly.

This guide establishes the **foundational mental model** for safely calling LLMs and external services from FastAPI under production traffic.

---

## 1. The Four Independent Dimensions

You must manage **four orthogonal concerns**:

| Dimension        | Question                                  | Mechanism                 |
| ---------------- | ----------------------------------------- | ------------------------- |
| **Concurrency**  | How many calls are in flight?             | Semaphore                 |
| **Throughput**   | How many calls per unit of time?          | Rate limiter              |
| **Latency**      | How long are we willing to wait?          | Timeouts                  |
| **Failures**     | What happens when things go wrong?        | Retry logic + exceptions  |

Each dimension requires its **own control mechanism**. They cannot be mixed or substituted.

---

## 2. Core Definitions (Precise)

### Throughput (Rate)

How many requests are **allowed to start** per unit of time.

```
60 requests / minute
```

This applies to:
- first attempts
- retries

**Control mechanism**: Rate limiter (e.g., `AsyncLimiter`)

---

### Vendor Response Latency

How long the vendor **actually takes** to respond.

Important facts:
- This is **variable** (has a distribution: p50, p95, p99)
- You do **not control it**
- You can only measure it

---

### Call Timeout

The **maximum latency you are willing to tolerate** for a single attempt.

This is a **client-side budget**, not a measurement.

```python
async with asyncio.timeout(30):
    response = await vendor_call()
```

> Call timeout is an *upper bound you choose*, not the vendor's average latency.

**Purpose**:
- Cap worst-case latency
- Prevent zombie calls
- Make retries safe
- Indirectly bound concurrency

---

### Concurrency (In-Flight Requests)

How many requests have:
- started
- and not yet finished (success, failure, or timeout)

**The concurrency that matters**:

> **Concurrency at the downstream bottleneck** (the vendor, database, etc.)

**Control mechanism**: Semaphore

---

## 3. The Fundamental Bound

With a rate limiter and a call timeout:

```
max_concurrency ≈ rate × call_timeout
```

**Example**:

```
rate = 1 req/sec
call_timeout = 30 sec

max_concurrency ≈ 30 concurrent calls
```

This bound holds **even with retries**, provided:
- Retries pass through the same rate limiter
- Each attempt is capped by the same call timeout

**Critical insight**:

> Retries do **not** increase maximum concurrency.
> They only consume capacity *within* the same `rate × call_timeout` envelope.

---

## 4. How to Choose `call_timeout` in Practice

### What It Represents

`call_timeout` is **NOT**:
- Average vendor latency
- Expected latency
- "How long it usually takes"

It **IS**:

> The maximum vendor latency you are willing to wait before giving up.

---

### Practical Rule

Choose `call_timeout` based on:

1. Acceptable user-facing latency
2. SLA or SLO targets  
3. Worst-case vendor behavior you'll tolerate

Typical approaches:

| Approach                   | When to use                              |
| -------------------------- | ---------------------------------------- |
| Slightly above **p95**     | Balanced reliability                     |
| Around **p99**             | High reliability requirements            |
| Strict SLA budget          | Hard latency guarantees (e.g., "max 30s") |

**Example**:

```
Vendor p95 latency ≈ 18s
Vendor p99 latency ≈ 25s

Chosen call_timeout = 30s
```

This means:
- You accept that some calls will timeout (above p99)
- You cap how much latency contributes to concurrency
- Calls exceeding 30s are failed, not queued

---

## 5. Global, Shared Primitives

These must be created **once** at app startup, **not per-request**.

```python
import asyncio
from aiolimiter import AsyncLimiter
import httpx
from fastapi import FastAPI

app = FastAPI()

# GLOBAL primitives
llm_sem = asyncio.Semaphore(50)      # max concurrent vendor calls
llm_rate = AsyncLimiter(60, 60)      # 60 calls per minute

client: httpx.AsyncClient | None = None


@app.on_event("startup")
async def startup():
    global client
    client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=5.0,
            read=30.0,
            write=5.0,
            pool=5.0,
        )
    )


@app.on_event("shutdown")
async def shutdown():
    await client.aclose()
```

> ⚠️ **Critical**: If these are created per request, they do NOTHING.

---

## 6. HTTP Client: Always Set Timeouts

Never rely on defaults.

```python
client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        connect=5.0,   # max time to establish connection
        read=30.0,     # max time to read response
        write=5.0,     # max time to send request
        pool=5.0,      # max time to get connection from pool
    )
)
```

This prevents:
- Hung TCP connections
- Infinite waits
- Leaked semaphore slots
- Resource exhaustion

---

## 7. Exception Handling: httpx vs asyncio Timeouts

### Important Distinction

`httpx` does **NOT** raise `asyncio.TimeoutError`.

It raises:
- `httpx.ConnectTimeout`
- `httpx.ReadTimeout`
- `httpx.WriteTimeout`
- `httpx.PoolTimeout`

All inherit from:

```python
httpx.TimeoutException
```

### Meaning

| Error type               | Meaning                               | Retry? |
| ------------------------ | ------------------------------------- | ------ |
| `httpx.TimeoutException` | Vendor / network slowness             | ✅ Yes  |
| `asyncio.TimeoutError`   | Your system's budget expired          | ⚠️ Maybe |

**Rule**:

> `httpx.TimeoutException` → vendor problem → retry
> `asyncio.TimeoutError` → your budget problem → careful

---

## 8. The Gold-Standard Call Pattern

This is the **recommended baseline** for LLM or agent calls.

```python
import asyncio
import httpx


class RetryableError(Exception):
    """Transient errors that may succeed on retry"""
    pass


class FinalFailure(Exception):
    """Permanent failure after all retries exhausted"""
    pass


def backoff(attempt: int) -> float:
    """Exponential backoff with jitter"""
    import random
    base = min(2 ** attempt, 32)
    return base + random.uniform(0, 1)


async def call_llm(payload: dict):
    """
    Gold standard LLM call with:
    - Queue timeout (admission control)
    - Rate limiting (throughput control)
    - Semaphore (concurrency control)
    - Call timeout (latency control)
    - Retry logic with proper exception handling
    """
    for attempt in range(3):
        try:
            # Queue timeout: do not wait forever to START
            async with asyncio.timeout(5):
                async with llm_rate:        # throughput control
                    async with llm_sem:     # concurrency control
                        
                        # Call timeout: do not let vendor hang
                        async with asyncio.timeout(30):
                            response = await client.post(
                                "https://vendor/api",
                                json=payload,
                            )
                            response.raise_for_status()
                            return response.json()
        
        except httpx.TimeoutException:
            # Vendor / network slowness → retry
            if attempt < 2:
                await asyncio.sleep(backoff(attempt))
                continue
            raise FinalFailure("Vendor timeout after retries")
        
        except httpx.HTTPStatusError as e:
            # 5xx → retry, 4xx → don't retry
            if 500 <= e.response.status_code < 600:
                if attempt < 2:
                    await asyncio.sleep(backoff(attempt))
                    continue
            raise
        
        except asyncio.TimeoutError:
            # Could be queue timeout OR call timeout
            # Queue timeout → system overloaded → do NOT retry blindly
            if attempt == 0:
                await asyncio.sleep(backoff(attempt))
                continue
            raise FinalFailure("Timeout after retries")
    
    raise FinalFailure("All retries exhausted")
```

---

## 9. What Each Timeout Controls

### Queue Timeout (Admission Timeout)

```python
async with asyncio.timeout(5):
    async with llm_rate:
        async with llm_sem:
            ...
```

**Meaning**: "If I can't even START the call within 5 seconds, give up."

**Covers**:
- Waiting on the rate limiter
- Waiting on the semaphore

**Purpose**:
- Avoid unbounded queues
- Protect FastAPI latency
- Fail fast under overload

---

### Call Timeout

```python
async with asyncio.timeout(30):
    response = await client.post(...)
```

**Meaning**: "Once the vendor call starts, I'll wait at most 30 seconds."

**Covers**:
- TCP connection establishment
- Request transmission
- Vendor processing time
- Response reading

**Purpose**:
- Avoid zombie calls
- Make retries safe
- Bound worst-case latency

---

## 10. Retry Rules (Critical)

### ✅ Retry These

- Transient network errors
- 5xx responses (server errors)
- Vendor slowness (`httpx.TimeoutException`)
- Call timeout (but **not** queue timeout)

### ❌ Do NOT Retry These

- Queue timeouts (system is overloaded)
- 4xx responses (client errors)
- Authentication errors
- User input validation errors

**Rule of thumb**:

> If the system is already overloaded, retries make it worse.

---

## 11. Semaphore + Retry: Non-Negotiable Rule

> **Retries must happen OUTSIDE the semaphore scope.**

### ✅ Correct

```python
for attempt in range(3):
    async with llm_sem:
        result = await call_vendor()
    
    if needs_retry:
        await asyncio.sleep(backoff(attempt))
```

The semaphore is released **before** sleeping.

### ❌ Incorrect

```python
@retry_decorator
async with llm_sem:
    await call_vendor()
```

or

```python
async with llm_sem:
    for attempt in range(3):
        result = await call_vendor()
        if needs_retry:
            await asyncio.sleep(backoff(attempt))
```

**Why this matters**:

If you sleep while holding a semaphore:
- Throughput collapses
- Other requests are blocked unnecessarily
- Deadlocks appear under load

---

## 12. When You Do NOT Need a Semaphore

A semaphore is **optional** if:

1. You enforce a rate limiter
2. You enforce a call timeout
3. You have calculated and accepted:
   ```
   max_concurrency ≈ rate × call_timeout
   ```
4. Your system can handle that worst case
5. Retries are bounded and reasonable

In this case:

> A semaphore adds no safety — only an extra bottleneck.

---

## 13. What a Semaphore Is Actually For

A semaphore exists to do **only this**:

```
max_concurrency = min(rate × call_timeout, semaphore_size)
```

Use it **only if** you want:
- A smaller concurrency cap than the natural bound
- Stricter capacity control
- Cost protection
- Tail-latency protection

**Never use a semaphore without a call timeout.**

---

## 14. Rate Limiter Behavior (AsyncLimiter)

`AsyncLimiter`:
- **Waits** (does not reject)
- Does NOT return 429
- Queues callers fairly

This means:
- FastAPI requests may wait
- Workers are not blocked (async)
- Latency increases instead of failing

**If you want hard rejection**, you must implement it yourself (covered in Part 4).

---

## 15. Common Production Mistakes

❌ Semaphore inside retry decorator
❌ No queue timeout
❌ No HTTP client timeout
❌ Catching only `asyncio.TimeoutError`
❌ Rate limiter inside semaphore (order matters!)
❌ Per-request semaphores/rate limiters
❌ Unlimited FastAPI request wait time
❌ Sleeping while holding semaphore
❌ Retrying queue timeouts

---

## 16. Final Mental Model

| Mechanism       | Controls              | Purpose                          |
| --------------- | --------------------- | -------------------------------- |
| Rate limiter    | Starts per time       | Throughput control               |
| Call timeout    | Max latency           | Latency control                  |
| Semaphore       | Concurrent calls      | Concurrency control (optional)   |
| Queue timeout   | Max wait to start     | Admission control                |
| Retries         | Transient failures    | Reliability                      |

**The Formula**:

```
max_concurrency ≈ rate × call_timeout
```

With semaphore:

```
max_concurrency = min(rate × call_timeout, semaphore_size)
```

---

## Final Rules

1. **Concurrency is global** (shared primitives)
2. **Rate limiting waits** (unless you reject explicitly)
3. **Timeouts define ownership**, not failures
4. **httpx timeouts ≠ asyncio timeouts**
5. **Retries amplify load** (be careful)
6. **Overload should fail fast** (don't retry queue timeouts)
7. **Never sleep while holding semaphores**

---

**Next**: Part 2 covers FastAPI integration, shielded cleanup, and complete production patterns.

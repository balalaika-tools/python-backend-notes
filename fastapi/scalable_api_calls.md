# Production Guide: Safe and Scalable LLM & Agent Calls in FastAPI

This guide describes **battle-tested patterns** for safely calling LLMs (or agentic pipelines) from a FastAPI endpoint under real traffic.

The goals are:

* protect your system
* respect vendor limits
* avoid retry storms
* keep latency predictable
* fail in controlled ways

---

## 1. The Core Mental Model

> **Every external call is a shared resource.
> Control it explicitly.**

You are managing **four independent dimensions**:

1. **Concurrency** – how many calls are in flight
2. **Throughput** – how many calls per unit of time
3. **Latency** – how long you're willing to wait
4. **Failures** – what happens when things go wrong

Each dimension needs its **own mechanism**.

---

## 2. The Canonical Stack (in order)

```
🌍 Client
  ↓
🚪 API Gateway / Middleware   ← per-user limits (REJECT)
  ↓
🧠 FastAPI request
  ↓
⏳ Queue timeout
  ↓
🚦 Global Rate limiter        ← respects vendor limits (WAIT, not reject)
  ↓
🧵 Semaphore                  ← caps concurrent in-flight calls
  ↓
⏳ Client Call timeout        ← wait time per llm call
  ↓
🤖 HTTP client (with timeouts)
  ↓
🔁 Retry + backoff
```

**Order matters.**

---

## 3. Global, Shared Primitives (NOT per-request)

These must be created **once**, at app startup.

```python
import asyncio
from aiolimiter import AsyncLimiter
import httpx
from fastapi import FastAPI
```

```python
app = FastAPI()

llm_sem = asyncio.Semaphore(3)   # max concurrent vendor calls
llm_rate = AsyncLimiter(60, 60)  # 60 calls per minute

client: httpx.AsyncClient | None = None
```

```python
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

> ⚠️ If these are created per request, they do NOTHING.

---

## 4. HTTP Client: Always Set Timeouts

Never rely on defaults.

```python
import httpx
```

```python
client = httpx.AsyncClient(
    timeout=httpx.Timeout(
        connect=5.0,
        read=30.0,
        write=5.0,
        pool=5.0,
    )
)
```

This prevents:

* hung TCP connections
* infinite waits
* leaked semaphore slots

---

## 5. The Gold-Standard Call Pattern (with Correct Exceptions)

This is the **recommended baseline** for LLM or agent calls.

```python
import asyncio
import httpx
```

```python
class RetryableError(Exception):
    pass


class FinalFailure(Exception):
    pass
```

```python
async def call_llm(payload: dict):
    for attempt in range(3):
        try:
            # Queue timeout: do not wait forever to START
            async with asyncio.timeout(5):
                async with llm_rate:        # throughput control
                    async with llm_sem:     # concurrency control

                        # Call timeout: do not let vendor hang
                        async with asyncio.timeout(30):
                            return await client.post(
                                "https://vendor/api",
                                json=payload,
                            )

        except httpx.TimeoutException:
            # Vendor / network slowness (connect/read/write/pool)
            await asyncio.sleep(backoff(attempt))

        except httpx.HTTPStatusError as e:
            if 500 <= e.response.status_code < 600:
                await asyncio.sleep(backoff(attempt))
            else:
                raise

        except asyncio.TimeoutError:
            # Could be queue timeout or call timeout
            # Queue timeout → system overloaded → do NOT retry
            if attempt == 0:
                await asyncio.sleep(backoff(attempt))
            else:
                raise

    raise FinalFailure()
```

---

## 6. What Each Timeout Actually Means

### Queue timeout (`asyncio.timeout(5)`)

> "If I can't even START the call within 5 seconds, give up."

Covers:

* waiting on the rate limiter
* waiting on the semaphore

Use this to:

* avoid unbounded queues
* protect FastAPI latency
* fail fast under overload

---

### Call timeout (`asyncio.timeout(30)`)

> "Once the vendor call starts, I'll wait at most 30 seconds."

Covers:

* connect
* request
* vendor processing
* response read

Use this to:

* avoid zombie calls
* make retries safe

---

### httpx Timeouts (Important)

`httpx` does **NOT** raise `asyncio.TimeoutError`.

It raises:

* `httpx.ConnectTimeout`
* `httpx.ReadTimeout`
* `httpx.WriteTimeout`
* `httpx.PoolTimeout`

All inherit from:

```python
httpx.TimeoutException
```

**Meaning:**

| Error type               | Meaning                      |
| ------------------------ | ---------------------------- |
| `httpx.TimeoutException` | vendor / network slowness    |
| `asyncio.TimeoutError`   | your system's budget expired |

Treat them differently.

---

## 7. Retry Rules (Critical)

### ✅ Retry:

* transient network errors
* 5xx responses
* vendor slowness (`httpx.TimeoutException`)
* call timeout (`asyncio.timeout` around vendor call)

### ❌ Do NOT retry:

* queue timeouts (system is overloaded)
* invalid requests
* auth errors
* user input errors

**Rule of thumb:**

> If the system is already overloaded, retries make it worse.

---

## 8. Semaphore + Retry: Non-Negotiable Rule

> **Retries must happen OUTSIDE the semaphore scope.**

Correct:

```python
for attempt in ...:
    async with llm_sem:
        await call_vendor()
    await asyncio.sleep(backoff(attempt))
```

Incorrect:

```python
@retry
async with llm_sem:
    await call_vendor()
```

If you sleep while holding a semaphore:

* throughput collapses
* deadlocks appear under load

---

## 9. Rate Limiter Behavior (Important)

`AsyncLimiter`:

* **waits**
* does NOT return 429
* queues callers fairly

This means:

* FastAPI requests may wait
* workers are not blocked (async)
* latency increases instead of failing

If you want **hard rejection**, you must implement it yourself.

---

## 10. What the Client Sees

| Situation      | Client Outcome            |
| -------------- | ------------------------- |
| Queue overload | Fast fail (timeout / 429) |
| Vendor slow    | Retry → maybe succeed     |
| Vendor down    | Controlled failure        |
| Rate limit hit | Request waits             |
| System healthy | Normal latency            |

**You decide where to cut.**

---

## 11. SDK Retries: Disable or Ignore

Many vendor SDKs have retries.

Treat them as:

* best-effort safety nets
* NOT control mechanisms

**Never stack retries blindly:**

```
your retry × SDK retry × vendor retry = retry storm
```

One retry layer. Yours.

---

## 12. Common Production Mistakes

❌ Semaphore inside retry decorator
❌ No queue timeout
❌ No HTTP client timeout
❌ Catching only `asyncio.TimeoutError`
❌ Rate limiter inside semaphore
❌ Per-request semaphores
❌ Unlimited FastAPI request wait time

---

## 13. Minimal FastAPI Integration

```python
from fastapi import HTTPException
```

```python
@app.post("/llm")
async def llm_endpoint(payload: dict):
    try:
        async with asyncio.timeout(60):  # SLA boundary
            return await call_llm(payload)
    except asyncio.TimeoutError:
        raise HTTPException(504, "Request timeout")
```

This ensures:

* predictable upper-bound latency
* no runaway requests

---

## 14. Final Rules to Remember

1. **Concurrency is global**
2. **Rate limiting waits unless you reject**
3. **Timeouts define ownership, not failures**
4. **httpx timeouts ≠ asyncio timeouts**
5. **Retries amplify load**
6. **Overload should fail fast**
7. **Magic abstractions hide failure modes**

---

## 15. Shielded Cleanup — What It Is and WHEN You Need It

### The Problem

When any of these happen:

* SLA boundary hit
* client disconnect
* timeout

👉 the task is **cancelled** (`CancelledError`).

If inside that task you have:

* logging
* metrics
* releasing external locks
* persisting partial state
* notifying another service

⚠️ **these will NOT run unless you protect them**.

---

### What "Shielded" Means

> 🔑 *"This part must run EVEN IF the request is cancelled."*

You do this with `asyncio.shield()`.

---

### Basic Pattern

```python
async def call_llm():
    try:
        async with asyncio.timeout(60):
            return await actual_llm_work()
    except asyncio.TimeoutError:
        await asyncio.shield(cleanup())
        raise
```

What happens:

* the main task is cancelled
* `cleanup()`:

  * **is not cancelled**
  * runs to completion
* the exception is re-raised

---

### What MUST Go Into Shielded Cleanup

✅ **YES**

* metrics (`record_timeout()`)
* tracing
* releasing *external* resources
* marking a job as failed
* notifying a queue / orchestrator

❌ **NO**

* retries
* vendor calls
* heavy work
* anything slow

> ❗ Shielded cleanup must be **fast and bounded**.

---

### Best Production Pattern

```python
async def endpoint():
    try:
        async with asyncio.timeout(60):
            return await call_llm()
    except asyncio.TimeoutError:
        await asyncio.shield(record_sla_violation())
        raise HTTPException(504, "Request timeout")
```

---

## When to Add More

Add **only if needed**:

* circuit breakers
* per-user rate limits
* priority queues
* adaptive retry
* load shedding

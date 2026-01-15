# Part 3: Kubernetes & Distributed Systems — Multi-Pod Concerns

> **Critical insight**: Per-pod rate limiters are process-local. Vendor limits are global.

This guide explains **why per-pod rate limiting fails to protect vendor APIs**, what **local fairness** means, and how to **correctly handle bursty traffic** in a Kubernetes environment.

---

## 1. The Fundamental Problem: Per-Pod Limits Don't Protect Vendors

### Scenario

Assume:
- Vendor rate limit: **500 requests / minute**
- Kubernetes pods: **10**
- Each pod uses:
  ```python
  AsyncLimiter(500, 60)
  ```

### What Happens?

Each pod independently believes it may send **500 req/min**.

**Actual cluster behavior**:

```
Total cluster rate = 10 × 500 = 5,000 req/min ❌
```

The vendor limit is **exceeded by 10x**.

---

### Why This Happens

There is **no shared state** between pods:
- Each pod has its own memory
- Each `AsyncLimiter` is independent
- Pods cannot "see" each other's activity

**Key fact**:

> **Per-pod rate limiters are process-local.**
> **Vendor limits are global.**

Without coordination:
- Pods cannot know what other pods are doing
- Vendor limits will be violated under:
  - Scale-up
  - Autoscaling
  - Rolling deployments
  - Traffic bursts

**Conclusion**:

> **Per-pod rate limiting does NOT protect vendor APIs.**

---

## 2. What "Local Fairness" Actually Means

Local fairness is **not about the vendor**.

It means:

> **Protecting a single pod from overload, even if the cluster is healthy.**

---

### What Local Fairness Protects

Local fairness protects **pod-level resources**:
- CPU
- Memory
- Socket pools
- Event loop responsiveness
- Tail latency
- Pod stability

---

### What Local Fairness Ensures

- No single pod collapses under burst traffic
- Load is smoothed locally
- Failures are fast and controlled
- The event loop remains responsive
- Health checks continue to pass

**Mental model**:

> Local rate limiting is about **pod survivability**, not vendor protection.

---

## 3. Concrete Scenario: Bursty Traffic

### Setup

Assume:
- Vendor rate limit: **500 req/min** (global)
- Each pod can safely handle: **50 concurrent outbound calls**
- Suddenly: **500 requests arrive at ONE pod**

---

### What You Must Prevent

**Without local limits**:

```
500 requests arrive
  ↓
500 async tasks start
  ↓
500 HTTP calls open
  ↓
Sockets exhausted
Memory pressure
Event loop starvation
Latency explodes
Retries amplify load
Health checks fail
Pod removed from service
  ↓
Cascading failure to other pods
```

**Even if the vendor limit is respected globally, the pod dies first.**

---

## 4. Correct Layered Handling (Concrete Numbers)

### Layer 1 — Local Concurrency Cap (Semaphore)

```python
llm_sem = asyncio.Semaphore(50)
```

**Meaning**:

> "This pod will never have more than 50 in-flight vendor calls."

**Effect**:
- First 50 requests run
- Remaining 450 requests wait or fail fast
- The pod survives

This is a **capacity guard**, not a rate limit.

---

### Layer 2 — Local Queue Timeout (Admission Control)

```python
async with asyncio.timeout(5):
    async with llm_sem:
        ...
```

**Meaning**:

> "If a request cannot start within 5 seconds, reject it."

**Effect**:
- No unbounded queues
- No silent latency growth
- Overload fails fast
- Client gets fast 504/429 response

---

### Layer 3 — Local Rate Limiter (Fairness, NOT Vendor Protection)

**Do NOT use the vendor rate.**

Instead, base it on **pod capacity**.

#### Calculate Pod Capacity

Assumptions:
- Semaphore = 50
- Average vendor latency ≈ 30s

Sustainable per-pod throughput:

```
throughput ≈ semaphore / avg_latency
throughput ≈ 50 / 30s
throughput ≈ 1.67 req/sec
throughput ≈ 100 req/min
```

#### Set Local Rate Limiter

```python
llm_rate = AsyncLimiter(80, 60)
```

**Why 80, not 100?**

- Safety margin
- Handles latency variance
- Prevents self-overload

**Purpose**:
- Smooths bursts
- Prevents pod from self-overloading
- Keeps latency predictable
- **NOT** for vendor protection

---

### What Happens to the 500 Incoming Requests

With:
- Semaphore = 50
- Local rate = 80/min
- Queue timeout = 5s

**Result per pod**:

| Requests | Outcome                               |
| -------- | ------------------------------------- |
| ~50      | Start immediately (semaphore slots)   |
| ~30      | Start gradually (rate-limited queue)  |
| ~420     | Fail fast (queue timeout → 504/429)   |

**The pod remains stable.**

The load balancer will distribute rejected requests to other pods (if available).

---

## 5. How the Vendor Is Actually Protected

**Not by per-pod logic.**

Vendor protection requires a **global rate limiter**, such as:

| Solution                    | Pros                          | Cons                     |
| --------------------------- | ----------------------------- | ------------------------ |
| Redis-based token bucket    | Precise, cluster-wide         | Requires Redis           |
| API Gateway rate limiting   | Simple, external              | Less flexible            |
| Istio/Envoy rate limiting   | Service mesh integration      | Complex setup            |
| Distributed rate limiter    | Custom, highly accurate       | Engineering effort       |

Only a **shared, cluster-wide limiter** can enforce:

```
Σ(vendor calls from all pods) ≤ vendor limit
```

Without this:

> **Vendor limits WILL be violated under scale.**

---

## 6. The Correct Production Architecture

```
Incoming traffic
  ↓
Load Balancer (Kubernetes Service)
  ↓
[Per-Pod Layered Defense]
  ↓
  Local queue timeout (fail fast)
  ↓
  Local semaphore (machine capacity)
  ↓
  Local rate limiter (fairness / smoothing)
  ↓
  GLOBAL vendor rate limiter (Redis/Gateway)
  ↓
Vendor API
```

**Each layer has a different responsibility**:

| Layer                  | Scope  | Purpose                    |
| ---------------------- | ------ | -------------------------- |
| Queue timeout          | Local  | Admission control          |
| Semaphore              | Local  | Pod capacity protection    |
| Local rate limiter     | Local  | Burst smoothing            |
| Global rate limiter    | Global | Vendor contract enforcement|

---

## 7. How to Choose Values (Rules of Thumb)

### Semaphore Size

```
= maximum concurrent calls the pod can safely handle
```

**Based on**:
- CPU cores
- Memory available
- Socket/connection limits
- Benchmark results
- Vendor latency profile

**Typical values**:
- Small pods: 20-50
- Medium pods: 50-100
- Large pods: 100-200

**Never**:
- Unlimited
- Larger than your socket pool
- Based on vendor limits (that's global)

---

### Local Rate Limiter

```
≈ (semaphore / avg_vendor_latency) × safety_margin

safety_margin ≈ 0.7 - 0.9
```

**Example**:

```
semaphore = 50
avg_latency = 30s
safety = 0.8

local_rate ≈ (50 / 30) × 0.8
local_rate ≈ 1.33 req/sec
local_rate ≈ 80 req/min
```

**Purpose**: Smooth local load, not enforce vendor limits.

---

### Global Rate Limiter

```
= vendor contract (exactly)
```

**Never**:
- Per pod
- Divided by number of pods
- Based on local capacity

**Examples**:
- OpenAI: 500 req/min
- Anthropic: 100 req/min
- Custom API: whatever they give you

---

### Queue Timeout

```
= how long you're willing to wait before starting work
```

**Typical values**:
- Strict latency: 2-5s
- Moderate: 5-10s
- Loose: 10-30s

**Rule**: Should be much smaller than SLA boundary.

---

## 8. Kubernetes Autoscaling Considerations

### The Problem

With Horizontal Pod Autoscaler (HPA):
- Pods scale up → total cluster capacity increases
- But per-pod rate limiters remain the same
- **Vendor limits are still global**

**Example**:

```
Initial: 10 pods × 80 req/min = 800 req/min (local)
Scaled: 20 pods × 80 req/min = 1,600 req/min (local)

But vendor limit = 500 req/min (global) ❌
```

---

### The Solution

**Global rate limiter must be**:
- Shared across all pods
- Independent of pod count
- Enforced at the cluster level

**Never**:
- Divide vendor limit by pod count
- Reconfigure on scale events
- Rely on "coordination" between pods

---

## 9. Rolling Deployments and Rate Limits

### The Problem

During rolling deployments:
- Old pods still running
- New pods starting
- **Total pod count temporarily increases**

**Example**:

```
Normal: 10 pods
During deploy: 10 old + 5 new = 15 pods temporarily
```

If each pod enforces local limits based on "expected cluster size":
- You'll have 50% more pods than planned
- Vendor limits will be exceeded

---

### The Solution

Use a **global rate limiter** that is:
- Independent of deployment state
- Shared across old and new pods
- Enforced regardless of pod count

---

## 10. Load Balancer Behavior

### Non-Deterministic Distribution

Load balancers (Kubernetes Service) distribute traffic:
- Round-robin
- Least connections
- Random
- **But NOT based on internal pod state**

**This means**:
- One pod might be overloaded
- Another pod might be idle
- LB doesn't know about semaphore pressure
- LB doesn't know about rate limiter state

---

### Why This Matters

**Scenario**:

```
Pod A: semaphore exhausted (50/50)
Pod B: idle (0/50)

Next request → LB sends to Pod A
  ↓
Queue timeout
  ↓
503 response
```

But Pod B was available.

---

### Solutions

1. **Readiness probes** (reactive)
   - Pod A fails health check
   - LB stops routing to it
   - But there's a delay

2. **Fast queue timeouts** (proactive)
   - Pod A rejects quickly (504/429)
   - Client retries
   - LB routes retry to Pod B

3. **Connection-based routing**
   - Use least-connections algorithm
   - Better distribution under uneven load

---

## 11. Complete Example: Multi-Pod System

```python
import asyncio
from aiolimiter import AsyncLimiter
import httpx
from fastapi import FastAPI, HTTPException
import redis.asyncio as redis

app = FastAPI()

# === Local primitives (per-pod) ===
llm_sem = asyncio.Semaphore(50)           # Pod capacity
llm_rate_local = AsyncLimiter(80, 60)     # Local smoothing

# === Global primitives (shared) ===
redis_client: redis.Redis = None
VENDOR_LIMIT_KEY = "vendor:openai:limit"
VENDOR_LIMIT = 500  # req/min


@app.on_event("startup")
async def startup():
    global redis_client
    redis_client = redis.from_url("redis://redis:6379")


async def acquire_global_vendor_token() -> bool:
    """
    Global rate limiter using Redis.
    Returns True if token acquired, False otherwise.
    """
    # Simple sliding window implementation
    now = asyncio.get_event_loop().time()
    window_start = now - 60  # 1 minute window
    
    pipe = redis_client.pipeline()
    
    # Remove old entries
    pipe.zremrangebyscore(VENDOR_LIMIT_KEY, 0, window_start)
    
    # Count current entries
    pipe.zcard(VENDOR_LIMIT_KEY)
    
    # Add new entry if under limit
    pipe.zadd(VENDOR_LIMIT_KEY, {str(now): now})
    
    # Set expiry
    pipe.expire(VENDOR_LIMIT_KEY, 61)
    
    results = await pipe.execute()
    
    count = results[1]
    
    if count >= VENDOR_LIMIT:
        # Remove the entry we just added
        await redis_client.zrem(VENDOR_LIMIT_KEY, str(now))
        return False
    
    return True


async def call_llm(payload: dict):
    """
    Multi-pod safe LLM call with:
    - Local queue timeout
    - Local semaphore
    - Local rate limiter
    - Global vendor rate limiter
    """
    
    for attempt in range(3):
        try:
            # Local admission control
            async with asyncio.timeout(5):
                # Local rate smoothing
                async with llm_rate_local:
                    # Global vendor protection
                    if not await acquire_global_vendor_token():
                        raise HTTPException(429, "Vendor rate limit")
                    
                    # Local capacity protection
                    async with llm_sem:
                        # Call timeout
                        async with asyncio.timeout(30):
                            response = await client.post(
                                "https://vendor/api",
                                json=payload,
                            )
                            response.raise_for_status()
                            return response.json()
        
        except httpx.TimeoutException:
            if attempt < 2:
                await asyncio.sleep(backoff(attempt))
                continue
            raise FinalFailure("Vendor timeout")
        
        except asyncio.TimeoutError:
            # Queue or call timeout
            if attempt == 0:
                await asyncio.sleep(backoff(attempt))
                continue
            raise FinalFailure("System timeout")
    
    raise FinalFailure("All retries exhausted")
```

---

## 12. Final Takeaways

### Per-Pod vs Global

| Concern              | Scope  | Mechanism                    |
| -------------------- | ------ | ---------------------------- |
| Pod capacity         | Local  | Semaphore                    |
| Pod admission        | Local  | Queue timeout                |
| Burst smoothing      | Local  | Local rate limiter           |
| Vendor protection    | Global | Redis/Gateway rate limiter   |

---

### Key Principles

1. ❌ Per-pod rate limiting does **NOT** protect vendor APIs
2. ✅ Per-pod rate limiting provides **local fairness**
3. ✅ Semaphores enforce **machine capacity**
4. ✅ Global rate limiting enforces **vendor contracts**
5. ❗ Without layering, burst traffic causes cascading failures
6. ❗ Kubernetes autoscaling and deployments require global coordination

---

### One-Line Design Principle

> **We enforce vendor limits globally and protect each pod locally from overload.**

This is the correct, production-grade mental model for distributed systems.

---

**Next**: Part 4 covers the complete production architecture, including API Gateway, ASGI admission control, and the full execution order with responsibilities clearly separated.

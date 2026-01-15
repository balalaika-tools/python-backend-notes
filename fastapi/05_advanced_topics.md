# Part 5: Advanced Topics — Pod-Aware Resilience Patterns

> **Key principle**: Some mechanisms must be **shared across pods**, others must remain **local to each pod**.

This guide covers **pod-aware control mechanisms** required when your FastAPI service runs with **multiple pods behind a load balancer**.

The goal is not sophistication — it is **globally consistent, controlled failure**.

---

## 0. Pod Awareness: The Mental Model

In a multi-pod environment:

- Each pod has **its own memory**
- The load balancer distributes traffic **non-deterministically**
- Local state ≠ global truth
- **Coordination requires shared state** (Redis, etc.)

---

### Rule of Thumb

> **Protecting a downstream dependency → shared state**
> **Protecting a pod's own health → local state**

**Examples**:

| Concern                | Scope  | State      | Why                                    |
| ---------------------- | ------ | ---------- | -------------------------------------- |
| Circuit breaker        | Global | Redis      | All pods must agree when to stop       |
| Vendor rate limit      | Global | Redis      | Vendor sees all pods                   |
| Semaphore              | Local  | In-memory  | Pod capacity is per-pod                |
| Load shedding          | Local  | In-memory  | Pod health is local                    |
| Adaptive retry budget  | Local  | In-memory  | Based on local conditions              |

We will explicitly call out scope in every section.

---

## 1. Circuit Breakers (🔴 MUST Be Pod-Aware)

### What Problem They Solve

When a downstream dependency (LLM vendor, agent service, tool API) is **systematically failing**, retries across *multiple pods*:

- Multiply traffic against a broken system
- Burn global rate limits
- Increase tail latency everywhere
- Create cascading failures
- Prevent recovery

A **pod-aware circuit breaker** ensures **all pods agree** when to stop calling.

---

### Mental Model

> "If the vendor is failing for everyone, **all pods stop calling**."

---

### Circuit Breaker States (Global)

| State         | Behavior                                  |
| ------------- | ----------------------------------------- |
| **Closed**    | Normal operation                          |
| **Open**      | All pods fail fast (no vendor calls)      |
| **Half-open** | Limited probe calls globally (test recovery)|

**State transitions**:

```
Closed → Open: After N failures in window
Open → Half-open: After timeout
Half-open → Closed: After M successes
Half-open → Open: After any failure
```

---

### Where It Belongs in the Call Stack

```
Queue timeout
  ↓
Circuit breaker (GLOBAL fail fast)
  ↓
Global vendor rate limiter
  ↓
Local rate limiter (optional)
  ↓
Semaphore
  ↓
Vendor call
```

**Critical**: Circuit breaker must come **before** rate limiting and concurrency controls.

**Why**: If breaker is open, don't waste rate limit tokens or semaphore slots.

---

### Why In-Memory Breakers Are WRONG in Multi-Pod Setups

Without shared state:

```
Pod A → breaker OPEN
Pod B → breaker CLOSED
Pod C → breaker CLOSED
```

**Result**:
- Vendor still receives traffic from Pods B and C
- Circuit breaker loses its purpose
- Retries continue to amplify the outage
- No coordinated recovery

👉 **Circuit breakers MUST be shared (Redis, etc.)**

---

### Pod-Aware Redis-Backed Circuit Breaker

```python
import redis.asyncio as redis
import time
from typing import Optional


class CircuitBreakerOpen(Exception):
    """Circuit breaker is open, calls are not allowed"""
    pass


class PodAwareCircuitBreaker:
    """
    Redis-backed circuit breaker shared across all pods.
    
    State stored in Redis:
    - {key}:state → "closed" | "open" | "half_open"
    - {key}:failures → failure count in current window
    - {key}:opened_at → timestamp when opened
    - {key}:successes → success count in half-open state
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        key: str,
        failure_threshold: int = 5,
        success_threshold: int = 2,
        timeout_seconds: int = 60,
    ):
        self.redis = redis_client
        self.key_prefix = f"breaker:{key}"
        self.failure_threshold = failure_threshold
        self.success_threshold = success_threshold
        self.timeout = timeout_seconds
    
    async def allow(self) -> None:
        """
        Check if a call is allowed.
        
        Raises:
            CircuitBreakerOpen if breaker is open.
        """
        state = await self._get_state()
        
        if state == "open":
            # Check if timeout expired
            opened_at = await self.redis.get(f"{self.key_prefix}:opened_at")
            if opened_at:
                elapsed = time.time() - float(opened_at)
                if elapsed > self.timeout:
                    # Move to half-open
                    await self._set_state("half_open")
                    await self.redis.set(f"{self.key_prefix}:successes", 0)
                else:
                    raise CircuitBreakerOpen(f"Circuit breaker open for {self.key_prefix}")
            else:
                raise CircuitBreakerOpen(f"Circuit breaker open for {self.key_prefix}")
        
        elif state == "half_open":
            # Allow limited probing
            pass
    
    async def record_success(self) -> None:
        """Record a successful call"""
        state = await self._get_state()
        
        if state == "half_open":
            # Increment success counter
            successes = await self.redis.incr(f"{self.key_prefix}:successes")
            
            if successes >= self.success_threshold:
                # Recovery successful, close breaker
                await self._set_state("closed")
                await self.redis.set(f"{self.key_prefix}:failures", 0)
        
        elif state == "closed":
            # Reset failure counter on success
            await self.redis.set(f"{self.key_prefix}:failures", 0)
    
    async def record_failure(self) -> None:
        """Record a failed call"""
        state = await self._get_state()
        
        if state == "half_open":
            # Any failure in half-open → back to open
            await self._set_state("open")
            await self.redis.set(f"{self.key_prefix}:opened_at", time.time())
        
        elif state == "closed":
            # Increment failure counter
            failures = await self.redis.incr(f"{self.key_prefix}:failures")
            
            # Set expiry on counter (sliding window)
            await self.redis.expire(f"{self.key_prefix}:failures", 60)
            
            if failures >= self.failure_threshold:
                # Open the breaker
                await self._set_state("open")
                await self.redis.set(f"{self.key_prefix}:opened_at", time.time())
    
    async def _get_state(self) -> str:
        """Get current state"""
        state = await self.redis.get(f"{self.key_prefix}:state")
        return state.decode() if state else "closed"
    
    async def _set_state(self, state: str) -> None:
        """Set state"""
        await self.redis.set(f"{self.key_prefix}:state", state)


# Setup
breaker = PodAwareCircuitBreaker(
    redis_client=redis_client,
    key="vendor:openai",
    failure_threshold=5,
    success_threshold=2,
    timeout_seconds=60,
)


# Usage
async def call_llm_with_breaker(payload: dict):
    """
    LLM call with circuit breaker protection
    """
    # Check breaker FIRST (before any resource allocation)
    await breaker.allow()
    
    try:
        # Actual call logic
        async with asyncio.timeout(5):
            async with llm_rate:
                await vendor_limiter.wait_and_acquire()
                async with llm_sem:
                    async with asyncio.timeout(30):
                        response = await client.post(
                            "https://vendor/api",
                            json=payload,
                        )
                        response.raise_for_status()
                        result = response.json()
        
        # Success
        await breaker.record_success()
        return result
    
    except (httpx.HTTPStatusError, httpx.TimeoutException) as e:
        # Failure
        await breaker.record_failure()
        raise
```

---

## 2. Priority Queues (🟡 Pod-Aware IF You Have Backlog)

### What Problem They Solve

In multi-pod systems without a shared queue:

- One pod may be overloaded
- Another pod may be idle
- Request importance is applied inconsistently
- High-priority work gets stuck behind low-priority

---

### Mental Model

> "Important work should not depend on which pod the load balancer chose."

---

### Pod-Local vs Pod-Aware Queues

#### ❌ Pod-Local Queues (Default `asyncio.PriorityQueue`)

```
Load Balancer
  ├─ Pod A → long queue (100 requests)
  ├─ Pod B → empty (0 requests)
  └─ Pod C → medium (20 requests)
```

**Problems**:
- Unfairness (LB chose wrong pod)
- Wasted capacity (Pods B idle while A overloaded)
- Priority inversion (high-priority in A waits, while low-priority in B runs)

---

#### ✅ Pod-Aware Queues (Redis / Message Broker)

```
Load Balancer
  ↓
  [All requests go to shared queue]
  ↓
Shared Priority Queue (Redis)
  ↓
  [Worker pods pull from queue]
  ↓
Pod A, Pod B, Pod C (pull next highest priority)
```

**Benefits**:
- Global ordering
- Consistent prioritization
- Better utilization
- No wasted capacity

---

### When Redis Queue Is REQUIRED

✅ **Yes, use Redis/broker when**:

- Mixed workloads (realtime + batch)
- Different SLAs / user tiers
- High traffic with variable latency
- Background jobs
- Long-running tasks

❌ **Not needed when**:

- All requests are equivalent
- No backlog (requests complete quickly)
- Low traffic
- Strict latency requirements (queue adds overhead)

---

### Pod-Local Priority Queue (Simple Case)

For low traffic or single-pod deployments:

```python
import asyncio
from dataclasses import dataclass, field
from typing import Any


@dataclass(order=True)
class PriorityQueueItem:
    priority: int
    payload: Any = field(compare=False)
    future: asyncio.Future = field(compare=False)


# Per-pod queue
priority_queue = asyncio.PriorityQueue()


async def submit_with_priority(payload: dict, priority: int):
    """
    Submit request with priority.
    Lower number = higher priority.
    """
    future = asyncio.Future()
    item = PriorityQueueItem(priority, payload, future)
    
    await priority_queue.put(item)
    
    return await future


async def worker():
    """
    Worker that processes items from priority queue.
    """
    while True:
        item = await priority_queue.get()
        
        try:
            result = await call_llm(item.payload)
            item.future.set_result(result)
        except Exception as e:
            item.future.set_exception(e)
        finally:
            priority_queue.task_done()
```

> ⚠️ This is **not pod-aware**. Each pod has its own queue.

---

### Pod-Aware Priority Queue (Redis-Backed)

For multi-pod production systems:

```python
import redis.asyncio as redis
import json
import asyncio


class RedisPriorityQueue:
    """
    Shared priority queue using Redis sorted set.
    
    All pods share the same queue.
    """
    
    def __init__(self, redis_client: redis.Redis, key: str):
        self.redis = redis_client
        self.key = key
    
    async def push(self, payload: dict, priority: int) -> str:
        """
        Add item to queue.
        Lower score = higher priority.
        
        Returns:
            Task ID
        """
        task_id = f"{time.time()}:{id(payload)}"
        
        await self.redis.zadd(
            self.key,
            {json.dumps({"id": task_id, "payload": payload}): priority}
        )
        
        return task_id
    
    async def pop(self, timeout: float = 1.0) -> Optional[dict]:
        """
        Pop highest priority item (blocking with timeout).
        
        Returns:
            Item dict or None if timeout.
        """
        # BZPOPMIN: blocking pop with timeout
        result = await self.redis.bzpopmin(self.key, timeout=timeout)
        
        if result:
            key, member, score = result
            return json.loads(member)
        
        return None


# Setup
redis_queue = RedisPriorityQueue(
    redis_client=redis_client,
    key="llm:priority_queue"
)


# Submit work
@app.post("/llm")
async def llm_endpoint(payload: dict, priority: int = 5):
    """
    Endpoint that submits to shared priority queue.
    """
    task_id = await redis_queue.push(payload, priority)
    
    # In practice, you'd have a separate worker that processes
    # and stores results, then return result location
    return {"task_id": task_id, "status": "queued"}


# Worker (runs in each pod)
async def priority_queue_worker():
    """
    Worker that pulls from shared priority queue.
    """
    while True:
        item = await redis_queue.pop(timeout=1.0)
        
        if item:
            try:
                result = await call_llm(item["payload"])
                # Store result somewhere (Redis, DB, etc.)
                await store_result(item["id"], result)
            except Exception as e:
                logger.exception("Worker error", task_id=item["id"])
                await store_error(item["id"], str(e))
```

---

## 3. Adaptive Retry (🟢 Pod-Local by Design)

### What Problem They Solve

Retries are dangerous under partial failure.

Adaptive retry ensures pods **back off independently** based on *current local conditions*.

---

### Mental Model

> "Retries are allowed only when THIS pod can afford them."

---

### Why Adaptive Retry Should Stay Local

Adaptive retry decisions depend on:

- Local latency
- Local queue pressure
- Local semaphore contention
- Global breaker state (already shared via Redis)

They do **not** require consensus between pods.

Each pod should adapt to **its own health**.

---

### Retry Budget Computation

```python
def compute_retry_budget(
    *,
    breaker_open: bool,
    queue_wait_seconds: float,
    recent_error_rate: float,
    semaphore_pressure: float,
) -> int:
    """
    Compute how many retries are safe right now.
    
    Returns:
        Number of retries allowed (0-3).
    """
    
    # No retries if circuit breaker is open
    if breaker_open:
        return 0
    
    # No retries if queue is backing up
    if queue_wait_seconds > 2.0:
        return 0
    
    # No retries if semaphore is saturated
    if semaphore_pressure > 0.9:
        return 0
    
    # Fewer retries if error rate is high
    if recent_error_rate > 0.5:
        return 1
    
    if recent_error_rate > 0.2:
        return 2
    
    # Full retries if system is healthy
    return 3


def get_semaphore_pressure() -> float:
    """
    Calculate semaphore pressure (0.0 - 1.0).
    
    Returns:
        Fraction of semaphore slots in use.
    """
    # This requires tracking (conceptual)
    # In practice, you'd track this in metrics
    return 0.5  # placeholder


async def call_with_adaptive_retry(payload: dict):
    """
    LLM call with adaptive retry budget.
    """
    
    # Compute retry budget based on current conditions
    max_retries = compute_retry_budget(
        breaker_open=await breaker.is_open(),
        queue_wait_seconds=get_average_queue_wait(),
        recent_error_rate=get_recent_error_rate(),
        semaphore_pressure=get_semaphore_pressure(),
    )
    
    for attempt in range(max_retries + 1):
        try:
            return await call_llm_with_breaker(payload)
        
        except RetryableError:
            if attempt == max_retries:
                raise
            
            # Adaptive backoff
            await asyncio.sleep(backoff(attempt))
    
    raise FinalFailure("All retries exhausted")
```

---

### Tracking Local Metrics

```python
from collections import deque
import time


class LocalMetrics:
    """
    Track local pod metrics for adaptive decisions.
    """
    
    def __init__(self, window_size: int = 100):
        self.recent_calls = deque(maxlen=window_size)
        self.queue_waits = deque(maxlen=50)
    
    def record_call(self, success: bool, duration: float):
        """Record a call result"""
        self.recent_calls.append({
            "success": success,
            "duration": duration,
            "timestamp": time.time(),
        })
    
    def record_queue_wait(self, wait_seconds: float):
        """Record time spent waiting in queue"""
        self.queue_waits.append(wait_seconds)
    
    def get_error_rate(self) -> float:
        """Calculate recent error rate"""
        if not self.recent_calls:
            return 0.0
        
        errors = sum(1 for call in self.recent_calls if not call["success"])
        return errors / len(self.recent_calls)
    
    def get_average_queue_wait(self) -> float:
        """Calculate average queue wait time"""
        if not self.queue_waits:
            return 0.0
        
        return sum(self.queue_waits) / len(self.queue_waits)


# Global instance (per-pod)
local_metrics = LocalMetrics()
```

---

## 4. Load Shedding (🟢 Mostly Pod-Local)

### What It Is

**Intentional rejection** to protect the system.

---

### Mental Model

> "If THIS pod is unhealthy, it rejects early — even if other pods don't."

---

### Why Load Shedding Is Usually Local

Signals used:

- Local queue length
- Local latency percentiles
- Local semaphore pressure
- Local CPU / memory
- Local error rate

These signals:
- Change rapidly
- Are not worth synchronizing
- Would lag if centralized

---

### Where Load Shedding Belongs

```
Client
  ↓
Load shedding (local reject)
  ↓
Queue timeout
  ↓
Circuit breaker (global)
  ↓
Rate limiter
  ↓
Semaphore
```

**Earlier = cheaper.**

Reject before doing any work.

---

### Queue-Length Shedding

```python
MAX_QUEUE_SIZE = 100


async def check_queue_pressure():
    """
    Reject if queue is too long.
    """
    if priority_queue.qsize() > MAX_QUEUE_SIZE:
        raise HTTPException(429, "System overloaded - queue full")


@app.post("/llm")
async def llm_endpoint(payload: dict):
    # Shed load early
    await check_queue_pressure()
    
    # Proceed with request
    return await call_llm(payload)
```

---

### Latency-Based Shedding

```python
def should_shed_load() -> bool:
    """
    Shed load if latency is too high.
    """
    p95 = get_p95_latency()
    
    if p95 > SLA_LATENCY * 0.9:
        return True
    
    return False


@app.post("/llm")
async def llm_endpoint(payload: dict):
    if should_shed_load():
        raise HTTPException(503, "Service temporarily overloaded")
    
    return await call_llm(payload)
```

---

### Tier-Based Shedding

```python
def should_shed_for_tier(tier: str) -> bool:
    """
    Shed low-tier users under pressure.
    """
    pressure = get_system_pressure()  # 0.0 - 1.0
    
    if pressure > 0.9:
        # Under extreme pressure, only serve premium
        return tier != "premium"
    
    elif pressure > 0.7:
        # Under moderate pressure, shed free tier
        return tier == "free"
    
    return False


@app.post("/llm")
async def llm_endpoint(
    payload: dict,
    tier: str = "free",
):
    if should_shed_for_tier(tier):
        raise HTTPException(
            429,
            f"Service under pressure - {tier} tier temporarily limited"
        )
    
    return await call_llm(payload)
```

---

## 5. Pod-Aware End-to-End Call Flow

Complete flow with all mechanisms:

```
Request arrives
  ↓
1. Load shedding (local, fast reject)
  ↓
2. User rate limit check (global, Redis)
  ↓
3. Queue timeout (local, wait limit)
  ↓
4. Circuit breaker check (global, Redis)
  ↓
5. Priority queue (optional, Redis if needed)
  ↓
6. Global vendor rate limiter (Redis)
  ↓
7. Local rate limiter (optional, burst smoothing)
  ↓
8. Semaphore (local, capacity)
  ↓
9. Call timeout
  ↓
10. Vendor call (HTTP client with timeouts)
  ↓
11. Adaptive retry (local decision)
```

---

### Combined Implementation

```python
async def complete_llm_call(
    payload: dict,
    user_id: str,
    tier: str,
    priority: int = 5,
) -> dict:
    """
    Complete production LLM call with all safeguards.
    """
    
    # 1. Load shedding (local)
    if should_shed_for_tier(tier):
        raise HTTPException(429, "Service under pressure")
    
    # 2. User rate limit (global)
    await check_user_rate_limit(user_id, tier)
    
    # 3. Queue timeout + circuit breaker
    try:
        async with asyncio.timeout(5):
            # 4. Circuit breaker (global)
            await breaker.allow()
            
            # 5. Global vendor rate limiter
            await vendor_limiter.wait_and_acquire(timeout=3.0)
            
            # 6. Local rate limiter (optional)
            async with llm_rate_local:
                
                # 7. Semaphore (local capacity)
                async with llm_sem:
                    
                    # 8. Call timeout
                    async with asyncio.timeout(30):
                        response = await client.post(
                            "https://vendor/api",
                            json=payload,
                        )
                        response.raise_for_status()
                        result = response.json()
            
            # Success
            await breaker.record_success()
            local_metrics.record_call(success=True, duration=...)
            
            return result
    
    except CircuitBreakerOpen:
        raise HTTPException(503, "Service temporarily unavailable")
    
    except VendorRateLimitExceeded:
        raise HTTPException(429, "Vendor rate limit exceeded")
    
    except asyncio.TimeoutError:
        await breaker.record_failure()
        local_metrics.record_call(success=False, duration=...)
        raise HTTPException(504, "Request timeout")
    
    except httpx.HTTPStatusError as e:
        await breaker.record_failure()
        local_metrics.record_call(success=False, duration=...)
        
        if 500 <= e.response.status_code < 600:
            # Retry with adaptive budget
            return await call_with_adaptive_retry(payload)
        
        raise HTTPException(502, f"Vendor error: {e.response.status_code}")
```

---

## 6. Pod-Awareness Rules (Non-Negotiable)

1. ✅ Circuit breakers **must be shared** (Redis)
2. ✅ Vendor rate limiters **must be shared** (Redis)
3. ✅ User rate limiters **must be shared** (Redis)
4. ⚠️ Priority queues are shared **only if backlog exists**
5. ❌ Adaptive retries are always **local**
6. ❌ Load shedding is **early and local**
7. ❌ Semaphores are always **local** (per-pod capacity)
8. ❗ Never sleep while holding semaphores
9. ❗ Never retry during overload
10. ❗ Global limits protect vendors, local limits protect pods

---

## 7. When to Add These Patterns

### Start With (Baseline)

- Semaphore (local capacity)
- Call timeout
- Queue timeout
- Basic retry logic
- User rate limiting (Redis)
- Global vendor rate limiter (Redis)

### Add When Needed

**Circuit breaker** (Redis):
- Frequent vendor outages
- Cascading failures observed
- Need coordinated failure across pods

**Priority queues** (Redis):
- Mixed workloads (realtime + batch)
- Different SLAs
- Long queues

**Adaptive retry**:
- High error rates
- Variable latency
- Need to reduce retry storms

**Load shedding**:
- Traffic spikes
- Tier-based service
- Need graceful degradation

---

## Final Thought

In distributed systems:

> **Correctness is not local. Failure must be coordinated.**

A pod-aware system does not try to be perfect —
it ensures **all pods fail together, on purpose, and fast**.

This prevents:
- Cascading failures
- Retry storms
- Vendor limit violations
- Split-brain scenarios
- Resource exhaustion

**The right architecture makes failure safe, predictable, and recoverable.**

---

## Summary: What Lives Where

| Mechanism              | Scope  | Storage    | Purpose                        |
| ---------------------- | ------ | ---------- | ------------------------------ |
| Semaphore              | Local  | In-memory  | Pod capacity protection        |
| Local rate limiter     | Local  | In-memory  | Burst smoothing                |
| Queue timeout          | Local  | In-memory  | Admission control              |
| Load shedding          | Local  | In-memory  | Early rejection                |
| Adaptive retry         | Local  | In-memory  | Conditional retry              |
| Circuit breaker        | Global | Redis      | Coordinated failure            |
| Vendor rate limiter    | Global | Redis      | Vendor contract enforcement    |
| User rate limiter      | Global | Redis      | Fairness enforcement           |
| Priority queue         | Global | Redis      | Global ordering (if needed)    |

---

**This completes the comprehensive guide to safe, scalable LLM and agent calls in production FastAPI services.**

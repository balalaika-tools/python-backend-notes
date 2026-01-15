# Part 4: Complete Production Architecture — Full Stack

> **Principle**: Each layer has a **non-overlapping responsibility**.

This guide defines the **complete production architecture** for protecting your FastAPI service from inbound floods, enforcing fairness, respecting vendor contracts, and preventing pod collapse.

---

## 1. High-Level Architecture Overview

```text
Internet
  ↓
API Gateway / Ingress Controller
  ↓
Kubernetes Service (Load Balancer)
  ↓
Ingress Routing & Readiness Checks
  ↓
ASGI Server (Uvicorn/Gunicorn) — Per-Pod Admission Control
  ↓
FastAPI Application
  ├─ User/Endpoint Rate Limiting (Redis)
  ├─ Business Logic
  └─ External Vendor Call Pipeline
      ├─ Global Vendor Rate Limiter (Redis)
      ├─ Local Rate Limiter (burst smoothing)
      ├─ Semaphore (capacity)
      └─ HTTP Client
  ↓
External Vendor APIs
```

---

## 2. Layer 1: API Gateway / Ingress Controller

### Role

Protect the **entire cluster** from excessive or malicious inbound traffic.

### Scope

Cluster-wide, **before traffic reaches any pod**.

---

### 1️⃣ Global Request Rate Limiting

> "How much traffic is allowed into the system?"

**Example policies**:

```yaml
# nginx-ingress example
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  annotations:
    nginx.ingress.kubernetes.io/limit-rps: "2000"
    nginx.ingress.kubernetes.io/limit-connections: "5000"
```

or

```yaml
# Kong Gateway example
rate_limiting:
  minute: 10000
  hour: 100000
  policy: cluster
```

**Stops**:
- DDoS floods
- Bot traffic
- Accidental infinite loops
- Abusive clients

---

### 2️⃣ Per-IP Rate Limiting

> "How much traffic per individual client?"

**Example**:

```yaml
nginx.ingress.kubernetes.io/limit-rpm: "100"
```

**Stops**:
- Single client floods
- Runaway scripts
- Misconfigured clients

---

### 3️⃣ Connection Limiting

> "How many open sockets do we tolerate?"

**Example**:

```yaml
nginx.ingress.kubernetes.io/limit-connections: "20"  # per IP
```

**Stops**:
- Slowloris attacks
- Connection exhaustion
- Keep-alive abuse

---

### 4️⃣ Bounded Buffering

> "We do not queue unlimited requests."

**Configuration**:

```nginx
# nginx example
proxy_buffering on;
proxy_buffer_size 4k;
proxy_buffers 8 4k;
```

**Effect**:
- Small internal queues
- Early rejection with `429` / `503`
- No application buffering

---

### What the Gateway Does NOT Do

❌ User-level fairness (application logic)
❌ Business rules (tenant quotas, etc.)
❌ Vendor API protection (downstream)
❌ Retry or async fan-out awareness

**Rule**:

> Gateway protects **infrastructure**, not business logic.

---

## 3. Layer 2: Ingress Routing & Readiness

### Role

Route traffic **only to healthy pods**.

### Scope

Cluster-wide, **reactive protection**.

---

### How It Works

1. Each pod exposes a readiness endpoint
2. Kubernetes probes it periodically
3. If readiness fails → pod removed from service
4. Ingress stops routing traffic to it
5. Traffic shifts to healthy pods

---

### Readiness Probe Configuration

```yaml
# kubernetes deployment
apiVersion: apps/v1
kind: Deployment
spec:
  template:
    spec:
      containers:
      - name: fastapi
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          timeoutSeconds: 2
          failureThreshold: 3
```

---

### FastAPI Readiness Endpoint

```python
from fastapi import FastAPI, Response

app = FastAPI()


def queue_size() -> int:
    """Get current queue size (conceptual)"""
    # In practice, track this in your metrics
    return 0


def recent_error_rate() -> float:
    """Calculate recent error rate"""
    # Track last N requests
    return 0.0


@app.get("/ready")
async def readiness():
    """
    Readiness probe - can this pod handle traffic?
    
    Checks:
    - Semaphore not saturated
    - Queue not full
    - Recent error rate acceptable
    - Dependencies reachable
    """
    
    # Check 1: Pod overloaded?
    if llm_sem.locked() and queue_size() > 80:
        return Response(
            status_code=503,
            content='{"status": "not ready", "reason": "pod overloaded"}',
            media_type="application/json",
        )
    
    # Check 2: High error rate?
    if recent_error_rate() > 0.5:
        return Response(
            status_code=503,
            content='{"status": "not ready", "reason": "high error rate"}',
            media_type="application/json",
        )
    
    # Check 3: Dependencies healthy?
    # (Check Redis, database, etc.)
    
    return {"status": "ready"}
```

**Kubernetes will**:
- Remove unhealthy pods from service
- Stop routing new connections
- Allow existing connections to drain
- Shift load to healthy pods

---

### Liveness vs Readiness

| Probe      | Question                    | Action if fails         |
| ---------- | --------------------------- | ----------------------- |
| Liveness   | Is the process alive?       | Restart pod             |
| Readiness  | Can it handle traffic?      | Remove from service     |

**Rule**:

> Liveness = "restart me"
> Readiness = "don't route to me"

---

## 4. Layer 3: ASGI Server — Pod Admission Control

### Role

Answer: **"Should this pod accept another request right now?"**

### Scope

Per-pod, **hard capacity protection**.

---

### What This Is NOT

This is **not rate limiting**.
This is **admission control**.

It prevents:
- Pod collapse
- Memory blowups
- Unbounded coroutine creation
- Event loop starvation

---

### ASGI Server Configuration

This happens **before FastAPI code runs**.

#### Uvicorn (Standalone)

```bash
uvicorn app:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 1 \
  --limit-concurrency 50 \
  --backlog 100 \
  --timeout-keep-alive 5
```

**Meaning**:

| Flag                   | Purpose                                |
| ---------------------- | -------------------------------------- |
| `--limit-concurrency`  | Max in-flight requests per worker      |
| `--backlog`            | Queued connections before refusal      |
| `--timeout-keep-alive` | Keep-alive timeout                     |

**Effect**:

- Max 50 concurrent requests handled
- Up to 100 queued connections
- Requests beyond this are **rejected early**

---

#### Gunicorn + Uvicorn Workers

```bash
gunicorn app:app \
  -k uvicorn.workers.UvicornWorker \
  --workers 2 \
  --worker-connections 50 \
  --backlog 100 \
  --timeout 60
```

**Effective limit**:

```
max concurrent = workers × worker-connections
max concurrent = 2 × 50 = 100
```

---

### Why This Matters (Even With Rate Limits)

**Key distinction**:

| Mechanism          | Question           | When applied        |
| ------------------ | ------------------ | ------------------- |
| Rate limiting      | "How often?"       | Per time window     |
| Admission control  | "How many at once?"| Per moment          |

**Without admission control**:

- A single legal burst can kill the pod
- Rate limits alone cannot prevent overload
- All rate-limited requests might arrive simultaneously

**Example**:

```
Rate limit: 100 req/min
At t=0: all 100 requests arrive
Without admission control:
  → 100 async tasks start
  → Pod collapses
```

---

## 5. Layer 4: FastAPI — User-Level Fairness & Business Rules

### Role

Enforce fairness based on **application logic**.

### Scope

Shared across pods via **Redis** or similar.

---

### 1️⃣ User / API Key Rate Limiting (Global)

> "How many requests is this user allowed to make?"

**Implementation**: Redis-backed rate limiter

```python
from limits import RateLimitItemPerMinute
from limits.storage import RedisStorage
from limits.strategies import FixedWindowRateLimiter
from fastapi import HTTPException, Header
from typing import Optional

# Setup (at startup)
storage = RedisStorage("redis://redis:6379")
limiter = FixedWindowRateLimiter(storage)

# Define limits per tier
RATE_LIMITS = {
    "free": RateLimitItemPerMinute(10),
    "pro": RateLimitItemPerMinute(100),
    "enterprise": RateLimitItemPerMinute(1000),
}


async def check_user_rate_limit(
    user_id: str,
    tier: str = "free",
) -> None:
    """
    Check if user has exceeded their rate limit.
    Raises HTTPException(429) if exceeded.
    """
    limit = RATE_LIMITS.get(tier, RATE_LIMITS["free"])
    
    if not limiter.hit(limit, f"user:{user_id}"):
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded for tier: {tier}",
            headers={
                "X-RateLimit-Limit": str(limit.amount),
                "X-RateLimit-Window": f"{limit.per}s",
            },
        )


@app.post("/llm")
async def llm_endpoint(
    payload: dict,
    x_api_key: Optional[str] = Header(None),
):
    # Lookup user and tier
    user_id, tier = await get_user_from_api_key(x_api_key)
    
    # Check user rate limit (global, Redis-backed)
    await check_user_rate_limit(user_id, tier)
    
    # Proceed with request
    return await call_llm(payload)
```

---

### 2️⃣ Per-Endpoint Rate Limiting (Optional)

Some endpoints are heavier or more expensive.

```python
ENDPOINT_LIMITS = {
    "/chat": RateLimitItemPerMinute(20),
    "/search": RateLimitItemPerMinute(100),
    "/analyze": RateLimitItemPerMinute(5),
}


async def check_endpoint_rate_limit(
    user_id: str,
    endpoint: str,
) -> None:
    limit = ENDPOINT_LIMITS.get(endpoint)
    if limit:
        key = f"user:{user_id}:endpoint:{endpoint}"
        if not limiter.hit(limit, key):
            raise HTTPException(429, f"Endpoint rate limit exceeded")
```

**Why this cannot live at the gateway**:

- Gateway doesn't know business logic
- User identity might require JWT validation
- Tier-based limits require database lookups

---

### 3️⃣ Semaphore — Per-Pod Capacity Guard

> "Can this pod survive another expensive operation?"

```python
# Per-pod, in-memory
llm_sem = asyncio.Semaphore(50)
```

**Purpose**:
- Protect CPU, memory, connections
- Prevent pod overload
- NOT a rate limiter

---

## 6. Layer 5: Outbound Vendor Protection (Critical)

### The Problem

**Inbound limits do not protect vendors.**

Vendor limits are:
- Global (shared across all pods)
- API-key / account scoped
- Strictly enforced by vendor

---

### 7️⃣ Global Vendor Rate Limiter (Redis)

**Role**: Enforce vendor contract across the entire cluster

**Scope**: All pods, all retries

Every outbound vendor call **must pass through this**.

---

### Implementation: Redis Token Bucket

```python
import redis.asyncio as redis
import time
from fastapi import HTTPException


class VendorRateLimitExceeded(Exception):
    pass


class GlobalVendorRateLimiter:
    """
    Redis-backed global rate limiter for vendor API calls.
    
    Uses sliding window algorithm.
    """
    
    def __init__(
        self,
        redis_client: redis.Redis,
        vendor_key: str,
        limit: int,
        window_seconds: int = 60,
    ):
        self.redis = redis_client
        self.key = f"vendor:rate:{vendor_key}"
        self.limit = limit
        self.window = window_seconds
    
    async def acquire(self) -> bool:
        """
        Try to acquire a token for a vendor call.
        
        Returns:
            True if token acquired, False if rate limit exceeded.
        """
        now = time.time()
        window_start = now - self.window
        
        # Use pipeline for atomic operations
        pipe = self.redis.pipeline()
        
        # Remove old entries outside window
        pipe.zremrangebyscore(self.key, 0, window_start)
        
        # Count current entries in window
        pipe.zcard(self.key)
        
        results = await pipe.execute()
        count = results[1]
        
        # Check if under limit
        if count >= self.limit:
            return False
        
        # Add new entry
        await self.redis.zadd(self.key, {f"{now}": now})
        
        # Set expiry (cleanup)
        await self.redis.expire(self.key, self.window + 10)
        
        return True
    
    async def wait_and_acquire(self, timeout: float = 5.0) -> None:
        """
        Wait up to timeout seconds to acquire a token.
        
        Raises:
            VendorRateLimitExceeded if timeout exceeded.
        """
        start = time.time()
        
        while True:
            if await self.acquire():
                return
            
            elapsed = time.time() - start
            if elapsed > timeout:
                raise VendorRateLimitExceeded(
                    f"Could not acquire vendor token within {timeout}s"
                )
            
            # Small sleep before retry
            await asyncio.sleep(0.1)


# Setup (at startup)
vendor_limiter = GlobalVendorRateLimiter(
    redis_client=redis_client,
    vendor_key="openai",
    limit=500,  # 500 req/min
    window_seconds=60,
)


async def call_llm(payload: dict):
    """
    LLM call with global vendor rate limiting.
    """
    for attempt in range(3):
        try:
            async with asyncio.timeout(5):  # Queue timeout
                async with llm_rate_local:  # Local smoothing
                    
                    # GLOBAL VENDOR PROTECTION
                    await vendor_limiter.wait_and_acquire(timeout=3.0)
                    
                    async with llm_sem:  # Local capacity
                        async with asyncio.timeout(30):  # Call timeout
                            response = await client.post(
                                "https://vendor/api",
                                json=payload,
                            )
                            response.raise_for_status()
                            return response.json()
        
        except VendorRateLimitExceeded:
            # Global rate limit hit
            if attempt < 2:
                await asyncio.sleep(backoff(attempt))
                continue
            raise HTTPException(429, "Vendor rate limit exceeded")
        
        except httpx.TimeoutException:
            if attempt < 2:
                await asyncio.sleep(backoff(attempt))
                continue
            raise FinalFailure("Vendor timeout")
    
    raise FinalFailure("All retries exhausted")
```

---

## 7. Complete Execution Order (Critical)

The order in which controls are applied **matters**.

```text
1. Incoming request
   ↓
2. API Gateway limits (flood protection)
   ↓
3. Ingress routing (readiness checks)
   ↓
4. ASGI admission control (per-pod capacity)
   ↓
5. FastAPI user/endpoint limits (Redis, fairness)
   ↓
6. Business logic / validation
   ↓
7. Queue timeout (start waiting)
   ↓
8. Local rate limiter (burst smoothing, optional)
   ↓
9. GLOBAL vendor rate limiter (Redis, vendor protection)
   ↓
10. Semaphore (local concurrency)
    ↓
11. Call timeout (per-attempt budget)
    ↓
12. HTTP client (with timeouts)
    ↓
13. Vendor API
    ↓
14. Retry logic (if needed)
```

---

### Why Order Matters

**Rule**:

> **Reject before waiting. Wait before reserving. Reserve before calling.**

| Stage                  | Cost                | Action         |
| ---------------------- | ------------------- | -------------- |
| Gateway reject         | Minimal             | Fast reject    |
| User limit exceeded    | Cheap (Redis GET)   | Fast reject    |
| Queue timeout          | Medium (async wait) | Wait or reject |
| Semaphore              | Expensive (slot)    | Reserve        |
| Vendor call            | Very expensive      | Execute        |

**Anti-pattern**:

```python
# WRONG: Semaphore before checks
async with llm_sem:
    if not check_user_rate_limit():
        raise HTTPException(429)
    await vendor_call()
```

This wastes semaphore slots on rejected requests.

**Correct**:

```python
# RIGHT: Checks before semaphore
if not check_user_rate_limit():
    raise HTTPException(429)

async with llm_sem:
    await vendor_call()
```

---

## 8. Responsibility Matrix

Clear separation of concerns:

| Concern                | Gateway | Ingress | ASGI | FastAPI   | Vendor Call |
| ---------------------- | ------- | ------- | ---- | --------- | ----------- |
| Flood protection       | ✅       | ❌       | ❌    | ❌         | ❌           |
| Total RPS ceiling      | ✅       | ❌       | ❌    | ❌         | ❌           |
| Per-IP limits          | ✅       | ❌       | ❌    | ❌         | ❌           |
| Pod health routing     | ❌       | ✅       | ❌    | ❌         | ❌           |
| Pod admission control  | ❌       | ❌       | ✅    | ❌         | ❌           |
| Per-user fairness      | ❌       | ❌       | ❌    | ✅ (Redis) | ❌           |
| Endpoint limits        | ❌       | ❌       | ❌    | ✅         | ❌           |
| Business logic         | ❌       | ❌       | ❌    | ✅         | ❌           |
| Local capacity         | ❌       | ❌       | ❌    | ✅ (sem)   | ❌           |
| Vendor quotas          | ❌       | ❌       | ❌    | ❌         | ✅ (Redis)   |

---

## 9. Minimal, Non-Overengineered Setup

For a typical production system:

### Gateway

- Total RPS limit: `2000/sec`
- Per-IP limit: `100/sec`
- Connection limits: `20 per IP`

### Ingress

- Readiness probes: every 5s
- Failure threshold: 3 consecutive failures

### ASGI (Uvicorn)

- `--limit-concurrency 50`
- `--backlog 100`

### FastAPI

- User rate limiter: Redis-backed
- Semaphore: `50`
- Local rate limiter: `80/min` (optional)
- Global vendor limiter: Redis-backed, `500/min`

This covers **all critical failure modes** without over-engineering.

---

## 10. Deployment Configuration Example

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fastapi-app
spec:
  replicas: 10
  template:
    spec:
      containers:
      - name: app
        image: myapp:latest
        command:
          - uvicorn
          - app:app
          - --host=0.0.0.0
          - --port=8000
          - --limit-concurrency=50
          - --backlog=100
        
        ports:
        - containerPort: 8000
        
        resources:
          requests:
            cpu: "500m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1Gi"
        
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10
        
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3
        
        env:
        - name: REDIS_URL
          value: "redis://redis:6379"
```

---

### Nginx Ingress

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: fastapi-ingress
  annotations:
    nginx.ingress.kubernetes.io/limit-rps: "2000"
    nginx.ingress.kubernetes.io/limit-connections: "5000"
    nginx.ingress.kubernetes.io/limit-rpm: "100"  # per IP
spec:
  rules:
  - host: api.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: fastapi-service
            port:
              number: 8000
```

---

## Final Mental Model

> **Gateway**: who may enter
> **Ingress**: which pod is healthy
> **ASGI**: can this pod accept work
> **FastAPI**: who gets how much
> **Redis vendor limiter**: when we may call vendors

Each layer protects a different resource:

- Gateway → infrastructure
- Ingress → cluster
- ASGI → pod
- FastAPI → users and business rules
- Vendor limiter → external contracts

---

## Final Verdict

This architecture:

✅ Survives floods and bursts
✅ Enforces fairness
✅ Respects vendor contracts
✅ Prevents pod collapse
✅ Works with Kubernetes autoscaling
✅ No hidden coupling
✅ No redundant limits
✅ Clear responsibilities

> **Rate limits control "how often".**
> **Admission control decides "whether at all".**

This is **canonical, production-grade architecture** for FastAPI services calling external APIs.

---

**Next**: Part 5 covers advanced topics including pod-aware circuit breakers, priority queues, adaptive retry, and load shedding strategies.

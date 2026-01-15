# Part 2: Production Implementation — FastAPI Integration

This guide covers **complete FastAPI integration patterns**, including endpoint setup, shielded cleanup, SDK considerations, and what clients experience.

---

## 1. Minimal FastAPI Integration

```python
from fastapi import FastAPI, HTTPException
import asyncio

app = FastAPI()


@app.post("/llm")
async def llm_endpoint(payload: dict):
    """
    Complete LLM endpoint with SLA boundary protection
    """
    try:
        # SLA boundary: absolute maximum latency for this request
        async with asyncio.timeout(60):
            return await call_llm(payload)
    
    except asyncio.TimeoutError:
        raise HTTPException(504, "Request timeout")
    
    except FinalFailure as e:
        raise HTTPException(502, f"Upstream failure: {str(e)}")
    
    except Exception as e:
        # Log unexpected errors
        logger.exception("Unexpected error in LLM endpoint")
        raise HTTPException(500, "Internal server error")
```

**What this ensures**:
- Predictable upper-bound latency
- No runaway requests
- Clean error responses
- Proper HTTP status codes

---

## 2. What the Client Sees

| Situation              | HTTP Status | Client Experience           |
| ---------------------- | ----------- | --------------------------- |
| Queue overload         | 504 / 429   | Fast fail                   |
| Vendor slow            | 200         | Retry succeeded             |
| Vendor down            | 502         | Controlled failure          |
| Rate limit hit         | —           | Request waits (transparent) |
| System healthy         | 200         | Normal latency              |
| All retries exhausted  | 502         | Final failure               |
| SLA timeout            | 504         | Gateway timeout             |

**You decide where to cut.**

---

## 3. Complete Production Call Pattern

This pattern includes all production safeguards:

```python
import asyncio
import httpx
from typing import Optional
import structlog

logger = structlog.get_logger()


class RetryableError(Exception):
    pass


class FinalFailure(Exception):
    pass


def backoff(attempt: int) -> float:
    """Exponential backoff with jitter"""
    import random
    base = min(2 ** attempt, 32)
    return base + random.uniform(0, 1)


async def call_llm(
    payload: dict,
    *,
    request_id: Optional[str] = None,
) -> dict:
    """
    Production-grade LLM call with:
    - Structured logging
    - Metrics (conceptual)
    - Proper exception handling
    - Retry logic
    - All timeout layers
    """
    
    log = logger.bind(
        request_id=request_id,
        payload_keys=list(payload.keys()),
    )
    
    for attempt in range(3):
        log = log.bind(attempt=attempt)
        
        try:
            # Queue timeout: admission control
            async with asyncio.timeout(5):
                log.debug("acquiring_rate_limit")
                
                async with llm_rate:
                    log.debug("acquiring_semaphore")
                    
                    async with llm_sem:
                        log.info("calling_vendor")
                        
                        # Call timeout: per-attempt latency control
                        async with asyncio.timeout(30):
                            response = await client.post(
                                "https://vendor/api",
                                json=payload,
                                headers={"X-Request-ID": request_id} if request_id else {},
                            )
                            response.raise_for_status()
                            
                            result = response.json()
                            
                            log.info(
                                "vendor_success",
                                status_code=response.status_code,
                                attempt=attempt,
                            )
                            
                            # TODO: record_success_metric()
                            
                            return result
        
        except httpx.TimeoutException as e:
            log.warning(
                "vendor_timeout",
                exception=str(e),
                attempt=attempt,
            )
            
            if attempt < 2:
                await asyncio.sleep(backoff(attempt))
                continue
            
            # TODO: record_timeout_metric()
            raise FinalFailure(f"Vendor timeout after {attempt + 1} attempts")
        
        except httpx.HTTPStatusError as e:
            log.warning(
                "vendor_http_error",
                status_code=e.response.status_code,
                attempt=attempt,
            )
            
            # 5xx → retry
            if 500 <= e.response.status_code < 600:
                if attempt < 2:
                    await asyncio.sleep(backoff(attempt))
                    continue
            
            # 4xx → don't retry
            raise FinalFailure(f"Vendor error: {e.response.status_code}")
        
        except asyncio.TimeoutError:
            log.warning(
                "timeout_error",
                attempt=attempt,
            )
            
            # First attempt timeout → might be call timeout, try once more
            if attempt == 0:
                await asyncio.sleep(backoff(attempt))
                continue
            
            # Subsequent timeout → likely system overload
            raise FinalFailure(f"Timeout after {attempt + 1} attempts")
        
        except Exception as e:
            log.error(
                "unexpected_error",
                exception=str(e),
                exception_type=type(e).__name__,
            )
            raise
    
    raise FinalFailure("All retries exhausted")
```

---


## 4. Shielded Cleanup — When and Why

### The Problem

When any of these happen:
- SLA boundary hit
- Client disconnect
- Timeout
- Cancellation

👉 The task receives `CancelledError`.

If you have critical cleanup operations:
- Logging
- Metrics
- Releasing external locks
- Persisting partial state
- Notifying other services

⚠️ **These will NOT run unless you protect them.**

---

### What "Shielded" Means

> "This part must run EVEN IF the request is cancelled."

You do this with `asyncio.shield()`.

---

### Basic Pattern

```python
async def call_llm_with_cleanup(payload: dict):
    try:
        async with asyncio.timeout(60):
            return await actual_llm_work(payload)
    
    except asyncio.TimeoutError:
        # Shield the cleanup from cancellation
        await asyncio.shield(cleanup_after_timeout(payload))
        raise
    
    except Exception:
        await asyncio.shield(cleanup_after_error(payload))
        raise
```

**What happens**:
- The main task is cancelled
- `cleanup_after_timeout()`:
  - **is not cancelled**
  - runs to completion
- The exception is re-raised

---

### What MUST Go Into Shielded Cleanup

✅ **YES**:
- Metrics recording (`record_timeout()`)
- Tracing / observability
- Releasing *external* resources
- Marking a job as failed in a queue
- Notifying an orchestrator
- Final state persistence

❌ **NO**:
- Retries
- New vendor calls
- Heavy computation
- Anything slow or unbounded

> ❗ Shielded cleanup must be **fast and bounded**.

---

### Production Pattern

```python
async def record_sla_violation(
    request_id: str,
    duration: float,
) -> None:
    """
    Fast, bounded cleanup operation
    """
    logger.error(
        "sla_violation",
        request_id=request_id,
        duration=duration,
    )
    # TODO: record_metric("sla_violation", 1)


@app.post("/llm")
async def llm_endpoint(payload: dict, request_id: str):
    import time
    start = time.time()
    
    try:
        async with asyncio.timeout(60):
            return await call_llm(payload, request_id=request_id)
    
    except asyncio.TimeoutError:
        duration = time.time() - start
        
        # Shield cleanup from cancellation
        await asyncio.shield(
            record_sla_violation(request_id, duration)
        )
        
        raise HTTPException(504, "Request timeout")
```

---

## 5. SDK Retries: Disable or Account For

Many vendor SDKs (OpenAI, Anthropic, etc.) have built-in retries.

### The Problem

```
Your retry × SDK retry × vendor retry = retry storm
```

If your code retries 3 times, and the SDK retries 3 times:
- **Actual attempts = 3 × 3 = 9**
- Rate limits blown
- Latency multiplied
- Cascading failures

---

### Two Approaches

#### 1️⃣ Disable SDK Retries (Recommended)

```python
# OpenAI example
import openai

client = openai.AsyncClient(
    max_retries=0,  # YOU control retries
    timeout=30.0,
)
```

#### 2️⃣ Account for SDK Retries

If you can't disable them:

```python
# SDK will retry 3 times internally
# So your outer retry should be 1
for attempt in range(1):  # Only ONE outer retry
    try:
        result = await sdk_call()
        break
    except Exception:
        if attempt == 0:
            await asyncio.sleep(backoff(attempt))
```

**Rule**:

> One retry layer. Yours. Control it explicitly.

---

## 6. Health Checks and Readiness

```python
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/health")
async def health():
    """Liveness probe - is the app running?"""
    return {"status": "healthy"}


@app.get("/ready")
async def readiness():
    """
    Readiness probe - can the app handle traffic?
    
    Checks:
    - Semaphore not saturated
    - Rate limiter responsive
    - Recent error rate acceptable
    """
    
    # Example checks
    if llm_sem.locked() and queue_size() > 80:
        return Response(
            status_code=503,
            content='{"status": "not ready", "reason": "overloaded"}',
        )
    
    if recent_error_rate() > 0.5:
        return Response(
            status_code=503,
            content='{"status": "not ready", "reason": "high error rate"}',
        )
    
    return {"status": "ready"}
```

**Kubernetes will**:
- Remove pod from service if readiness fails
- Stop routing traffic to it
- Shift load to healthy pods

---

## 7. Observability Considerations

### Structured Logging

```python
import structlog

logger = structlog.get_logger()

# Always log with context
logger.info(
    "vendor_call_success",
    request_id=request_id,
    attempt=attempt,
    duration_ms=duration * 1000,
    status_code=response.status_code,
)
```

---

### Key Metrics to Track

| Metric                          | Type      | Purpose                        |
| ------------------------------- | --------- | ------------------------------ |
| `llm_calls_total`               | Counter   | Total calls                    |
| `llm_call_duration_seconds`     | Histogram | Latency distribution           |
| `llm_errors_total`              | Counter   | Error count by type            |
| `llm_retries_total`             | Counter   | Retry attempts                 |
| `llm_queue_timeout_total`       | Counter   | Admission failures             |
| `llm_call_timeout_total`        | Counter   | Call timeouts                  |
| `llm_semaphore_wait_seconds`    | Histogram | Queue time at semaphore        |
| `llm_rate_limit_wait_seconds`   | Histogram | Queue time at rate limiter     |
| `llm_concurrent_calls`          | Gauge     | Current in-flight calls        |

---

## 8. Testing Considerations

### Unit Tests

```python
import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
async def test_call_llm_success():
    """Test successful LLM call"""
    
    mock_response = AsyncMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": "success"}
    mock_response.raise_for_status = AsyncMock()
    
    with patch('httpx.AsyncClient.post', return_value=mock_response):
        result = await call_llm({"prompt": "test"})
        
        assert result == {"result": "success"}


@pytest.mark.asyncio
async def test_call_llm_timeout():
    """Test timeout handling"""
    
    with patch('httpx.AsyncClient.post', side_effect=httpx.TimeoutException("timeout")):
        with pytest.raises(FinalFailure):
            await call_llm({"prompt": "test"})


@pytest.mark.asyncio
async def test_call_llm_retry_on_5xx():
    """Test retry on 5xx errors"""
    
    # First call fails, second succeeds
    responses = [
        httpx.HTTPStatusError("500", request=None, response=AsyncMock(status_code=500)),
        AsyncMock(status_code=200, json=lambda: {"result": "success"}),
    ]
    
    with patch('httpx.AsyncClient.post', side_effect=responses):
        result = await call_llm({"prompt": "test"})
        
        assert result == {"result": "success"}
```

---

### Integration Tests

```python
@pytest.mark.asyncio
async def test_endpoint_timeout():
    """Test SLA boundary timeout"""
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Mock slow vendor
        with patch('call_llm', side_effect=asyncio.sleep(100)):
            response = await ac.post(
                "/llm",
                json={"prompt": "test"},
                timeout=70,  # Longer than SLA
            )
            
            assert response.status_code == 504
```

---

## 9. Production Checklist

Before deploying:

- [ ] Global primitives (semaphore, rate limiter, client) initialized at startup
- [ ] HTTP client timeouts configured
- [ ] Queue timeout set (admission control)
- [ ] Call timeout set per attempt
- [ ] Retry logic outside semaphore
- [ ] Proper exception handling (httpx vs asyncio)
- [ ] SLA boundary at endpoint
- [ ] Shielded cleanup for critical operations
- [ ] Structured logging with request IDs
- [ ] Metrics instrumentation
- [ ] Health and readiness endpoints
- [ ] SDK retries disabled or accounted for
- [ ] Tests for success, failure, timeout cases

---

## Final Pattern Summary

```python
# Startup
app = FastAPI()
llm_sem = asyncio.Semaphore(50)
llm_rate = AsyncLimiter(60, 60)
client = httpx.AsyncClient(timeout=...)

# Call pattern
async def call_llm(payload):
    for attempt in range(3):
        try:
            async with asyncio.timeout(5):      # Queue timeout
                async with llm_rate:            # Rate limit
                    async with llm_sem:         # Semaphore
                        async with asyncio.timeout(30):  # Call timeout
                            return await client.post(...)
        except (httpx exceptions, asyncio.TimeoutError):
            # Handle and retry
            ...

# Endpoint
@app.post("/llm")
async def endpoint(payload):
    try:
        async with asyncio.timeout(60):  # SLA
            return await call_llm(payload)
    except asyncio.TimeoutError:
        await asyncio.shield(cleanup())
        raise HTTPException(504)
```

---

**Next**: Part 3 covers Kubernetes and multi-pod considerations: why per-pod limits don't protect vendors, and how to handle bursty traffic.

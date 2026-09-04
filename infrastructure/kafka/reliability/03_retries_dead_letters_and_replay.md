# Recovery Paths Must Preserve the Evidence of Failure

> **Who this is for**: engineers handling transient failures and poison records.

## Retry by failure class, not by exception count

A timeout may succeed on retry; an invalid currency will not. Retry transient failures with bounded
backoff. Route a repeatedly unprocessable record to a **dead-letter topic (DLT)** with its original
topic, partition, offset, key, payload reference, error class, and attempt count.

```text
orders → consumer → transient: retry topic → consumer
                  └ permanent: orders.dlt → investigation → controlled replay
```

---

## 1. Retry topics trade ordering for availability

Moving offset 8 aside lets offset 9 proceed, so entity order can change. If order is required, block
the partition with bounded retries or isolate failing keys through another design.

---

## 2. Replay is a production write operation

Replay with a new consumer group or explicit offsets only after checking retention, schema support,
downstream idempotency, rate limits, and expected volume. Record who initiated it and its bounds.

**Success signal:** a deliberately invalid event reaches the DLT with provenance, and replaying it
after correction creates one effect. DLT depth alone silently hides events that lost their source
identity.

> **Key insight**: a dead-letter topic is evidence and a recovery queue, not successful handling.

---

## 3. What breaks, and when not to retry

⚠️ Unbounded immediate retries can pin a partition and overload the dependency already failing.

Do not retry validation errors, authorization denials, or permanent missing resources without a
specific state change that could make the next attempt succeed.

---

**Next**: [Transactional Outbox and CDC](04_transactional_outbox_and_cdc.md)


# Webhook Deep Dive

> Reliable and secure event delivery across independently operated HTTP systems.

[![HTTP](https://img.shields.io/badge/HTTP-Webhooks-005C9C.svg)](https://www.rfc-editor.org/rfc/rfc9110)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)

---

## Contents

| File | Topic | Description |
|------|-------|-------------|
| [01_delivery_model_and_event_contracts.md](01_delivery_model_and_event_contracts.md) | Delivery model | Webhook roles, event envelopes, lifecycle, guarantees, and reconciliation |
| [02_producer_design.md](02_producer_design.md) | Producer | Subscriptions, outbox, delivery state, retry queues, replay, and endpoints |
| [03_consumer_design.md](03_consumer_design.md) | Consumer | Raw-body verification, durable inbox, quick acknowledgement, deduplication |
| [04_signatures_security_and_ssrf.md](04_signatures_security_and_ssrf.md) | Security | HMAC, replay defense, rotation, endpoint ownership, SSRF, and egress isolation |
| [05_retries_idempotency_ordering_and_replay.md](05_retries_idempotency_ordering_and_replay.md) | Reliability | Failure classes, backoff, duplicates, ordering, replay, and reconciliation |
| [06_testing_observability_and_operations.md](06_testing_observability_and_operations.md) | Operations | Fixtures, failure tests, metrics, dashboards, runbooks, and support tooling |

---

## Reading Order

**Working result by entry 2**: accept one raw signed event, reject a modified body, and durably
acknowledge the valid event before asynchronous processing.

1. **Do:** [Consumer Design](03_consumer_design.md) — build the raw-body, durable-inbox intake path.
2. **Harden the boundary:** [Signatures, Security, and SSRF](04_signatures_security_and_ssrf.md) — verify authenticity and replay bounds over the exact bytes.
3. **Understand:** [Delivery Model and Event Contracts](01_delivery_model_and_event_contracts.md) — name what the acknowledgement does and does not prove.
4. **Produce:** [Producer Design](02_producer_design.md) — add subscriptions, outbox delivery, signing, and attempt state.
5. **Recover:** [Retries, Idempotency, Ordering, and Replay](05_retries_idempotency_ordering_and_replay.md), then [Operations](06_testing_observability_and_operations.md).

**Stop here if** you only receive signed events and the inbox boundary meets the product need.
Continue into producer, replay, and operations notes when you own outbound delivery or customer support.

---

## Prerequisites

- [API Fundamentals](../01_api_fundamentals.md)
- [Safe and Scalable API Calls](../../fundamentals/fastapi/safe_and_scalable_api_calls/README.md) for outbound HTTP resilience

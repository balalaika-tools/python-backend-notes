# Kafka Reliability

> Derive guarantees from crash points, then design retries and external effects around them.

---

## Contents

| File | Role | Reader outcome |
|---|---|---|
| [Delivery semantics](01_delivery_semantics.md) | Foundation | Derive at-most- and at-least-once behavior |
| [Idempotence, transactions, exactly once](02_idempotence_transactions_and_exactly_once.md) | Deep dive | Bound each guarantee accurately |
| [Retries, dead letters, replay](03_retries_dead_letters_and_replay.md) | Implementation | Recover poison and transient failures safely |
| [Outbox and CDC](04_transactional_outbox_and_cdc.md) | Implementation | Eliminate a database/Kafka dual-write gap |

---

## Reading Order

**Working result by entry 2**: classify a crash trace and select its deduplication or transaction boundary.

1. **Do:** trace delivery semantics.
2. **Harden:** add idempotency or Kafka transactions where they actually apply.
3. **Recover:** design retry, replay, and outbox paths.

**Stop here if** duplicate effects are prevented and replay is tested. Continue to
[Operations](../operations/README.md) for platform failure and capacity.


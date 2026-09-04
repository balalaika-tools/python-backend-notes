# Use Kafka When a Retained Partitioned Log Is Part of the Requirement

> **Who this is for**: architects choosing among Kafka, queues, databases, and direct integrations.

## Three scenarios produce three different answers

- Many independent consumers must replay an ordered event history: start with Kafka.
- Workers must claim isolated jobs with per-job acknowledgment and priorities: start with a queue.
- One service needs synchronous confirmation from another: start with HTTP or RPC.

---

## 1. The decision turns on the delivery model

| Need | Starting choice |
|---|---|
| Replayable high-throughput event streams | Kafka |
| Per-job routing, priorities, acknowledgments | RabbitMQ, SQS, or another work queue |
| Small durable stream already using Redis | Redis Streams |
| Transactional state, constraints, ad hoc queries | Relational database |
| Immediate request/response | HTTP or gRPC |
| External push across organizations | Webhook |

Kafka earns its operational cost when replay, multiple independent readers, partition ordering, and
sustained throughput matter together. It is not automatically the “scalable” answer to every async
problem.

---

## 2. Count the organizational cost

The design includes schema governance, topic ownership, retention, security, client compatibility,
capacity, on-call, replay safety, and disaster recovery. Managed Kafka reduces broker operations but
does not remove these application responsibilities.

**Success signal:** the architecture decision records required semantics, volume, replay window,
ordering key, failure policy, owners, and the simplest rejected alternative. “Industry standard” is
a silent non-requirement.

> **Key insight**: choose infrastructure by the state and recovery model it makes natural, not by
> peak benchmark or popularity.

---

## 3. What breaks, and when not to use Kafka

⚠️ Using Kafka as a task queue while assuming consumption deletes work produces surprising replay,
retention, and ownership behavior.

Do not use Kafka when one database transaction, a direct call, a webhook, or an existing queue meets
the contract with fewer operational states.

---

**Next**: [Kafka Learning Map](../README.md)


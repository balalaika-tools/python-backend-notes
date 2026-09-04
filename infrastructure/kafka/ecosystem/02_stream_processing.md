# Stream Processing Materializes Continuously Changing Answers

> **Who this is for**: engineers deriving, joining, or aggregating event streams.

## A window changes an unbounded stream into a bounded question

“Count payments” never finishes. “Count accepted payments per merchant in five-minute event-time
windows” defines keys, time boundaries, late-arrival policy, and an output update model.

---

## 1. State appears as soon as output depends on history

Filtering one record is stateless. Counts, joins, deduplication, and sessions require a state store,
partition-compatible keys, changelog/recovery, and retention. Event time uses the event's timestamp;
processing time uses when the application sees it. Late events make those answers diverge.

Kafka Streams is the native Java library; Flink and other engines provide broader distributed
processing models. Python services can consume and produce directly, but should not recreate a
stateful engine casually.

**Success signal:** feed on-time and deliberately late records and observe the documented window
updates after restart. A correct happy-path count silently avoids the hard time semantics.

> **Key insight**: a streaming computation is a maintained state machine whose correctness depends
> on keys, time, recovery, and output semantics—not a loop that happens to run forever.

---

## 2. What breaks, and when not to stream

⚠️ Joining streams partitioned by different keys produces incomplete or expensive results unless
one side is repartitioned deliberately.

Use batch SQL when minutes or hours of latency are acceptable and recomputation is simpler than
continuous state. Use a database view when all inputs already live transactionally in one database.

---

**Next**: [Share Groups and Queue Semantics](03_share_groups_and_queue_semantics.md)


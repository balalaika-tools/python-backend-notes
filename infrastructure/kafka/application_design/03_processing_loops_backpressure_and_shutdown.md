# Safe Consumers Bound Work Before They Commit Progress

> **Who this is for**: engineers turning a demo consumer into a long-running worker.

## The failure: polling outruns processing

A consumer fetches 500 records and launches 500 coroutines against a database pool of 20. Memory
grows, timeouts cascade, polling stalls, and the group reassigns the partition while old work still
runs. The fix is bounded in-flight work plus partition-aware commits.

---

## 1. Backpressure keeps fetched work within downstream capacity

Use a semaphore or bounded queue sized from the actual downstream bottleneck. Pause assigned
partitions when capacity is full and resume them after work completes, while continuing the client
heartbeats required by its protocol.

```text
poll → bounded queue (100) → workers (20) → database
          full: pause partitions       success: mark offset complete
```

Rate limits and concurrency limits solve different problems: a rate limit bounds work per time;
concurrency bounds simultaneous resource occupancy.

---

## 2. Parallel completion cannot commit through a gap

Offsets 10, 11, and 12 run concurrently. If 11 fails while 12 succeeds, committing 13 would skip 11
on restart. Track completed offsets and advance the commit frontier only through the highest
contiguous success—in this case, 11 until offset 11 succeeds.

For simpler correctness, process each partition sequentially and parallelize across partitions.
Add within-partition concurrency only when order is irrelevant and the commit-frontier complexity
is justified.

---

## 3. Shutdown is a protocol, not a signal handler

On termination: stop accepting new work, keep group membership alive if possible, finish within a
deadline, commit only contiguous successes, then close the consumer. If the deadline expires,
abandon unfinished work and rely on idempotent replay.

**Success signal:** terminate the worker during a controlled slow event; after restart, every
unfinished event reappears and no completed effect is missing. Low lag alone cannot prove this.

> **Key insight**: consumer concurrency is safe only when ownership, completion, and committed
> progress remain aligned at partition granularity.

---

## 4. What breaks, and when not to parallelize

⚠️ Committing the largest completed offset silently skips earlier unfinished records. The symptom is
a business gap with a healthy committed lag metric.

Do not parallelize within a partition when processing order is part of the invariant. Increase
partitions with a correct key or optimize the handler before weakening ordering.

---

**Next**: [Topic and Partition Design](04_topic_and_partition_design.md)


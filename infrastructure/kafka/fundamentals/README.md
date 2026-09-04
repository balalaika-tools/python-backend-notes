# Kafka Fundamentals

> Follow one event from a producer call to durable storage and a consumer-group offset.

---

## Contents

| File | Role | Topic | Reader outcome |
|---|---|---|---|
| [First event round trip](01_first_event_round_trip.md) | Implementation | Local KRaft cluster | Produce, inspect, and consume one event |
| [Logs, topics, partitions, and offsets](02_log_topics_partitions_and_offsets.md) | Foundation | Storage model | Trace where a record lives and why reading does not delete it |
| [Partitioning, keys, and ordering](03_partitioning_keys_and_ordering.md) | Deep dive | Routing | Choose a key and state the resulting ordering boundary |
| [Consumer groups and rebalancing](04_consumer_groups_offsets_and_rebalancing.md) | Deep dive | Parallel consumption | Predict assignment, lag, replay, and rebalance behavior |
| [Replication, leaders, and KRaft](05_replication_leaders_and_kraft.md) | Deep dive | Cluster failure | Explain which failures remain available and durable |

---

## Reading Order

**Working result by entry 2**: a consumed `order.created` event whose partition and offset the
reader can explain.

1. **Do:** run the first round trip.
2. **Understand:** replay it through the retained-log mental model.
3. **Harden the model:** add ordering, group coordination, and replication.

**Stop here if** you only need to evaluate Kafka or discuss a design. Continue to
[Application design](../application_design/README.md) to write a service.

---

## Prerequisites

- Docker and a shell for the runnable quick start.
- No prior Kafka knowledge.


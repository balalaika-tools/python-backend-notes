# Replication Separates an Acknowledged Write from a Durable Write

> **Who this is for**: engineers deciding which broker failures Kafka should survive.

## One acknowledged record, two outcomes

A partition leader accepts offset 51. With replication factor one, its disk failure loses the only
copy. With three replicas, `acks=all`, and `min.insync.replicas=2`, the write succeeds only after the
required in-sync replicas have it.

---

## 1. Leaders serialize writes while followers copy the log

Each partition has one leader handling reads and writes and zero or more follower replicas. An
**in-sync replica (ISR)** is a replica sufficiently caught up to remain eligible for safe leadership.
Replication factor describes desired copies; ISR describes currently healthy copies.

```text
producer → broker 1: P2 leader, offset 51
                 ├→ broker 2: P2 follower (ISR)
                 └→ broker 3: P2 follower (ISR)
```

If broker 1 fails, the controller chooses an eligible follower as leader. Availability during that
election is brief; durability depends on what was replicated before acknowledgment.

---

## 2. Three settings form one durability contract

`replication.factor=3` creates three copies. `min.insync.replicas=2` defines how many must remain
eligible for an `acks=all` write. `acks=all` makes the producer wait for that rule. Configuring only
one of the three does not express the full contract.

When ISR falls below two, writes fail rather than pretend to be durable. That is a deliberate
availability-for-consistency trade.

---

## 3. KRaft protects cluster metadata, not event payloads

**KRaft** is Kafka's Raft-based metadata quorum. Controllers agree on topics, partition leadership,
and cluster configuration; brokers store partition data. Kafka 4.x does not use ZooKeeper; Kafka
4.0 was the [first ZooKeeper-free major release](https://kafka.apache.org/blog/2025/03/18/apache-kafka-4.0.0-release-announcement/).

Losing controller quorum prevents metadata changes and leader elections even if broker disks still
contain data. Losing partition replicas threatens event data even if the controllers are healthy.
Monitor these planes separately.

> **The near-miss**: a controller is not a database replica for topic contents. It coordinates
> metadata; partition replicas carry the events.

---

## 4. Success and failure signals

**Success signal:** topic description shows the intended replication factor and ISR count, and a
controlled broker stop elects a new leader while acknowledged records remain readable. A green
broker process count alone is a silent failure because partitions can be under-replicated.

⚠️ Enabling unclean leader election can restore availability by electing a stale replica, losing
acknowledged records. Treat it as an explicit data-loss policy, not a generic recovery switch.

> **Key insight**: durability is an end-to-end acknowledgment policy across producer settings,
> replica health, and broker admission—not a property implied by “Kafka is replicated.”

---

## 5. When not to self-manage this layer

Do not self-host Kafka solely to avoid a service fee when the team cannot staff quorum, disk,
upgrade, security, and restore operations. A managed service can move those mechanics to a provider;
it does not remove application-level key, schema, offset, or idempotency decisions.

---

**Next**: [Application Design](../application_design/README.md)

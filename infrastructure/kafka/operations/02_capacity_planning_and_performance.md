# Capacity Starts with Bytes, Retention, and the Slowest Consumer

> **Who this is for**: engineers sizing topics and diagnosing throughput ceilings.

## Build a rough envelope before tuning knobs

For ingress `20 MB/s`, retention `7 days`, replication factor `3`, raw replicated storage is about
`20 × 604800 × 3 ≈ 36 TB`, before indexes, headroom, and compaction behavior. Network also includes
replication and consumer egress.

---

## 1. Partitions are parallel capacity with fixed overhead

Measure producer bytes/sec per partition and consumer processing rate, then choose enough partitions
for peak load plus failure headroom. Batch size, linger, and compression trade latency and CPU for
fewer requests and better sequential I/O.

Capacity must cover a broker outage: a cluster that works only when every broker is healthy has no
failure budget.

**Success signal:** a load test at expected record sizes sustains peak ingress while lag returns to
zero after the burst and one-broker-loss capacity remains acceptable. Tiny synthetic records can
silently produce a meaningless result.

> **Key insight**: Kafka performance is a pipeline budget across producer batching, partition
> leaders, replicas, disks, networks, and consumers; the tightest stage sets throughput.

---

## 2. What breaks, and when not to add partitions

⚠️ Disk nearly full makes recovery and rebalancing slower precisely when extra space is required.

Do not add partitions to fix a slow handler or hot key without measuring placement and downstream
capacity. More shards cannot parallelize one dominant key.

---

**Next**: [Observability and Incident Response](03_observability_and_incident_response.md)


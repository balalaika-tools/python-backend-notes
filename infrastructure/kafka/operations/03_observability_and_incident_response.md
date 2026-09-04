# Kafka Incidents Need Broker and Business Signals Together

> **Who this is for**: teams defining dashboards, alerts, and first-response checks.

## Lag alone cannot identify the bottleneck

Rising lag may mean slow handlers, partition skew, rebalances, broker latency, or a failed downstream
database. Correlate consumer lag and record age with processing latency, error rate, assignment
changes, broker request latency, ISR shrinkage, controller health, and disk utilization.

---

## 1. Triage from consequence toward cause

```text
business freshness breached?
  → which group/topic/partition?
  → arrival spike or processing slowdown?
  → rebalance churn or dependency errors?
  → broker latency, ISR, disk, controller quorum?
```

Alert on sustained user-impacting conditions, not every transient metric movement. Preserve client
IDs, group IDs, topic, partition, offset, and event ID in structured diagnostics without logging
credentials or sensitive payloads.

**Success signal:** an injected slow handler produces an alert that identifies the group and hot
partition, and the runbook distinguishes scaling from replay or broker repair. A green cluster
dashboard silently misses stopped consumers.

> **Key insight**: Kafka health is the ability of a named event flow to stay fresh and recover, not
the mere availability of broker processes.

---

## 2. What breaks, and when not to page

⚠️ Topic-wide average lag hides one stuck partition behind many idle partitions.

Do not page on a momentary rebalance or small lag without a breached duration or freshness objective.
Use tickets or dashboards for capacity trends; reserve pages for actionable urgency.

---

**Next**: [Deployment, Upgrades, and Disaster Recovery](04_deployment_upgrades_and_disaster_recovery.md)


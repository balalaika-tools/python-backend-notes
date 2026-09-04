# Recovery Requires a Tested Ownership and Data-Loss Contract

> **Who this is for**: teams choosing managed Kafka or owning cluster lifecycle.

## Decide recovery objectives before choosing topology

State the recovery-time objective (RTO), recovery-point objective (RPO), regional failure model,
and who can declare failover. Replication inside one cluster does not provide independent regional
recovery.

---

## 1. Managed service changes responsibility, not semantics

A provider may own broker replacement, patching, and control-plane durability. Your team still owns
topics, keys, schemas, ACLs, quotas, client compatibility, lag, replay, and downstream idempotency.

Kafka 4.x uses KRaft; ZooKeeper belongs only in migration plans for legacy 3.x clusters. Rolling
upgrades require checking supported version paths, protocol compatibility, client versions, and
feature gates against the exact release notes.

---

## 2. Cross-cluster replication is not automatic failover correctness

MirrorMaker or provider replication copies records asynchronously. Consumer offsets, topic configs,
ACLs, schemas, and external effects need explicit recovery treatment. Failback can duplicate or
reorder business processing.

**Success signal:** a game day loses a broker or region, restores the declared event flows within
RTO, measures actual RPO, and proves idempotent resume. A replicated topic count alone is insufficient.

> **Key insight**: disaster recovery is a coordinated application-state transition; copied Kafka
> records are only one input to it.

---

## 3. What breaks, and when not to self-host

⚠️ An untested restore often discovers missing schemas, ACLs, offsets, or credentials after the data
has already been copied.

Do not self-host when no team owns 24/7 storage, quorum, upgrade, certificate, and restore duties.

---

**Next**: [Ecosystem and Decisions](../ecosystem/README.md)

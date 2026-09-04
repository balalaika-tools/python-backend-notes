# Kafka Security Must Constrain Both Connection and Action

> **Who this is for**: engineers moving beyond a plaintext local broker.

## An authenticated producer can still be over-privileged

TLS encrypts traffic; SASL or mutual TLS authenticates a service identity; access-control lists
(ACLs) authorize that identity to named cluster resources. Missing any layer leaves a different gap.

---

## 1. Start from one service identity

Give `orders-api` write access to `orders.events.v1`, and `billing-worker` read access plus its own
consumer group. Do not share credentials across applications: attribution and revocation disappear.
Keep secrets outside source, images, logs, and event payloads; rotate them with overlapping validity.

An attacker who can create topics or alter configs can redirect or disrupt data even without broker
shell access. Admin APIs and Kafka Connect's plugin/REST surfaces require tighter trust boundaries.

**Success signal:** the intended write/read succeeds while a test write to an unrelated topic and
read using another group's ID are denied. A successful TLS handshake alone silently proves no
authorization.

> **Key insight**: Kafka security is the intersection of authenticated identity, resource action,
> network path, and data classification—not a single “secure protocol” setting.

---

## 2. What breaks, and when not to share a cluster

⚠️ Wildcard ACLs turn one compromised client into a cluster-wide producer or consumer.

Do not rely on ACLs alone for tenants requiring hard resource, encryption-key, or failure-domain
isolation. Use separate clusters or a managed-service isolation boundary.

---

**Next**: [Capacity Planning and Performance](02_capacity_planning_and_performance.md)


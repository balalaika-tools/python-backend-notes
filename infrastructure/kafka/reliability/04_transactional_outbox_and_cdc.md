# An Outbox Turns Two Writes into One Recoverable Handoff

> **Who this is for**: services that update a database and publish a corresponding event.

## The dual-write gap

`COMMIT order` followed by `publish order.created` can crash between calls, leaving durable business
state with no event. Reversing the calls creates an event for a database change that may roll back.

---

## 1. Store business state and intent in one database transaction

```text
BEGIN → insert orders row → insert outbox(event_id, payload, unpublished) → COMMIT
                                      ↓
                         relay/CDC publishes to Kafka
```

The relay may publish twice around its own crash, so consumers still deduplicate by `event_id`.
**Change data capture (CDC)** reads database-log changes; a polling relay claims outbox rows directly.

---

## 2. Ownership decides between polling and CDC

Polling is simple and application-owned but adds query load and cleanup. CDC scales integration and
captures ordered database changes but introduces connector, log-retention, and schema-operational
dependencies.

**Success signal:** crash after database commit and before publish; the relay later emits the event.
Then crash after publish and verify a duplicate causes one downstream effect.

> **Key insight**: the outbox does not make database and Kafka atomic; it records a durable promise
> inside the database so publication can be retried until observed.

---

## 3. What breaks, and when not to use an outbox

⚠️ Deleting outbox rows before confirmed publication turns relay failure into permanent event loss.

Do not add an outbox when Kafka is already the authoritative input and all outputs remain inside one
Kafka transaction. Use the smaller atomic boundary.

---

**Next**: [Operations](../operations/README.md)


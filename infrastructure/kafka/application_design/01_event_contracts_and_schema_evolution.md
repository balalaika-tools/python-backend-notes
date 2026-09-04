# Event Contracts Must Outlive Any One Deployment

> **Who this is for**: engineers designing payloads shared by independently deployed services.

## A minimal event with identity and meaning

```json
{
  "event_id": "evt-101",
  "event_type": "order.created",
  "schema_version": 1,
  "occurred_at": "2026-09-04T09:15:00Z",
  "producer": "orders-api",
  "data": {"order_id": "ord-42", "currency": "EUR", "total_minor": 2590}
}
```

Validate this envelope at the producer boundary and again at the consumer boundary. `event_id`
supports deduplication, `event_type` selects behavior, and `schema_version` makes interpretation
explicit. Money uses minor units so binary floating point cannot change the amount.

---

## 1. Independent deployment makes payload changes distributed changes

An in-process function signature changes atomically with its caller. An event may remain retained
while producers and consumers deploy days apart. Removing `currency` can therefore break replay
long after the producer that wrote the record has gone.

Prefer additive evolution: add optional fields with meaningful defaults, let consumers ignore
unknown fields, and keep the semantic meaning of existing fields stable.

---

## 2. Compatibility is about readers and writers

- **Backward compatibility**: the new reader accepts old data.
- **Forward compatibility**: the old reader accepts new data.
- **Full compatibility**: both directions hold across the supported window.

Changing `total_minor` from integer cents to a decimal major-unit string is not compatible merely
because JSON can represent both. The wire shape and business meaning changed.

Use JSON Schema, Avro, or Protobuf plus a schema registry when automated compatibility enforcement
is worth the platform cost. The registry checks structure; contract tests must still check meaning.

---

## 3. Events describe facts, not remote commands in disguise

`order.created` states a completed domain fact and can serve many consumers. `send-this-email-now`
targets one worker and behaves more like a command. Mixing the two makes ownership, retries, and
audit meaning unclear.

> **Key insight**: an event contract includes semantics and compatibility promises, not just a
> serializable payload.

---

## 4. What breaks, how to verify, and when not to evolve in place

**Success signal:** compatibility tests read representative retained v1 records with the v2
consumer and exercise v2 records against the oldest supported reader. Checking only schema-registry
acceptance silently misses changed business meaning.

⚠️ Reusing `event_type` while changing its meaning corrupts consumers without a parse error. Publish
a new event type or topic when the fact itself changes.

Do not put large blobs, secrets, or mutable database snapshots into every event. Store blobs in
object storage, publish a stable reference, and minimize personal data whose retention you cannot
later revoke cleanly.

---

**Next**: [Python Producers and Consumers](02_python_producers_and_consumers.md)


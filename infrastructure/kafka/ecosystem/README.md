# Kafka Ecosystem and Decisions

> Add connectors, processing, or queue semantics only when the baseline log model is insufficient.

---

## Contents

| File | Role | Reader outcome |
|---|---|---|
| [Kafka Connect](01_kafka_connect_and_data_integration.md) | Decision guide | Choose connectors or application code |
| [Stream processing](02_stream_processing.md) | Foundation | Choose stateless, stateful, windowed, or external processing |
| [Share groups](03_share_groups_and_queue_semantics.md) | Deep dive | Evaluate queue-like per-record delivery |
| [When to use Kafka](04_when_to_use_kafka.md) | Decision guide | Select Kafka or a simpler alternative |

**Working result by entry 2**: classify an integration and a transformation, then choose whether
Connect or stream processing owns it. **Stop here if** ordinary producers and consumers suffice.


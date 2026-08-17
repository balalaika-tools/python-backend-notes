# infrastructure/README.md (25 lines)
ORDERING: n/a — directory index with no teaching sequence.
EXPLANATION: n/a — directory index with no central mechanism to restate.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index is concise, accurately scopes both infrastructure collections, and sends prerequisite learning to its canonical owners.

# infrastructure/observability/README.md (26 lines)
ORDERING: n/a — directory index with no teaching sequence.
EXPLANATION: n/a — directory index with no central mechanism to restate.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index gives every observability note a distinct role and keeps prerequisites out of the teaching files themselves.

# infrastructure/observability/01_opentelemetry_primer.md (149 lines)
ORDERING: payoff absent/149 (n/a, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:15 (PASS; 0 markers/15 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 4 high, 0 med, 1 low

FIX-HIGH: The note has no `## The short version` — add the bounded inputs, a concrete request trace with named values and an observable backend result, an exact success signal, and linked deferrals before section 1.
FIX-HIGH: `span` first appears in the signals table at line 23 without saying what kind of object it is — gloss it there as one timed operation within a trace.
FIX-HIGH: The primer never shows the first real failure — add the symptom produced by a missing `service.name` or unreachable exporter and how the reader distinguishes that from an uninstrumented request.
FIX-HIGH: The note argues for OTel over vendor SDKs but never states when not to add it — add the boundary for a small service whose existing vendor instrumentation already meets its portability and correlation needs.
FIX-LOW: Lines 13 and 149 each declare a `> **Key insight**:` — retain one transferable insight and demote the other to ordinary summary prose.

# infrastructure/observability/02_python_sdk.md (364 lines)
ORDERING: payoff line 215/364 (0.591, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:14 (PASS; 0 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 6; unexplained rules/defenses 1; intuition-building explanation yes.
Summary: 1 critical, 4 high, 0 med, 0 low

FIX-CRITICAL: The production-oriented exporter examples at lines 63–65, 135–136, and 243–255 hard-code `insecure=True` — make TLS the default for any non-loopback endpoint and confine plaintext to an explicit local-development branch.
FIX-HIGH: The note has no `## The short version` — add a 10–25-line minimal FastAPI trace, counted inputs, exact exported-span success signal, and linked deferrals before installation.
FIX-HIGH: The first composed app does not begin until line 215 and contains no route invocation or backend observation — provide an early `/hello` request that yields a named server span and state exactly where the reader sees it.
FIX-HIGH: Gloss `OTLP`, `TracerProvider`, `BatchSpanProcessor`, `MeterProvider`, `semantic conventions`, and `semconv` at their first prose uses; the code currently introduces provider and protocol vocabulary before a local model.
FIX-HIGH: The rule “Always define a `Resource`” at line 31 precedes its causal explanation — first show how omitted identity becomes `unknown_service`, then state the rule and the verification query.

# infrastructure/observability/03_metrics_export_methods.md (428 lines)
ORDERING: payoff line 44/428 (0.103, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:16 (PASS; 0 markers/16 explanatory paragraphs); restatement PASS; unglossed first uses 5; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 3 high, 0 med, 1 low

FIX-CRITICAL: The three trace-export examples at lines 71–73, 227–233, and 320–322 use `insecure=True` in copyable application configurations — default to verified TLS outside an explicitly labeled loopback/dev setup.
FIX-HIGH: The note has no `## The short version` — add the default ownership choice, counted inputs, one runnable method, its exact scrape/export observation, and linked deferrals before the comparison.
FIX-HIGH: None of the three runnable methods gives a worked success signal or the most common silent failure — add the expected `/metrics` sample or Collector-received metric and distinguish an unscripted target, failed OTLP export, and duplicate series.
FIX-HIGH: Gloss `OTLP`, `remote_write`, `PrometheusMetricReader`, resource attributes, and `BYOC` at first use so a reader can compare ownership models without importing vocabulary from another note.
FIX-LOW: Add exactly one `> **Key insight**:` capturing the transferable decision: choose the in-app metric API independently from the transport and backend routing.

# infrastructure/observability/04_collector_config.md (508 lines)
ORDERING: payoff line 284/508 (0.559, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 0:23 (PASS; 0 markers/23 explanatory paragraphs); restatement PASS; unglossed first uses 6; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 3 high, 1 med, 1 low

FIX-CRITICAL: The shell example at line 501 uses `abc123` as an API key value — replace it with an unmistakable non-secret placeholder such as `${GROUNDCOVER_API_KEY:?set-a-test-key}` and keep the example from teaching credential-shaped literals.
FIX-HIGH: The note has no `## The short version` — put a minimal OTLP receiver → batch processor → debug exporter pipeline with counted inputs, a visible test span, and linked production deferrals before the component catalogue.
FIX-HIGH: The first composed pipeline is buried at line 284 after six component sections — move the minimal pipeline to the entry block and preserve the full multi-signal production config as later hardening.
FIX-HIGH: Gloss `OTLP`, `gRPC`, `protobuf`, `OOM`, `OTTL`, and `semconv` at first use; several correctness-sensitive processor choices currently depend on unexplained abbreviations.
FIX-MED: The file is 508 lines with no `<!-- length-justification: ... -->` — either justify why config anatomy and deployment topology must remain together or split deployment manifests into a named operations note.
FIX-LOW: Lines 397, 432, and 503 pin Collector `0.150.0`, while the latest released build is `0.158.0`; refresh the checked-date comment or explain the tested pin rather than calling it current (official release: https://github.com/open-telemetry/opentelemetry-collector-releases/releases/tag/v0.158.0, checked 2026-08-17).

# infrastructure/redis/README.md (64 lines)
ORDERING: n/a — directory index and route selector with no per-note teaching sequence.
EXPLANATION: n/a — directory index with no central mechanism to restate.
Summary: 0 critical, 0 high, 0 med, 1 low

FIX-LOW: The redis-py badge at line 6 says `5.x`, while the collection's client note covers 5.x through 8.x and the official client supports current Redis releases from redis-py 6+ — make the badge describe the tested range instead of an obsolete single major (https://github.com/redis/redis-py, checked 2026-08-17).

# infrastructure/redis/01_data_structures.md (778 lines)
ORDERING: payoff line 30/778 (0.039, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 0:20 (PASS; 0 markers/20 explanatory paragraphs); restatement PASS; unglossed first uses 4; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 2 critical, 3 high, 1 med, 2 low

FIX-CRITICAL: The lock example at lines 85–92 releases with a bare `DEL`; use a unique owner token and atomic compare-and-delete so an expired holder cannot delete a successor's lock (official safe-release pattern: https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/, checked 2026-08-17).
FIX-CRITICAL: Lines 589–597 say a consumer-group message has “no duplicate processing” and is delivered exactly once — state at-least-once delivery, show the crash-after-side-effect-before-`XACK` replay, and require an idempotent handler (official Streams behavior: https://redis.io/docs/latest/develop/data-types/streams/, checked 2026-08-17).
FIX-HIGH: The note has no `## The short version` — add a counted Redis connection plus one structure-selection example, exact `PING`/readback signals, and linked deferrals before the catalogue.
FIX-HIGH: The command tables for strings, lists, sets, sorted sets, and streams each exceed five entries without a marked default subset — mark the small starter set and exercise those commands in the first example for each type.
FIX-HIGH: Expand and gloss `TTL`, `FIFO`, `LIFO`, and `ziplist` at first use; acronym and storage-encoding vocabulary currently appears before its operational meaning.
FIX-MED: The file is 778 lines with no length justification — split the six-type tutorial from the command lookup at “Quick Reference,” or record why one file is required.
FIX-LOW: Line 193 calls the compact hash encoding a `ziplist`; Redis 7+ uses listpack configuration (`hash-max-listpack-*`) — update the term and retain the size-threshold caveat (https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/memory-optimization/, checked 2026-08-17).
FIX-LOW: Add exactly one `> **Key insight**:` that transfers beyond the examples: choose a Redis structure by the atomic operation the application needs, not by superficial resemblance to a Python container.

# infrastructure/redis/02_pubsub_and_streams.md (904 lines)
ORDERING: payoff line 87/904 (0.096, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 0:14 (PASS; 0 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 6; unexplained rules/defenses 1; intuition-building explanation yes.
Summary: 2 critical, 4 high, 1 med, 1 low

FIX-CRITICAL: The “production-ready” processor at lines 534–564 reads failures back with `XRANGE`, which does not increment the delivery counter, so poison messages can retry forever and never reach the dead-letter branch; retry through `XREADGROUP` history or claim operations, and test the transition to a DLQ after the stated maximum (delivery-counter behavior: https://redis.io/docs/latest/develop/data-types/streams/, checked 2026-08-17).
FIX-CRITICAL: Lines 264–281 and 306–310 repeatedly say each message is delivered exactly once within a group — replace this with at-least-once semantics and show why handlers must be idempotent when a worker crashes after its side effect but before `XACK` (https://redis.io/docs/latest/develop/use-cases/streaming/, checked 2026-08-17).
FIX-HIGH: The note has no `## The short version` — add the Pub/Sub-versus-Streams decision, counted inputs, one minimal working pair, exact observed output, and linked durability/recovery deferrals.
FIX-HIGH: The sync baseline at lines 54–83 publishes before starting its subscriber, so it prints zero subscribers and then waits forever — start the subscriber and confirm its subscription before publishing, and show the expected receive line.
FIX-HIGH: The combined FastAPI example calls `XADD` “durable — guaranteed processing” at line 801 but neither configures Redis persistence nor reclaims stale pending messages — narrow the claim and link the exact persistence, idempotency, and recovery requirements.
FIX-HIGH: Gloss `PEL`, `KRaft`, `ISR`, `KSQL`, `CDC`, and dead-letter queue at first use instead of requiring Kafka and Streams vocabulary to interpret the comparisons.
FIX-MED: The file is 904 lines with no length justification — split the canonical consumer/recovery implementation from the Pub/Sub-versus-Streams decision tutorial while preserving a linked baseline.
FIX-LOW: Add exactly one `> **Key insight**:` capturing that durability changes both storage and consumer responsibility: retained messages still require acknowledgment, recovery, and idempotency.

# infrastructure/redis/03_caching_patterns.md (708 lines)
ORDERING: payoff line 34/708 (0.048, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 0:27 (PASS; 0 markers/27 explanatory paragraphs); restatement PASS; unglossed first uses 3; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 3 critical, 3 high, 1 med, 1 low

FIX-CRITICAL: Lines 113–146 promise that the two-step DB/cache write-through example is “always fresh” with “No stale reads”; show partial-failure and concurrent-writer races, then use a version/transaction/outbox design or narrow the guarantee.
FIX-CRITICAL: Lines 569–583 label delete-on-write “safe,” but a reader can miss, read the old DB value, lose a race to the writer's update-and-delete, and then repopulate stale data; add that interleaving and a delayed second delete, version check, or bounded-staleness contract.
FIX-CRITICAL: The stampede lock at lines 431–442 uses a constant token and bare `DEL`; release only when a unique ownership token still matches so an expired holder cannot delete the replacement lock (https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/, checked 2026-08-17).
FIX-HIGH: The note has no `## The short version` — add a minimal cache-aside read with counted inputs, exact hit/miss observations, and linked stampede/invalidation deferrals.
FIX-HIGH: The actionable examples never give a reproducible success signal or common silent-failure tell — show DB-call counts and returned versions for miss, hit, invalidation, and stale-fill races.
FIX-HIGH: Expand and gloss `TTL`, `XFetch`, and `CDC` at first use; the later strategy choices depend on these terms before they are grounded.
FIX-MED: The file is 708 lines with no length justification — split baseline caching and invalidation from advanced refresh/stampede techniques at a named production boundary.
FIX-LOW: Add exactly one `> **Key insight**:` stating that cache correctness is a version-ordering problem, not merely choosing an expiration duration.

# infrastructure/redis/04_python_clients.md (513 lines)
ORDERING: payoff line 30/513 (0.058, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 0:17 (PASS; 0 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 5; unexplained rules/defenses 1; intuition-building explanation yes.
Summary: 1 critical, 4 high, 2 med, 1 low

FIX-CRITICAL: Copyable connection examples at lines 45, 48, and 503 embed `password="secret"` — load credentials from an environment/secret provider and use an unmistakable placeholder in every example.
FIX-HIGH: The note has no `## The short version` — add a counted, pooled client setup with `PING`/set/get observations and linked TLS, retry, and shutdown deferrals before the ecosystem survey.
FIX-HIGH: Lines 226–233 and the comparison row at 281 claim MULTI/EXEC is all-or-nothing even though lines 283 and 288 correctly explain that runtime command errors do not roll back — replace the rollback language with “queued commands execute without interleaving” and show the runtime-error result array.
FIX-HIGH: The “production-ready” quick reference at lines 494–512 names built-in `ConnectionError` and `TimeoutError`, not `redis.ConnectionError` and `redis.TimeoutError`, and therefore does not apply the intended redis-py retry classes — import and use the Redis exceptions explicitly.
FIX-HIGH: Expand and gloss `RESP`, `TLS`, `AUTH`, `MULTI/EXEC`, and `WATCH` at first use so protocol and transaction decisions do not arrive as unexplained command names.
FIX-MED: Line 22 says RESP3 changes Python reply types by default in redis-py 8, but the current client defaults to RESP3 on the wire while preserving legacy RESP2-compatible response shapes unless compatibility is opted out — update the migration advice around `legacy_responses=False` rather than predicting protocol-driven parser breaks (https://github.com/redis/redis-py, checked 2026-08-17).
FIX-MED: The file is 513 lines with no length justification — justify the combined client/reference role or split serialization and error/retry reference material after the FastAPI baseline.
FIX-LOW: Add exactly one `> **Key insight**:` that distinguishes one logical client from the bounded pool of physical connections it manages.

# infrastructure/redis/05_rate_limiting.md (535 lines)
ORDERING: payoff line 11/535 (0.021, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 21:31 (PASS; 21 markers/31 explanatory paragraphs); restatement PASS; unglossed first uses 4; unexplained rules/defenses 1; intuition-building explanation yes.
Summary: 1 critical, 5 high, 1 med, 1 low

FIX-CRITICAL: The non-atomic sliding-counter implementation at lines 194–214 is called the production default at lines 217–232, but concurrent callers can all observe the same below-limit count and then increment past the cap — present the Lua check-and-increment as the copyable default and label the split version explanatory only.
FIX-HIGH: The note has no `## The short version` — add one bounded limiter, exact allowed/denied observations, counted inputs, and links to clock, cluster, and failure hardening before algorithm 1.
FIX-HIGH: The `EVALSHA` wrappers at lines 269–290 and 369–381 have no `NOSCRIPT` recovery after restart/failover — catch the missing-script response, reload once, and retry safely.
FIX-HIGH: The two-key sliding Lua call at lines 281–289 will fail with `CROSSSLOT` in Redis Cluster — use one shared hash tag in both keys in the implementation, not only in the later general warning.
FIX-HIGH: The multi-dimensional script at lines 477–491 increments global and user counters before later checks can reject, but never states whether rejected attempts consume those quotas — define attempted-versus-admitted semantics and roll back earlier increments when the contract is admitted requests.
FIX-HIGH: Expand `RPM`, `TPM`, `TOCTOU`, and `Lua` at first use; these are central inputs and mechanisms, not optional reference vocabulary.
FIX-MED: The file is 535 lines with no length justification — split the algorithm tutorial from cluster/retry/admission-controller hardening after the atomic single-dimension baseline.
FIX-LOW: Replace the “The Core Insight” heading with the required single `> **Key insight**:` marker and phrase it as the transferable mapping from a policy dimension to atomic Redis state.

# infrastructure/redis/06_ha_and_persistence.md (332 lines)
ORDERING: payoff absent/332 (n/a, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:27 (PASS; 0 markers/27 explanatory paragraphs); restatement PASS; unglossed first uses 5; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 3 high, 0 med, 1 low

FIX-CRITICAL: Line 64 says zero data loss requires `appendfsync always` plus replication, but Redis replication is asynchronous and acknowledged writes can still be lost during failover; state that these settings reduce different loss windows but do not provide a zero-loss guarantee (https://redis.io/docs/latest/operate/oss_and_stack/management/replication/ and https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/, checked 2026-08-17).
FIX-HIGH: The note has no `## The short version` — add a counted topology/persistence decision with one observable restart or failover outcome and linked scale/lock deferrals before the persistence catalogue.
FIX-HIGH: No configuration is exercised end to end — add exact `INFO persistence`/replication observations for a successful write, restart, and replica promotion plus the tell for lag or an unhealthy persistence rewrite.
FIX-HIGH: Expand and gloss `HA`, `RDB`, `OOM`, `CRC16`, and `AP`/`CP` at first use; the note currently asks a first-time Redis operator to reason about guarantees through unexplained abbreviations.
FIX-LOW: Add exactly one `> **Key insight**:` that distinguishes persistence, availability, and sharding as independent guarantees rather than one “production Redis” switch.

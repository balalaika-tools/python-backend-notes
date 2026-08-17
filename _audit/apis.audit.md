# apis/01_api_fundamentals.md (208 lines)
ORDERING: payoff line 120/208 (0.577, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:13 (PASS; 2 markers/13 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The first concrete contract trace is buried at line 120 (57.7%) and there is no `## The short version` — open with the problem/mental model, a counted input list, a named request/commit/timeout trace, its exact observed outcome, and linked deferrals for authorization, retries, compatibility, and operations.

# apis/02_api_styles_and_selection.md (156 lines)
ORDERING: payoff line 108/156 (0.692, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 13:4 (FAIL; 13 markers/4 explanatory paragraphs); restatement PASS; unglossed first uses 5; unexplained rules/defenses 12; intuition-building explanation yes.
Summary: 0 critical, 6 high, 0 med, 1 low

FIX-HIGH: The first composed selection example is buried at line 108 (69.2%) and there is no `## The short version` — open with one bounded set of requirements, the selected style, the observable architecture decision, a counted input list, and linked deferrals for the deeper trade-offs.
FIX-HIGH: Expand and gloss `WSDL` and `WS-*` at line 14 before using them as SOAP selection criteria.
FIX-HIGH: Gloss Protocol Buffers at line 16 as gRPC's usual schema and binary message format rather than leaving `Protobuf` as assumed vocabulary.
FIX-HIGH: Expand Server-Sent Events (`SSE`) at line 34 and state that it is a one-way HTTP event stream before comparing it with polling.
FIX-HIGH: Explain the `N+1` access pattern at line 58 as one parent lookup followed by one lookup per result before treating it as a GraphQL cost.
FIX-HIGH: The twelve `✅`/`⚠️` conclusions at lines 44–76 have no causal prose in their own subsections — precede each style pair with the concrete requirement it satisfies and the operational failure or cost that earns the warning.
FIX-LOW: Add one transferable `> **Key insight**:` stating that interaction shape and ownership boundary, not payload syntax, determine the API style.

# apis/03_api_contracts_and_lifecycle.md (201 lines)
ORDERING: payoff line 101/201 (0.502, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 1:16 (PASS; 1 markers/16 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: The first concrete compatibility migration is buried at line 101 (50.2%) and there is no `## The short version` — open with the `customer_name` to `display_name` expand/migrate/contract trace, a counted list of contract inputs, the visible old/new-consumer success signal, and linked hardening deferrals.
FIX-HIGH: Gloss AsyncAPI at line 33 as a machine-readable contract format for asynchronous channels and messages; a product name alone does not tell a first-time reader what artifact it produces.
FIX-LOW: Add one transferable `> **Key insight**:` explaining that compatibility is an overlap property of independently deployed producers and consumers, not merely a schema-diff result.

# apis/04_soap_overview.md (134 lines)
ORDERING: payoff line 79/134 (0.590, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:10 (PASS; 0 markers/10 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: The first request with a visible SOAP outcome is the fault at line 79 (59.0%) and there is no `## The short version` — open with a counted set of WSDL/client inputs, one request/fault exchange, the exact observed fault, and links to version, security, timeout, and XML-hardening sections.
FIX-HIGH: Expand and gloss `WSDL` and `WS-*` at their first prose use on line 3; their definitions at lines 62 and 99 arrive after readers have already been asked to evaluate them.
FIX-MED: Section 1 opens with a dictionary definition of SOAP at line 9 — start with the interoperability problem of consuming a provider-owned formal XML contract, then attach the envelope mental model.
FIX-LOW: Add one transferable `> **Key insight**:` distinguishing SOAP's message-processing contract from merely sending XML over HTTP.

# apis/05_graphql_overview.md (169 lines)
ORDERING: payoff line 11/169 (0.065, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:13 (PASS; 0 markers/13 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: The query/response payoff appears early, but `## The short version` is absent — wrap that exchange with the problem/mental model, a counted list of schema/query inputs, an exact success signal, and linked deferrals for authorization, cost control, N+1 loading, and evolution.
FIX-HIGH: Gloss schema introspection at line 56 before presenting it as a tooling strength and security-policy choice; state that clients can query the schema's types and fields.
FIX-MED: Section 1 opens with a definition at line 9 — lead with the client problem of needing different connected projections, then introduce the typed field-selection mechanism.
FIX-LOW: Add one transferable `> **Key insight**:` explaining that GraphQL moves response-shape choice to the consumer while leaving data-access cost and authorization with the server.
NO-ACTION: The September 2025 specification citation is still the latest release as checked 2026-08-17: https://spec.graphql.org/.

# apis/06_grpc_overview.md (168 lines)
ORDERING: payoff line 77/168 (0.458, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:12 (PASS; 0 markers/12 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 4 high, 1 med, 1 low

FIX-HIGH: The first call fragment is buried at line 77 (45.8%) and there is no `## The short version` — open with a counted set of `.proto`, generated-client, channel, and request inputs, one callable unary RPC, its exact response/status, and linked deferrals for deadlines, TLS, retries, and compatibility.
FIX-HIGH: Gloss ProtoJSON at line 115 as Protocol Buffers' specified JSON mapping before warning that its compatibility differs from binary wire compatibility.
FIX-HIGH: Gloss server reflection at line 144 as runtime service/schema discovery before asking the reader to choose an exposure policy.
FIX-HIGH: The `.proto` definition, generated modules, channel/stub creation, call, and visible result are never assembled — add one runnable unary client/server baseline whose output proves generation and transport wiring before the streaming and operational material.
FIX-MED: Section 1 defines gRPC before establishing why generated cross-language calls are needed — introduce a concrete client/server contract-drift problem, then explain how the `.proto`-generated method boundary addresses it.
FIX-LOW: Add one transferable `> **Key insight**:` stating that generated call syntax does not erase network ambiguity, deadlines, compatibility, or retry semantics.

# apis/README.md (54 lines)
ORDERING: n/a (pure collection index and reading-order file; no per-file teaching sequence).
EXPLANATION: n/a (pure collection index and link list; explanation heuristics do not apply).
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index names every owned API note and deep-dive branch with concise scope descriptions and valid local entry links.

# apis/restful/01_rest_mental_model.md (176 lines)
ORDERING: payoff line 42/176 (0.239, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:16 (PASS; 2 markers/16 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: The first complete resource/representation exchange starts at line 42 (23.9%), beyond the 15% boundary, and there is no `## The short version` — open with that `GET`/`200` example, a counted input list, the exact response signal, and linked deferrals for hypermedia, state, and production HTTP semantics.
FIX-HIGH: Gloss hypermedia at line 9 as representations containing links or controls for available next actions; the detailed explanation at line 83 comes too late for the opening definition.
FIX-MED: Section 1 opens with a formal definition and six-row constraint table — put the concrete “JSON endpoints are not automatically REST” problem and one resource exchange before the taxonomy.
FIX-LOW: Add one transferable `> **Key insight**:` stating that REST's value comes from constraints creating shared visibility and evolvability, not from noun-shaped URLs alone.

# apis/restful/02_http_semantics.md (180 lines)
ORDERING: payoff line 139/180 (0.772, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:15 (PASS; 0 markers/15 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 0 low

FIX-HIGH: The first concrete request is buried at line 139 (77.2%) and still has no response outcome; add `## The short version` with a counted set of method/target/headers, one request/response showing safe and idempotent semantics, its exact status/body signal, and links to negotiation, intermediaries, and retry hardening.
FIX-HIGH: Expand and gloss QUIC at line 17 as HTTP/3's underlying secure multiplexed transport before using it to distinguish protocol versions.
FIX-MED: Section 1 starts with version/framing taxonomy rather than the reader's failure — lead with a proxy or retry interpreting a mislabeled operation incorrectly, then explain why shared semantics survive HTTP versions.

# apis/restful/03_resource_and_uri_design.md (228 lines)
ORDERING: payoff line 11/228 (0.048, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 3:18 (PASS; 3 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 3; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: The domain-to-resource trace appears early, but `## The short version` is absent — add the problem/mental model, a counted list of domain inputs, one request/response with an observable resource outcome, and linked deferrals for commands, concurrency, bulk work, and tenant boundaries.
FIX-HIGH: The `❌`/`✅` deep-nesting comparison at lines 68–70 states conclusions without the failure mechanism — explain how deeply coupled paths duplicate authorization context, destabilize identifiers, and make independently addressable comments harder to link or move before presenting the alternatives.
FIX-LOW: Add one transferable `> **Key insight**:` stating that a resource boundary follows identity, lifecycle, and authorization rather than database layout.

# apis/restful/04_representations_validation_and_errors.md (258 lines)
ORDERING: payoff line 109/258 (0.422, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 1:14 (PASS; 1 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: The first request with a visible error outcome is buried at line 109 (42.2%) and there is no `## The short version` — open with a counted malformed-request example, its exact Problem Details response, and links to schema separation, layered validation, framework mapping, and partial-result hardening.
FIX-HIGH: Line 204 tells readers to “log the full internal error,” which can reintroduce the raw dependency details and secret-bearing context prohibited at line 135 — prescribe structured, access-controlled exception telemetry with a correlation ID and explicit redaction of credentials, request bodies, SQL values, and raw dependency payloads.
FIX-MED: Section 1 opens with a representation definition — start with the failure caused by serializing an ORM object directly (writable internal fields and unstable storage shape), then introduce separate public input/output types.
FIX-LOW: Add one transferable `> **Key insight**:` explaining that status codes classify interoperability while stable problem identifiers drive application decisions.

# apis/restful/05_pagination_filtering_and_search.md (261 lines)
ORDERING: payoff line 63/261 (0.241, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 3:19 (PASS; 3 markers/19 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 0 med, 1 low

FIX-HIGH: The first query/output pagination trace starts at line 63 (24.1%), beyond the 15% boundary, and there is no `## The short version` — open with a counted cursor request, returned items/`next_cursor`, the exact success signal, and links to signing, filter safety, search, and consistency limits.
FIX-HIGH: Expand and gloss HMAC at the signed-cursor implementation on lines 102–104 as a keyed message-authentication code used to detect cursor modification; code imports are not a first-use explanation.
FIX-HIGH: Gloss collation at line 203 as the database's text comparison and ordering rules before asking readers to define it for stable sorting.
FIX-LOW: Add one transferable `> **Key insight**:` stating that pagination stability comes from a deterministic ordered position plus bounded query semantics, not from cursor encoding itself.

# apis/restful/06_concurrency_idempotency_and_retries.md (266 lines)
ORDERING: payoff line 11/266 (0.041, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:23 (PASS; 0 markers/23 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: The ambiguous-outcome trace appears early, but `## The short version` is absent — wrap it with a counted set of request/identity/state inputs, the exact timeout-versus-commit observation, and links to conditional writes, idempotency storage, retry classification, and client hardening.
FIX-LOW: Add one transferable `> **Key insight**:` stating that retry safety is a property of durable operation identity and effects, not of transport failure or method name alone.

# apis/restful/07_caching_and_performance.md (173 lines)
ORDERING: payoff line 60/173 (0.347, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 1:18 (PASS; 1 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: The first complete validation exchange begins at line 60 (34.7%) and there is no `## The short version` — open with a counted `ETag`/`If-None-Match` exchange, its exact `304` success signal, and linked deferrals for private/shared selection, `Vary`, invalidation, and security testing.
FIX-HIGH: Expand TTL at line 122 as time to live—the fallback expiry after which cached state is no longer reused—before making it part of the invalidation principle.
FIX-MED: Section 1 defines a cache before putting the reader in the stale or cross-tenant response failure — lead with that consequence, then attach storage and reuse rules.
FIX-LOW: Convert the invalidation principle into the required single `> **Key insight**:` or add an equivalent transferable insight using the mandated label.

# apis/restful/08_security.md (245 lines)
ORDERING: payoff line 74/245 (0.302, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 1:25 (PASS; 1 markers/25 explanatory paragraphs); restatement PASS; unglossed first uses 5; unexplained rules/defenses 1; intuition-building explanation yes.
Summary: 0 critical, 7 high, 0 med, 1 low

FIX-HIGH: The first attack/defense code starts at line 74 (30.2%) and there is no `## The short version` — open with a counted principal/order example, the cross-tenant denial signal, and linked deferrals for token validation, property authorization, browser boundaries, abuse, and verification.
FIX-HIGH: Expand and gloss Broken Object Level Authorization (`BOLA`) and Insecure Direct Object Reference (`IDOR`) at line 70 before using the acronyms as the section's central failure class.
FIX-HIGH: Expand JSON Web Token (`JWT`) at line 103 and identify it as a signed claim container whose tenant semantics are trusted only under an explicit issuer, audience, and token-profile contract.
FIX-HIGH: Expand cross-site scripting (`XSS`) at line 160 and state that injected browser script can steal or misuse explicitly managed bearer credentials.
FIX-HIGH: Expand server-side request forgery (`SSRF`) at line 191 before treating URL-fetch and webhook destinations as instances of it.
FIX-HIGH: The defense example at lines 72–92 lacks the required attacker-ordered explanation — show an authenticated tenant-7 user substituting tenant-8's `order_id`, the unscoped lookup returning that row, the resulting disclosure/mutation, and how the scoped predicate moves the tenant choice back to trusted principal context.
FIX-HIGH: Replace line 103's unconditional claim that a JWT tenant claim is “the strongest source” and cannot be forged with the actual trust chain — validate signature/algorithm, issuer, audience, expiry, and the issuer's tenant-entitlement semantics, or resolve allowed tenants server-side when that contract is absent.
FIX-LOW: Add one transferable `> **Key insight**:` stating that API authorization is a decision over principal, operation, object relationship, property, and current state—not a one-time token check.

# apis/restful/09_versioning_compatibility_and_openapi.md (207 lines)
ORDERING: payoff line 11/207 (0.053, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:14 (PASS; 0 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: The evolution trace appears early, but `## The short version` is absent — add a counted old/new contract example, the exact old-client/new-provider success signal, and linked deferrals for version selection, OpenAPI limits, deprecation, and rollback testing.
FIX-HIGH: The response schema closes `Order` with `additionalProperties: false` at line 110 while the note calls additive response fields usually compatible — either make response objects open to additive fields or state that old strict validators will reject additions and therefore closure changes the compatibility policy; keep stricter unknown-field rejection on request schemas where intended.
FIX-LOW: Add one transferable `> **Key insight**:` explaining that wire-compatible schema evolution can still break behavior, rollback, or exhaustive clients.
NO-ACTION: The “latest published specification is 3.2.0” claim at line 73 remains current as checked 2026-08-17: https://spec.openapis.org/oas/latest.html.

# apis/restful/10_testing_observability_and_operations.md (207 lines)
ORDERING: payoff line 49/207 (0.237, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:14 (PASS; 0 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: The first executable contract assertion starts at line 49 (23.7%), beyond the 15% boundary, and there is no `## The short version` — open with a counted fixture/client set, one test command and exact passing output, and links to the broader matrix, telemetry, SLOs, rollout, and incident diagnosis.
FIX-HIGH: Expand service-level objective (`SLO`) at the line-129 heading and distinguish it from the service-level indicators measured in the following paragraph.
FIX-LOW: Add one transferable `> **Key insight**:` stating that production confidence comes from preserving the same contract decisions across tests, telemetry, rollout, and incident recovery.

# apis/restful/README.md (37 lines)
ORDERING: n/a (pure subcollection index and reading-order file; no per-file teaching sequence).
EXPLANATION: n/a (pure subcollection index and link list; explanation heuristics do not apply).
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index assigns a clear topic and scope to all ten REST chapters and provides both sequential and risk-oriented entry guidance.

# apis/webhooks/01_delivery_model_and_event_contracts.md (218 lines)
ORDERING: payoff line 45/218 (0.206, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 10:16 (PASS; 10 markers/16 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 10; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The first named delivery/attempt outcome begins at line 45 (20.6%), beyond the 15% boundary, and there is no `## The short version` — open with that event/delivery/attempt trace, a counted input list, the exact duplicate/receipt signal, and links to signing, durability, retry, replay, and reconciliation.
FIX-HIGH: The six event-name and four payload `✅`/`❌`/`⚠️` conclusions at lines 98–104 and 132–142 lack local causal explanations — show how command/vague names break stable consumer routing and how thin/full payload mechanics produce each stated availability, staleness, and exposure trade-off before the markers.

# apis/webhooks/02_producer_design.md (227 lines)
ORDERING: payoff line 62/227 (0.273, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:19 (PASS; 2 markers/19 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: The first durable producer transition begins at line 62 (27.3%) and there is no `## The short version` — open with a counted invoice/subscription/outbox example, its committed-event success signal, and links to relay, leases, endpoint security, retries, and replay.
FIX-HIGH: Expand server-side request forgery (`SSRF`) at line 41 and state that a customer-controlled callback URL can make the delivery worker reach internal or metadata services; a cross-link alone is not a first-use gloss.
FIX-LOW: Add one transferable `> **Key insight**:` stating that the business transaction creates an immutable event, while deliveries and attempts are independently retryable operational state.

# apis/webhooks/03_consumer_design.md (276 lines)
ORDERING: payoff line 84/276 (0.304, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:17 (PASS; 0 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 0 med, 1 low

FIX-HIGH: The first composed ingress implementation starts at line 84 (30.4%) and there is no `## The short version` — open with a counted raw-body/headers/secret/database example, one signed delivery, the exact `204` plus durable-row success signal, and linked deferrals for worker leases, ordering, and poison events.
FIX-HIGH: Expand HMAC at line 40 as a hash-based message authentication code over the exact request bytes before pointing to the implementation chapter.
FIX-HIGH: The full security-and-durability pipeline at lines 9–20 precedes any smallest complete consumer trace — first show verify exact bytes, insert one event under a unique ID, return `204`, and observe the inbox row; then layer compression limits, worker leasing, reconciliation, and quarantine.
FIX-LOW: Add one transferable `> **Key insight**:` stating that a fast `2xx` is safe only after durable acceptance, while business processing belongs to an idempotent worker.

# apis/webhooks/04_signatures_security_and_ssrf.md (282 lines)
ORDERING: payoff line 54/282 (0.191, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:16 (PASS; 0 markers/16 explanatory paragraphs); restatement PASS; unglossed first uses 5; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 5 high, 0 med, 1 low

FIX-HIGH: The first implementation begins at line 54 (19.1%), beyond the 15% boundary, and lacks a caller/result; add `## The short version` with counted body/header/secret inputs, one sign/verify call, the exact accepted/rejected signal, and links to rotation, replay storage, SSRF, and ownership controls.
FIX-HIGH: Expand HMAC at line 25 as a hash-based message authentication code that proves possession of a shared secret and detects body modification.
FIX-HIGH: Expand server-side request forgery (`SSRF`) at line 16 and state that an attacker-controlled callback URL can turn the producer into a request client for otherwise unreachable services.
FIX-HIGH: Expand mutual TLS (`mTLS`) at line 190 as client-and-server certificate authentication before positioning it as defense in depth.
FIX-HIGH: Gloss RFC1918 at line 204 as private IPv4 address space and IMDSv2 at line 237 as AWS's session-oriented instance metadata service protection; neither acronym tells a first-time reader what destination or defense is meant.
FIX-LOW: Add one transferable `> **Key insight**:` explaining that signatures protect message authenticity while SSRF controls protect the producer's network—neither substitutes for the other.

# apis/webhooks/05_retries_idempotency_ordering_and_replay.md (222 lines)
ORDERING: payoff line 9/222 (0.041, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:18 (PASS; 2 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: The duplicate-delivery trace appears early, but `## The short version` is absent — wrap it with a counted event/delivery/attempt state set, the exact duplicate-ignore/`204` observation, and links to backoff, transactional effects, ordering, replay, and reconciliation.
FIX-LOW: Add one transferable `> **Key insight**:` stating that retries preserve event identity, while replay changes operational attempt history without inventing a new business fact.

# apis/webhooks/06_testing_observability_and_operations.md (235 lines)
ORDERING: payoff line 191/235 (0.813, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:17 (PASS; 0 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 0 med, 1 low

FIX-HIGH: The first concrete operational trace is buried at line 191 (81.3%) and the earlier fixture tree has no executed result; add `## The short version` with counted fixture/signer/endpoint inputs, one exact verification test, its passing output and common reserialization failure signal, and links to the full matrices, SLOs, retention, and runbooks.
FIX-HIGH: Expand server-side request forgery (`SSRF`) at the line-49 test heading and state that these cases prove customer URLs cannot reach forbidden destinations.
FIX-HIGH: Expand service-level objective (`SLO`) at the line-140 heading before listing producer and consumer targets.
FIX-LOW: Add one transferable `> **Key insight**:` stating that HTTP acceptance and business processing are separate operational pipelines and require separate lag, failure, and recovery signals.

# apis/webhooks/README.md (33 lines)
ORDERING: n/a (pure subcollection index and reading-order file; no per-file teaching sequence).
EXPLANATION: n/a (pure subcollection index and link list; explanation heuristics do not apply).
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index cleanly separates producer, consumer, shared security, reliability, and operations ownership and links every chapter.

# apis/websockets/01_protocol_and_connection_lifecycle.md (169 lines)
ORDERING: payoff line 32/169 (0.189, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:19 (PASS; 0 markers/19 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 0 med, 0 low

FIX-HIGH: The handshake exchange starts at line 32 (18.9%), beyond the 15% boundary, and there is no `## The short version` — open with counted URL/origin/subprotocol inputs, the request/`101` response, its exact negotiated-protocol signal, and links to authentication, framing, closure, and recovery.
FIX-HIGH: Expand network address translation (`NAT`) at line 106 and state that an idle mapping can expire without either WebSocket peer receiving a close frame.
FIX-HIGH: Expand Web Real-Time Communication (`WebRTC`) at line 153 and identify it as the browser/platform stack for peer media/data connectivity before recommending it as an alternative.

# apis/websockets/02_message_protocols_and_contracts.md (203 lines)
ORDERING: payoff line 72/203 (0.355, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:18 (PASS; 0 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 0 med, 1 low

FIX-HIGH: The first concrete response envelope starts at line 72 (35.5%) without its triggering command, and there is no `## The short version` — open with a counted command/envelope/connection-state example, the correlated reply signal, and links to limits, state machines, evolution, and recovery.
FIX-HIGH: Expand `Ack` at line 66 as an application acknowledgement that confirms a defined receipt or processing milestone, distinct from protocol ping/pong and socket delivery.
FIX-HIGH: Gloss AsyncAPI at line 198 as a machine-readable description format for asynchronous channels and messages before stating what it cannot express.
FIX-LOW: Add one transferable `> **Key insight**:` stating that WebSocket supplies ordered message transport on one connection, while the application must define identity, state, authorization, and recovery semantics.

# apis/websockets/03_reliability_reconnection_and_flow_control.md (201 lines)
ORDERING: payoff line 109/201 (0.542, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:23 (PASS; 0 markers/23 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: The first concrete recovery outcome is the resume-expired trace at line 109 (54.2%) and there is no `## The short version` — open with a counted connection/event-position example, the exact replay-or-snapshot result, and links to heartbeats, backoff, ordering, backpressure, and command ambiguity.
FIX-LOW: Add one transferable `> **Key insight**:` stating that reconnect restores transport only; durable identity plus replay or snapshot restores application state.

# apis/websockets/04_authentication_and_security.md (186 lines)
ORDERING: payoff line 61/186 (0.328, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 5:20 (PASS; 5 markers/20 explanatory paragraphs); restatement PASS; unglossed first uses 3; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 0 med, 1 low

FIX-HIGH: The first concrete attack/allowlist outcome begins at line 61 (32.8%) and there is no `## The short version` — open with counted cookie/origin/resource inputs, the malicious-origin rejection signal, and links to credential choices, per-message authorization, revocation, abuse, and telemetry.
FIX-HIGH: Expand Cross-Origin Resource Sharing (`CORS`) and XMLHttpRequest (`XHR`) at line 75 before contrasting their browser response policy with WebSocket origin enforcement.
FIX-HIGH: Expand TTL at line 107 as time to live—the maximum age of a cached authorization decision before re-evaluation.
FIX-LOW: Add one transferable `> **Key insight**:` stating that a long-lived authenticated channel creates repeated authorization decisions, not one permission grant at handshake time.

# apis/websockets/05_scaling_and_distributed_architecture.md (209 lines)
ORDERING: payoff line 11/209 (0.053, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:23 (PASS; 0 markers/23 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: The multi-process ownership failure appears early, but `## The short version` is absent — add counted socket-owner/event-router/durable-state inputs, one cross-pod delivery trace with its observed client result, and links to routing, leases, backpressure, deployment, and regional hardening.
FIX-HIGH: Expand TTL at line 53 as time to live—the expiry used to remove stale presence or directory leases after an owner disappears.
FIX-LOW: Add one transferable `> **Key insight**:` stating that scaling sockets requires separating live connection ownership, event movement, and durable recovery state.

# apis/websockets/06_implementation_testing_and_operations.md (366 lines)
ORDERING: payoff line 21/366 (0.057, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:9 (PASS; 0 markers/9 explanatory paragraphs); restatement FAIL; unglossed first uses 3; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 6 high, 1 med, 1 low

FIX-CRITICAL: Lines 154–156 call `receive_text()` before checking `MAX_INBOUND_BYTES`, so the framework has already buffered and decoded the complete (and possibly decompressed) message and the advertised 16 KiB security bound is not enforced before allocation — configure and test the selected ASGI/WebSocket backend's pre-allocation message limit, retain the application check as defense in depth, and document compressed/fragmented behavior; Uvicorn exposes `--ws-max-size` and `--ws-max-queue` (checked 2026-08-17): https://www.uvicorn.org/settings/.
FIX-HIGH: The runnable block appears early, but `## The short version` is absent — add the problem/mental model, a counted environment/client input list, one subscribe/ping procedure with the exact reply signal, and links to security, queueing, deployment, and recovery omissions.
FIX-HIGH: The first example is a 221-line hardened service containing custom authentication, validation, queues, task coordination, and cleanup before a minimal connection runs — precede it with a small safe origin/authenticate/accept/receive/reply baseline and explicitly link each deferred production concern to the reference implementation.
FIX-HIGH: Expand HMAC at its first code use on line 24 and explain that the keyed digest authenticates the exact `user_id.expires_at` value while `compare_digest` prevents timing-sensitive equality checks.
FIX-HIGH: Expand Asynchronous Server Gateway Interface (`ASGI`) at line 268 and identify the WebSocket scope as the reason HTTP-only middleware is bypassed.
FIX-HIGH: Expand round-trip time (`RTT`) at line 346 before using it as a heartbeat metric.
FIX-HIGH: The full-note restatement test fails because removing the code leaves no causal explanation of the signed-cookie format, pre-accept rejection behavior, queue-overflow transition, or sender/receiver task shutdown — add short prose traces for each so a reader can explain why the implementation remains bounded and authenticated without reciting code.
FIX-MED: Lines 199–209 assign WebSocket close codes/reasons before `accept()`, but Starlette sends an HTTP `403` denial in that state, so clients do not observe the advertised `1008`/`1002` close semantics — use an explicit pre-upgrade denial response/status where supported and reserve WebSocket close codes for accepted connections; checked 2026-08-17: https://www.starlette.io/websockets/#send-denial-response.
FIX-LOW: Add one transferable `> **Key insight**:` stating that one reader, one writer, and a bounded queue turn concurrent producers into one ordered ownership path per socket.

# apis/websockets/README.md (33 lines)
ORDERING: n/a (pure subcollection index and reading-order file; no per-file teaching sequence).
EXPLANATION: n/a (pure subcollection index and link list; explanation heuristics do not apply).
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index gives every WebSocket chapter a distinct role and presents the intended protocol-to-operations progression without duplicating note content.

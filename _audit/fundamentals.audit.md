# fundamentals/README.md (48 lines)
ORDERING: n/a — repository-section index and reading map.
EXPLANATION: n/a — repository-section index and reading map.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index bounds the section and offers task-oriented entry routes without pretending to be a teaching note.

# fundamentals/auth/README.md (72 lines)
ORDERING: n/a — section index and decision lookup.
EXPLANATION: n/a — section index and decision lookup.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The file is a navigable map whose sessions-versus-tokens appendix supports lookup rather than a teaching sequence.

# fundamentals/auth/cognito/cognito.md (312 lines)
ORDERING: payoff line 95/312 (0.304, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:10 (PASS; 0 markers/10 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 1 high, 0 med, 1 low

FIX-CRITICAL: Lines 238–249 say Lite includes 50,000 free direct/social MAUs and estimate a 100k-Lite bill from that allowance — replace the pricing figures and worked estimate because AWS now grants 10,000 free direct/social MAUs to both Lite and Essentials; checked 2026-08-17 against https://aws.amazon.com/cognito/pricing/.
FIX-HIGH: Add `## The short version` before the service taxonomy with a bounded input list, one named User Pool login-to-API trace, its exact accepted/rejected observation, and linked deferrals; the first composed trace is currently buried at line 95 (30.4%).
FIX-LOW: Add exactly one transferable `> **Key insight**:`; use the boundary that User Pools issue application identity while Identity Pools exchange identity for AWS credentials.

# fundamentals/auth/cognito/oauth-jwt-guide.md (409 lines)
ORDERING: payoff line 11/409 (0.027, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:3 (PASS; 0 markers/3 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with the exact three Cognito inputs, a minimal client-credentials token request and API call, the expected status/claim, and linked deferrals for user login, validation, refresh, and gateway authorization.
FIX-MED: Line 384 restricts refresh-token rotation to Essentials/Plus without support in the current feature-plan documentation — remove the tier restriction or cite the exact enforced plan gate; AWS documents the app-client setting without that restriction; checked 2026-08-17 against https://docs.aws.amazon.com/cognito/latest/developerguide/amazon-cognito-user-pools-using-the-refresh-token.html and https://docs.aws.amazon.com/cognito/latest/developerguide/cognito-sign-in-feature-plans.html.
FIX-LOW: Add exactly one `> **Key insight**:` that transfers beyond Cognito: the issuer creates tokens, but each resource server still owns audience/scope enforcement.

# fundamentals/auth/cognito/tokens.md (385 lines)
ORDERING: payoff line 17/385 (0.044, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:4 (PASS; 0 markers/4 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 1 high, 0 med, 1 low

FIX-CRITICAL: Lines 252–260 present `validate_token_pyjwt()` while disabling audience validation and omitting issuer and `token_use` checks — make token kind explicit and validate signature, expiry, issuer, app-client/resource-server audience, and `token_use` in the callable itself.
FIX-HIGH: Add `## The short version` with the three token types, the one token an API should accept, a named valid/invalid claim trace, the exact rejection signal, and links to rotation and revocation.
FIX-LOW: Add exactly one `> **Key insight**:` explaining that token shape does not establish intended use; the verifier must bind type and audience to the endpoint.

# fundamentals/auth/cognito/user-pool.md (621 lines)
ORDERING: payoff line 7/621 (0.011, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 0:2 (PASS; 0 markers/2 explanatory paragraphs); restatement FAIL; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 2 med, 1 low

FIX-HIGH: Add `## The short version` before the 80-line pool configuration with a counted minimum input set, a small create-client/login baseline, the exact API response to verify, and linked deferrals for challenges, triggers, reset, and hosted login.
FIX-HIGH: Add causal prose around the central configuration choices so a reader can explain why a pool, app client, auth flow, and challenge compose; after removing code and lists, the note is primarily an instruction catalog and fails restatement.
FIX-MED: Line 92 lists `MfaConfiguration` as immutable, although Amazon Cognito exposes it through `UpdateUserPool` — separate genuinely immutable sign-in/schema choices from settings that remain changeable; checked 2026-08-17 against https://docs.aws.amazon.com/cognito-user-identity-pools/latest/APIReference/API_UpdateUserPool.html.
FIX-MED: Split the 621-line file at the user-management/Lambda-trigger boundary, or add a concrete `<!-- length-justification: ... -->` near the top.
FIX-LOW: Add exactly one `> **Key insight**:` about app clients being policy profiles over one shared directory.

# fundamentals/auth/jwt.md (492 lines)
ORDERING: payoff line 13/492 (0.026, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:13 (PASS; 0 markers/13 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 2 critical, 1 high, 0 med, 1 low

FIX-CRITICAL: Lines 200–206 demonstrate leeway with decoders that omit audience and, in the python-jose call, issuer validation — keep the leeway example correctness-complete by pinning the algorithm and supplying expected issuer and audience in both calls.
FIX-CRITICAL: Lines 268–293 make `audience` optional and disable `verify_aud` when absent in a function titled `validate_token` — require the endpoint's expected audience instead of allowing callers to silently skip this trust-boundary check.
FIX-HIGH: Add `## The short version` with a counted issuer/JWKS/audience input set, one fully validated token call, the exact accepted claims and rejected exception, and linked deferrals for caching, rotation, revocation, and framework integration.
FIX-LOW: Add exactly one `> **Key insight**:` that distinguishes cryptographic authenticity from endpoint suitability.

# fundamentals/auth/oauth2.md (312 lines)
ORDERING: payoff line 37/312 (0.119, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:6 (PASS; 0 markers/6 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with a counted actor/input list, one authorization-code-plus-PKCE trace with named values and visible token result, and linked deferrals for client credentials, refresh, device flow, scopes, and provider-specific setup.
FIX-MED: Lines 45 and 150–154 describe OAuth 2.1 requirements/removals as though OAuth 2.1 were a published standard — label it as the current Internet-Draft and distinguish its consolidation from already-published OAuth Security BCP guidance; checked 2026-08-17 against https://datatracker.ietf.org/doc/html/draft-ietf-oauth-v2-1-15.
FIX-LOW: Add exactly one `> **Key insight**:` about OAuth delegating bounded authority rather than proving an API caller's application-level permissions by itself.

# fundamentals/concurrency/00_decision_guide.md (224 lines)
ORDERING: payoff line 48/224 (0.214, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:8 (PASS; 0 markers/8 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with a four-choice decision trace, a counted set of bottleneck facts, the chosen model as success signal, and linked deferrals; the first complete decision flow is at line 48 (21.4%).
FIX-LOW: Add exactly one `> **Key insight**:` stating that scheduler choice follows the blocking resource and ownership boundary, not an `async`/CPU label alone.

# fundamentals/concurrency/01_state_and_safety.md (306 lines)
ORDERING: payoff line 15/306 (0.049, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:14 (PASS; 0 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` that turns the shared-list trace into a complete baseline with counted owners/state, a visible lost-update result, and linked deferrals for locks, processes, deployments, and context propagation.
FIX-LOW: Add exactly one `> **Key insight**:` about reachability plus mutation plus scheduler determining the safety boundary.

# fundamentals/concurrency/02_alternative_runtimes.md (229 lines)
ORDERING: payoff line 53/229 (0.231, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:8 (PASS; 0 markers/8 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with the default process-pool choice, three compatibility inputs, the minimal `InterpreterPoolExecutor` run and output, and linked deferrals; the first usable example is line 53 (23.1%).
FIX-LOW: Add exactly one `> **Key insight**:` distinguishing isolation-per-interpreter from shared-memory free threading.

# fundamentals/concurrency/README.md (106 lines)
ORDERING: n/a — section index, chooser, and command lookup.
EXPLANATION: n/a — section index, chooser, and command lookup.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The README clearly owns navigation and lookup while sending implementation teaching to canonical notes.

# fundamentals/concurrency/async/01_event_loop_and_tasks.md (328 lines)
ORDERING: payoff line 83/328 (0.253, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:10 (PASS; 0 markers/10 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: Add `## The short version` with a counted two-coroutine input, one timed sequential-versus-concurrent run and output, plus linked deferrals for task ownership, cancellation, and blocking work; the first composed payoff is line 83/328 (25.3%).

# fundamentals/concurrency/async/02_production_patterns.md (359 lines)
ORDERING: payoff line 20/359 (0.056, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 3:11 (PASS; 3 markers/11 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with bounded workload/capacity/deadline inputs, one runnable bounded call and exact timeout/queue observation, and linked deferrals for cancellation, cleanup, shutdown, and observability.
FIX-LOW: Add exactly one `> **Key insight**:` about bounding active work and queued work independently.

# fundamentals/concurrency/async/03_contextvars.md (384 lines)
ORDERING: payoff line 45/384 (0.117, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:12 (PASS; 2 markers/12 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: Add `## The short version` with one request ID, two tasks, the set/read/reset code, visible isolated output, and linked deferrals for threads, processes, mutable values, and framework middleware.

# fundamentals/concurrency/async/README.md (86 lines)
ORDERING: n/a — subsection index and diagnostic lookup.
EXPLANATION: n/a — subsection index and diagnostic lookup.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The README provides a compact mental-model reminder and routes full teaching to the three owned notes.

# fundamentals/concurrency/processes/01_process_pool_executor.md (363 lines)
ORDERING: payoff line 30/363 (0.083, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:11 (PASS; 0 markers/11 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with a counted CPU input/worker/result set, the existing minimal run plus exact output, and linked deferrals for pickling, batching, cancellation, startup, and shutdown.
FIX-LOW: Add exactly one `> **Key insight**:` about crossing a serialization boundary to buy interpreter isolation and CPU parallelism.

# fundamentals/concurrency/processes/README.md (71 lines)
ORDERING: n/a — subsection index and command lookup.
EXPLANATION: n/a — subsection index and command lookup.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The file stays within its map/lookup role and gives one clear next note.

# fundamentals/concurrency/threads/01_thread_pool_executor.md (363 lines)
ORDERING: payoff line 30/363 (0.083, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:11 (PASS; 0 markers/11 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with counted blocking calls/workers, the minimal run and exact elapsed/result signal, and linked deferrals for sizing, cancellation, context, deadlocks, and shared state.
FIX-LOW: Add exactly one `> **Key insight**:` about threads integrating blocking code without turning caller timeouts into worker termination.

# fundamentals/concurrency/threads/02_synchronization_primitives.md (490 lines)
ORDERING: payoff line 20/490 (0.041, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:18 (PASS; 0 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with one shared invariant, two threads, one lock-protected runnable trace, exact final state, and linked deferrals for conditions, queues, reader-writer patterns, deadlock, and CAS.
FIX-LOW: Add exactly one `> **Key insight**:` about protecting the invariant boundary rather than an individual source line.

# fundamentals/concurrency/threads/README.md (90 lines)
ORDERING: n/a — subsection index and primitive lookup.
EXPLANATION: n/a — subsection index and primitive lookup.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The README marks the thread use boundary and routes implementation details to their canonical owners.

# fundamentals/core_concepts/README.md (43 lines)
ORDERING: n/a — section index and reading map.
EXPLANATION: n/a — section index and reading map.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index is concise and its sequence identifies the role of each owned note.

# fundamentals/core_concepts/configuration.md (1050 lines)
ORDERING: payoff line 73/1050 (0.070, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 21:11 (PASS; 21 markers/11 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 1 high, 1 med, 1 low

FIX-CRITICAL: Replace the Stripe-shaped values at lines 35, 90, 152, 525, 630, and 984 with unmistakable non-credential placeholders such as `example-not-a-real-key`; the toy-not-correct scan forbids real-looking credentials even in negative examples.
FIX-HIGH: Add `## The short version` with a counted database URL/API key input set, the minimal `Settings` model and startup command, exact parsed output plus missing-variable failure, and linked deferrals for nesting, caching, secret delivery, and environment profiles.
FIX-MED: Split the 1,050-line note at “Secrets Management”/“Complete Production Example,” or add a concrete `<!-- length-justification: ... -->` near the top.
FIX-LOW: Add exactly one `> **Key insight**:` about treating deployment strings as untrusted input at one typed startup boundary.

# fundamentals/core_concepts/context_managers.md (346 lines)
ORDERING: payoff line 13/346 (0.038, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 4:7 (PASS; 4 markers/7 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with one resource/body/failure input trace, exact cleanup observation, and linked deferrals for suppression, async managers, composition, and reuse.
FIX-LOW: Add exactly one `> **Key insight**:` explaining that a context manager owns an enter/exit protocol, not merely a convenient `try/finally` spelling.

# fundamentals/core_concepts/decorators.md (1252 lines)
ORDERING: payoff line 16/1252 (0.013, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 8:39 (PASS; 8 markers/39 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 0 low

FIX-HIGH: Add `## The short version` with a counted function/decorator/call input set, the rebinding trace and exact output, and linked deferrals for signatures, factories, async wrappers, ordering, descriptors, and production mistakes.
FIX-MED: Split the 1,252-line note after the canonical three decorator shapes, with a named continuation for production patterns/protocol edge cases, or add a concrete length justification.

# fundamentals/core_concepts/exceptions.md (643 lines)
ORDERING: payoff line 18/643 (0.028, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 8:21 (PASS; 8 markers/21 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 0 low

FIX-HIGH: Add `## The short version` with named call-stack actors, one raised exception and visible propagated traceback, plus linked deferrals for translation, cleanup, retries, groups, and API boundaries.
FIX-MED: Split the 643-line note at domain exception design or document why propagation, policy, concurrency, and testing must remain one file with `<!-- length-justification: ... -->`.

# fundamentals/core_concepts/logging/01_basics.md (279 lines)
ORDERING: payoff line 19/279 (0.068, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:9 (PASS; 2 markers/9 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with a counted logger/level/message input set, the smallest setup, exact emitted line, the silent-level-filter tell, and links to hierarchy, handlers, and service patterns.
FIX-LOW: Add exactly one `> **Key insight**:` about a log call becoming an event only after admission, record creation, handling, and rendering.

# fundamentals/core_concepts/logging/02_hierarchy_and_propagation.md (240 lines)
ORDERING: payoff line 14/240 (0.058, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:9 (PASS; 0 markers/9 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: Add `## The short version` with two dotted logger names, one handler, a concrete emission trace, the exact duplicate/missing-line signal, and linked deferrals for propagation and configuration ownership.

# fundamentals/core_concepts/logging/03_handlers_and_formatters.md (352 lines)
ORDERING: payoff line 14/352 (0.040, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:4 (PASS; 0 markers/4 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with one record, two destinations, the runnable setup and exact console/file observations, plus linked deferrals for filters, queues, rotation, and failure handling.
FIX-LOW: Add exactly one `> **Key insight**:` explaining that handlers decide destinations while formatters decide representation of the same record.

# fundamentals/core_concepts/logging/04_patterns.md (332 lines)
ORDERING: payoff line 33/332 (0.099, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:10 (PASS; 0 markers/10 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with the smallest application shape, one selected configuration pattern, exact emitted result and duplicate-handler tell, and linked deferrals for services, subtrees, factories, and libraries.
FIX-LOW: Add exactly one `> **Key insight**:` about configuring each logging subtree once at its ownership boundary.

# fundamentals/core_concepts/logging/README.md (32 lines)
ORDERING: n/a — subsection index and reading map.
EXPLANATION: n/a — subsection index and reading map.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The four-note sequence is explicit and avoids duplicating the implementations it indexes.

# fundamentals/core_concepts/signals.md (342 lines)
ORDERING: payoff line 21/342 (0.061, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:10 (PASS; 2 markers/10 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with one worker, `SIGTERM`, grace deadline, runnable handler/checkpoint trace, exact shutdown observation, and linked deferrals for asyncio, Uvicorn, PID 1, ordering, and lifecycle tests.
FIX-LOW: Add exactly one `> **Key insight**:` about a signal starting a bounded shutdown protocol rather than performing cleanup inside the handler.

# fundamentals/core_concepts/structlog_guide.md (1031 lines)
ORDERING: payoff line 37/1031 (0.036, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 14:12 (PASS; 14 markers/12 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 0 low

FIX-HIGH: Add `## The short version` with a counted event/context/renderer set, a 10–25-line configuration and log call, exact JSON output plus missing-context tell, and linked deferrals for stdlib unification, middleware, sampling, and tests.
FIX-MED: Split the 1,031-line file after the minimal processor-chain/bound-logger baseline, with a named production-integration continuation, or add a concrete length justification.

# fundamentals/core_concepts/typing.md (378 lines)
ORDERING: payoff line 16/378 (0.042, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:7 (PASS; 2 markers/7 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with one typed function, one intentionally wrong call, the exact type-checker diagnostic, and links to unions, protocols, callables, metadata, and framework use.
FIX-LOW: Add exactly one `> **Key insight**:` about annotations specifying tool-visible contracts without enforcing runtime behavior by themselves.

# fundamentals/database/01_databases_and_schemas.md (770 lines)
ORDERING: payoff line 11/770 (0.014, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 0:17 (PASS; 0 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with one table/row/query input set, a minimal create-insert-select trace and exact result, plus linked deferrals for schemas, constraints, indexes, transactions, JSONB, and normalization.
FIX-MED: Split the 770-line file after the first relational schema/query baseline, with advanced PostgreSQL types/indexing/normalization as a named continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about constraints making data invariants shared and durable beyond one application process.

# fundamentals/database/02_python_drivers.md (640 lines)
ORDERING: payoff line 41/640 (0.064, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 5:1 (FAIL; 5 markers/1 explanatory paragraph); restatement FAIL; unglossed first uses 0; unexplained rules/defenses 3; intuition-building explanation yes.
Summary: 2 critical, 2 high, 2 med, 1 low

FIX-CRITICAL: Line 61 contains an executable psycopg SQL-injection example built with an f-string — remove executable interpolation and demonstrate the attacker-controlled value and resulting query in inert text beside only parameterized runnable code.
FIX-CRITICAL: Line 376 contains the same executable SQL-injection pattern for asyncpg — keep the unsafe shape non-executable and make `$1` binding the only runnable query.
FIX-HIGH: Add `## The short version` with counted DSN/query/parameter inputs, one sync or async driver call, exact returned row and connection-failure tell, and linked deferrals for pools, transactions, copying, and framework integration.
FIX-HIGH: Add causal prose for connection ownership, transaction boundaries, and placeholder binding; without code/tables/rules, the note does not let a new reader restate why driver operations are safe or durable.
FIX-MED: Add mechanism paragraphs before the cold `✅`/`❌` query rules and transaction prescriptions; the 5:1 register ratio exceeds the 2:1 contract.
FIX-MED: Split the 640-line note into a driver mental-model/baseline owner and an asyncpg/advanced-operations continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about the driver owning protocol, connection, and transaction mechanics beneath higher-level database APIs.

# fundamentals/database/03_sqlalchemy_orm.md (920 lines)
ORDERING: payoff line 30/920 (0.033, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 12:7 (PASS; 12 markers/7 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with one model/session/database input set, a minimal sync create/query and exact emitted SQL/result, and linked deferrals for relationships, transactions, loading, repositories, migrations, and performance.
FIX-MED: Split the 920-line note after the canonical sync model/session CRUD baseline, moving relationship/loading and production patterns to a named continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about the Session being a unit-of-work/identity-map boundary rather than a generic database connection.

# fundamentals/database/04_async_sqlalchemy.md (1407 lines)
ORDERING: payoff line 60/1407 (0.043, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 16:20 (PASS; 16 markers/20 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 1 high, 1 med, 1 low

FIX-CRITICAL: Line 1115 includes executable SQL interpolation in the raw-asyncpg section — remove the runnable injection shape and retain only the parameterized `$1` call, explaining the attack with inert query text.
FIX-HIGH: Add `## The short version` with counted engine/session/model inputs, one end-to-end FastAPI query and exact response, and linked deferrals for loading, transactions, retries, migrations, pooling, and raw asyncpg.
FIX-MED: Split the 1,407-line file after the async engine/session/FastAPI CRUD baseline; transactions, Alembic, repositories, pooling, and raw asyncpg need named continuation owners unless a concrete length justification explains the single-file dependency.
FIX-LOW: Add exactly one `> **Key insight**:` about async sessions making hidden I/O invalid, so loading boundaries must be explicit.

# fundamentals/database/05_connection_pooling.md (638 lines)
ORDERING: payoff line 40/638 (0.063, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 18:14 (PASS; 18 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with counted database cap/instance count/concurrency inputs, one computed pool configuration and observable checkout/timeout signal, and linked deferrals for PgBouncer, monitoring, leaks, startup herds, and query timeouts.
FIX-MED: Split the 638-line note after SQLAlchemy pool sizing/failure basics, with PgBouncer and asyncpg operations as a named continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about a pool being a queue plus a database-wide connection budget, not merely a reuse cache.

# fundamentals/database/06_alembic.md (893 lines)
ORDERING: payoff line 42/893 (0.047, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 0:7 (PASS; 0 markers/7 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 2 med, 1 low

FIX-HIGH: Add `## The short version` with counted metadata/database/revision inputs, one init-autogenerate-upgrade sequence, exact `current`/schema success signal, and linked deferrals for data changes, enums, branches, stamping, testing, and deployment.
FIX-MED: Lines 326–349 say `ALTER TYPE ... ADD VALUE` cannot run in a PostgreSQL transaction and prescribe autocommit; current PostgreSQL permits it in a transaction but the new value cannot be used until commit — update the failure condition and keep autocommit only for versions/workflows that demonstrably require it; checked 2026-08-17 against https://www.postgresql.org/docs/current/sql-altertype.html.
FIX-MED: Split the 893-line deep dive at the basic setup/core commands boundary or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about migrations being reviewed, immutable transition programs rather than authoritative diffs from current models.

# fundamentals/database/README.md (59 lines)
ORDERING: n/a — section index, learning map, and decision lookup.
EXPLANATION: n/a — section index, learning map, and decision lookup.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The README assigns canonical ownership and offers distinct task routes without duplicating implementation prose.

# fundamentals/fastapi/01_http_and_parameter_mapping.md (735 lines)
ORDERING: payoff line 110/735 (0.150, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 0:11 (PASS; 0 markers/11 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: Move a complete request-to-parameter mapping example, including the exact response or validation failure, above line 80; the first usable endpoint currently arrives at line 110.
FIX-HIGH: Add `## The short version` with counted path/query/body inputs, one minimal route, exact success/error output, and linked deferrals for files, forms, metadata, and advanced validation.
FIX-MED: Split the 735-line note after the minimal HTTP/FastAPI mapping baseline, with file/form upload and parameter-reference material in a named continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about FastAPI deriving request extraction and validation from the route signature.

# fundamentals/fastapi/02_dependency_injection.md (524 lines)
ORDERING: payoff line 48/524 (0.092, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 0:6 (PASS; 0 markers/6 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with one dependency graph, one route call and exact result/cleanup order, plus linked deferrals for classes, overrides, caching, security, and testing.
FIX-MED: Split the 524-line file after callable/yield dependency fundamentals, moving class dependencies, overrides, testing, and architecture patterns to a named continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about FastAPI resolving a per-request dependency graph and unwinding yielded resources after the response lifecycle.

# fundamentals/fastapi/03_pydantic.md (1289 lines)
ORDERING: payoff line 57/1289 (0.044, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 21:14 (PASS; 21 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: Lines 1, 24, and 53 overstate the model contract: Pydantic does serialize, normal models are mutable unless configured otherwise, `model_construct()` bypasses validation, and required fields need not precede defaulted fields. Replace the absolutes with construction-time guarantees and current field-order behavior; checked 2026-08-17 against https://docs.pydantic.dev/latest/concepts/models/.
FIX-HIGH: Add `## The short version` with one model/input set, exact parsed output and one `ValidationError`, plus linked deferrals for validators, serialization, settings, generics, and FastAPI integration.
FIX-MED: Split the 1,289-line note after BaseModel/Field/validation/serialization essentials, with advanced validators, settings, generics, performance, and migration material in named continuations, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about Pydantic guaranteeing the post-validation output shape at validation boundaries, not perpetual validity of every mutable instance.

# fundamentals/fastapi/04_authentication.md (1185 lines)
ORDERING: payoff line 60/1185 (0.051, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 1:6 (PASS; 1 marker/6 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 2 critical, 1 high, 2 med, 1 low

FIX-CRITICAL: JWT decoders at lines 181, 920, and 1114 pin an algorithm but omit issuer and audience verification; make the runnable baseline validate the expected `iss` and `aud` claims so a valid token minted for another service cannot be accepted.
FIX-CRITICAL: Line 915 keeps expiry-disabled decoding executable even under a `WRONG` label; make the unsafe shape inert and leave only expiry-validating, issuer/audience-validating code runnable.
FIX-HIGH: Add `## The short version` with one credential/token/claim set, a minimal login-plus-protected-route trace and exact 200/401 outputs, plus linked deferrals for refresh, RBAC, cookies, and external identity providers.
FIX-MED: Replace the direct bcrypt baseline with the current FastAPI recommendation based on `pwdlib` and Argon2, while retaining bcrypt only as a labeled compatibility path; checked 2026-08-17 against https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/.
FIX-MED: Split the 1,185-line file after the password/JWT protected-route baseline, moving refresh, RBAC, OAuth providers, cookies, and production operations into named continuations, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about authentication proving identity while authorization separately decides whether that identity may perform an action.

# fundamentals/fastapi/05_middleware.md (1199 lines)
ORDERING: payoff line 49/1199 (0.041, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 25:6 (FAIL; 25 markers/6 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 13; intuition-building explanation yes.
Summary: 0 critical, 1 high, 2 med, 1 low

FIX-HIGH: Add `## The short version` with counted request/middleware inputs, one minimal middleware and exact response/header/log effect, plus linked deferrals for ordering, ASGI, CORS, tracing, rate limiting, and testing.
FIX-MED: Add causal prose before the middleware-order, security, performance, and production prescriptions; 25 markers to 6 explanatory paragraphs leaves 13 rules/defenses without mechanisms and exceeds the 2:1 register contract.
FIX-MED: Split the 1,199-line file after the first function/class middleware lifecycle baseline, moving CORS, ASGI internals, observability, rate limiting, security, and production composition into named continuations, or justify the single-file dependency.
FIX-LOW: Gloss ASGI at first use and add exactly one `> **Key insight**:` about middleware composing around the request/response lifecycle in stack order.

# fundamentals/fastapi/06_websockets.md (1132 lines)
ORDERING: payoff line 75/1132 (0.066, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 19:4 (FAIL; 19 markers/4 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 11; intuition-building explanation yes.
Summary: 1 critical, 1 high, 2 med, 1 low

FIX-CRITICAL: Lines 481–515 make a query-string JWT strategy runnable and line 494 decodes it without issuer/audience validation; replace it with a short-lived one-time ticket or secure cookie baseline, and fully validate claims because URLs are routinely exposed in logs and telemetry.
FIX-HIGH: Add `## The short version` with one connect/message/disconnect sequence, minimal server/client code and exact observable events, plus linked deferrals for authentication, rooms, heartbeats, backpressure, scaling, and testing.
FIX-MED: Add mechanism prose for connection ownership, disconnect cleanup, authentication, broadcast failure, and backpressure; 19 markers to 4 explanatory paragraphs leaves 11 rules/defenses unexplained.
FIX-MED: Split the 1,132-line file after the minimal lifecycle/echo baseline, moving authentication, managers, rooms, Redis scaling, resilience, and operations into named continuations, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about a WebSocket being a long-lived bidirectional connection whose ownership and cleanup outlast a normal request handler.

# fundamentals/fastapi/07_error_handling.md (1061 lines)
ORDERING: payoff line 43/1061 (0.041, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 24:6 (FAIL; 24 markers/6 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 12; intuition-building explanation yes.
Summary: 0 critical, 1 high, 2 med, 1 low

FIX-HIGH: Add `## The short version` with one domain failure, minimal handler registration and exact JSON/status output, plus linked deferrals for validation, logging, correlation IDs, retries, and testing.
FIX-MED: Explain the mechanisms behind exception taxonomy, information disclosure, logging, retryability, and handler ordering; 24 markers to 6 explanatory paragraphs leaves 12 prescriptions without causal support.
FIX-MED: Split the 1,061-line file after the minimal domain-exception/handler baseline, moving validation customization, observability, resilience, security, and production architecture into named continuations, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about translating internal failures into stable public error contracts at one boundary.

# fundamentals/fastapi/08_streaming.md (1014 lines)
ORDERING: payoff line 289/1014 (0.285, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 13:13 (PASS; 13 markers/13 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: Move a complete working streaming response with exact client-visible chunks above line 80; the first end-to-end payoff is deferred to line 289.
FIX-HIGH: Add `## The short version` with one finite generator/endpoint/client trace, exact chunk output and disconnect tell, plus linked deferrals for SSE, files, proxy buffering, cancellation, backpressure, and tests.
FIX-MED: Split the 1,014-line note after a minimal `StreamingResponse`/disconnect baseline, moving SSE, files, external streams, testing, buffering, and production patterns into named continuations, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about streaming transferring ownership to an iterator whose cancellation, cleanup, and pacing remain part of request correctness.

# fundamentals/fastapi/09_background_tasks_and_routers.md (385 lines)
ORDERING: payoff line 32/385 (0.083, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 11:20 (PASS; 11 markers/20 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: Add `## The short version` with one background side effect and one included router, exact response/observable completion, and links to dependency layering, failure handling, queues, and testing.

# fundamentals/fastapi/10_api_design.md (386 lines)
ORDERING: payoff line 21/386 (0.054, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:8 (PASS; 0 markers/8 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with one resource/operation/error set, a minimal endpoint contract and exact request/response, plus linked deferrals for pagination, versioning, idempotency, filtering, and evolution.
FIX-LOW: Add exactly one `> **Key insight**:` about API design making resource semantics and failure behavior stable before implementation details.

# fundamentals/fastapi/11_api_security.md (1161 lines)
ORDERING: payoff line 120/1161 (0.103, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 0:15 (PASS; 0 markers/15 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: Move a complete secure endpoint with an exact accepted/rejected trace above line 80; the first runnable payoff currently arrives at line 120.
FIX-HIGH: Add `## The short version` with one threat/input/defense set, a minimal hardened route and exact 2xx/4xx result, plus linked deferrals for auth, CORS, CSRF, headers, rate limits, secrets, and uploads.
FIX-MED: Split the 1,161-line survey after a minimal threat-model/input-validation/auth baseline, moving browser controls, headers, rate limiting, secrets, uploads, logging, and deployment checks into named continuations, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about security controls being selected from trust boundaries and attacker capabilities, not copied as an undifferentiated checklist.

# fundamentals/fastapi/README.md (98 lines)
ORDERING: n/a — section index, learning map, and decision lookup.
EXPLANATION: n/a — section index, learning map, and decision lookup.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The README routes readers by task and assigns canonical note ownership without becoming a duplicate tutorial.

# fundamentals/fastapi/safe_and_scalable_api_calls/01_core_concepts.md (337 lines)
ORDERING: payoff line 93/337 (0.276, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:1 (PASS; 2 markers/1 explanatory paragraph); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: Move the first complete capacity-control example and exact overload outcome above line 80; the note spends its opening quarter on definitions before delivering a usable baseline.
FIX-HIGH: Add `## The short version` with counted arrival/concurrency/capacity inputs, one minimal limiter and exact admit/reject behavior, plus links to queues, deadlines, retries, and distributed control.
FIX-LOW: Gloss the first specialized term and add exactly one `> **Key insight**:` about admission control bounding work before scarce downstream capacity is consumed.

# fundamentals/fastapi/safe_and_scalable_api_calls/02_concurrency_and_timeouts.md (443 lines)
ORDERING: payoff line 209/443 (0.472, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 7:4 (PASS; 7 markers/4 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 2 high, 0 med, 1 low

FIX-CRITICAL: Lines 3 and 31–70 call client timeouts the only true kill switch and describe `asyncio.timeout()` as merely advisory. Python's timeout context cancels the current task and converts the resulting cancellation into `TimeoutError`, while HTTPX timeouts are phase/inactivity bounds rather than a total deadline; rebuild the hierarchy around explicit total deadlines plus transport phase limits. Checked 2026-08-17 against https://docs.python.org/3/library/asyncio-task.html and https://www.python-httpx.org/advanced/timeouts/.
FIX-HIGH: Move a complete semaphore-plus-total-deadline example and its timeout/overload output above line 80; the first usable composition is at line 209.
FIX-HIGH: Add `## The short version` with counted concurrency/deadline inputs, one minimal bounded call and exact success/timeout outcomes, plus linked deferrals for retry budgets, cancellation cleanup, and transport tuning.
FIX-LOW: Add exactly one `> **Key insight**:` about concurrency limits bounding in-flight work while deadlines bound how long each admitted unit may retain capacity.

# fundamentals/fastapi/safe_and_scalable_api_calls/03_call_patterns.md (610 lines)
ORDERING: payoff line 11/610 (0.018, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 11:2 (FAIL; 11 markers/2 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 7; intuition-building explanation yes.
Summary: 1 critical, 2 high, 2 med, 1 low

FIX-CRITICAL: The “gold-standard” wrapper at lines 86–93 retries a single `asyncio.TimeoutError`, so it retries queue-admission timeouts even though the note later says queue overload is not retryable; use distinct exception types/scopes and retry only eligible downstream attempts.
FIX-HIGH: Lines 215–227 acquire the limiter once in a probe context and then acquire it again for the call, consuming or waiting for two admissions; implement one atomic nonblocking admission operation and hold exactly that permit for the request.
FIX-HIGH: Add `## The short version` with one bounded outbound call, exact success/overload/timeout behavior, and linked deferrals for fallbacks, bulkheads, hedging, and observability.
FIX-MED: Add causal paragraphs for retry eligibility, permit ownership, fallback safety, and overload signaling; 11 markers to 2 explanatory paragraphs leaves 7 rules/defenses unsupported.
FIX-MED: Split the 610-line catalog after one correct bounded-call baseline, moving fallback/hedging/degradation patterns to a named continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about queue admission, execution, and retry being separate phases with separate failure semantics.

# fundamentals/fastapi/safe_and_scalable_api_calls/04_kubernetes.md (554 lines)
ORDERING: payoff line 27/554 (0.049, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 8:2 (FAIL; 8 markers/2 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 4; intuition-building explanation yes.
Summary: 0 critical, 1 high, 2 med, 1 low

FIX-HIGH: Add `## The short version` with counted replicas/worker/concurrency inputs, one deployment/autoscaling calculation and exact readiness/overload signal, plus linked deferrals for probes, disruption, ingress, and observability.
FIX-MED: Add mechanisms before the resource, probe, autoscaling, and shutdown prescriptions; 8 markers to 2 explanatory paragraphs leaves 4 operational rules unexplained.
FIX-MED: Split the 554-line note after the first deployment/resource/probe baseline, moving autoscaling, disruption, ingress, and operations to a named continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about Kubernetes capacity being the product of per-process limits, worker count, replicas, and rollout headroom.

# fundamentals/fastapi/safe_and_scalable_api_calls/05_production_architecture.md (551 lines)
ORDERING: payoff line 405/551 (0.735, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 52:2 (FAIL; 52 markers/2 explanatory paragraphs); restatement FAIL; unglossed first uses 1; unexplained rules/defenses 48; intuition-building explanation yes.
Summary: 2 critical, 3 high, 2 med, 1 low

FIX-CRITICAL: Lines 53–63 put ingress-nginx in the minimal production architecture even though the Kubernetes project retired Ingress-NGINX on 2026-03-24 with no further patches; migrate the baseline to a supported Gateway API implementation. Checked 2026-08-17 against https://kubernetes.io/blog/2025/11/11/ingress-nginx-retirement/ and https://kubernetes.io/blog/2026/01/29/ingress-nginx-statement/.
FIX-CRITICAL: Lines 38–63 present ingress rate limits as cluster-wide, but ingress-nginx annotations apply per controller replica and the effective limit multiplies as replicas scale; remove that guarantee or use a genuinely shared limiter. Checked 2026-08-17 against https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/.
FIX-HIGH: Move a minimal, supported end-to-end architecture with one request trace and overload outcome above line 80; the first complete payoff is deferred to line 405.
FIX-HIGH: Add `## The short version` with counted capacity/rate/deadline inputs, one supported deployment path and exact healthy/overload signals, plus linked deferrals for observability, scaling, and disaster modes.
FIX-HIGH: Add a causal restatement path explaining how each layer changes admission, deadline, retry, and failure propagation; the current configuration/checklist sequence cannot be restated without its tables and snippets.
FIX-MED: Add mechanism paragraphs before the 48 unexplained rules/defenses; the 52:2 register ratio overwhelmingly substitutes prescriptions for explanation.
FIX-MED: Split the 551-line architecture after one minimal supported request path, with scaling/observability/runbook material in a named continuation, or add a concrete length justification.
FIX-LOW: Gloss ASGI at first use and add exactly one `> **Key insight**:` about end-to-end capacity being constrained by the narrowest independently enforced layer.

# fundamentals/fastapi/safe_and_scalable_api_calls/06_advanced_patterns.md (737 lines)
ORDERING: payoff line 36/737 (0.049, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 12:8 (PASS; 12 markers/8 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 2 med, 1 low

FIX-HIGH: Add `## The short version` with one advanced-pattern trigger, minimal implementation and exact degraded/recovered outcome, plus linked deferrals for breakers, hedging, adaptive limits, and load shedding.
FIX-MED: Lines 148–160 say circuit breakers must use Redis/shared state. Scope breaker state to the actual failure domain and dependency partition; process-local, instance-local, or shared state can each be correct, while globally shared state can correlate unrelated failures. Checked 2026-08-17 against https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker.
FIX-MED: Split the 737-line multi-pattern catalog into named owners after the first complete pattern, or add a concrete justification for their required single-file order.
FIX-LOW: Add exactly one `> **Key insight**:` about advanced resilience controls reshaping load and failure propagation, so their scope must match the resource they protect.

# fundamentals/fastapi/safe_and_scalable_api_calls/07_streaming_patterns.md (640 lines)
ORDERING: payoff line 98/640 (0.153, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 1:1 (PASS; 1 marker/1 explanatory paragraph); restatement FAIL; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 1 med, 1 low

FIX-HIGH: Move one complete upstream-to-client streaming trace and exact disconnect/cleanup behavior above line 80 and within the first 15%; the payoff is at line 98.
FIX-HIGH: Add `## The short version` with one finite stream, minimal endpoint/client and exact chunks, plus linked deferrals for SSE, proxying, cancellation, backpressure, and testing.
FIX-HIGH: Add a prose restatement of iterator ownership, cancellation propagation, and resource cleanup; the current example-led path cannot be reconstructed without code.
FIX-MED: Split the 640-line note after the first correct finite/proxied stream baseline, moving SSE, heartbeats, buffering, testing, and production operations to a named continuation, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about cancellation and cleanup propagating across every hop in a streaming pipeline.

# fundamentals/fastapi/safe_and_scalable_api_calls/08_streaming_advanced.md (778 lines)
ORDERING: payoff line 18/778 (0.023, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 1:0 (FAIL; 1 marker/0 explanatory paragraphs); restatement FAIL; unglossed first uses 0; unexplained rules/defenses 1; intuition-building explanation yes.
Summary: 1 critical, 3 high, 2 med, 1 low

FIX-CRITICAL: Lines 716–717 stream `str(e)` to clients from the production endpoint, leaking internal or vendor details; log a correlation-safe internal error and emit a stable public event instead.
FIX-HIGH: Lines 50–64 cancel only pending first-responder tasks; if multiple tasks are already done, completed nonwinners can retain open responses/streams. Select one winner and close/cancel every other result in a `finally` block.
FIX-HIGH: Add `## The short version` with one advanced streaming failure, minimal safe code and exact client events, plus linked deferrals for racing, resume, fan-out, and observability.
FIX-HIGH: Add a code-independent restatement path for winner ownership, cancellation, resume identity, and error disclosure; the note cannot currently be reconstructed without its implementations.
FIX-MED: Add causal prose for the first-responder and production rules; a 1:0 register has one unexplained defense and no explanatory paragraph.
FIX-MED: Split the 778-line note into named pattern owners after one correct advanced baseline, or add a concrete dependency-based length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about advanced stream coordination requiring explicit ownership of every response, task, cursor, and client-visible error.

# fundamentals/fastapi/safe_and_scalable_api_calls/09_distributed_admission_control.md (773 lines)
ORDERING: payoff line 171/773 (0.221, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 19:27 (PASS; 19 markers/27 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 1 med, 1 low

FIX-HIGH: Lines 685–693 recommend Redis `KEYS` for operational inspection; `KEYS` is O(N), marked slow/dangerous, and can block production. Maintain an explicit index or use cursor-based `SCAN`; checked 2026-08-17 against https://redis.io/docs/latest/commands/keys/ and https://redis.io/docs/latest/develop/using-commands/keyspace/.
FIX-HIGH: Move one complete distributed admit/reject trace with exact Redis state/output above line 80; the first operational payoff is at line 171.
FIX-HIGH: Add `## The short version` with counted global quota/instance/request inputs, one atomic limiter and exact admit/reject result, plus linked deferrals for leases, failure policy, fairness, and observability.
FIX-MED: Split the 773-line note after one atomic distributed-limiter baseline, moving algorithms, failure recovery, observability, and operations to named continuations, or add a concrete length justification.
FIX-LOW: Add exactly one `> **Key insight**:` about distributed admission requiring one atomic shared decision plus an explicit policy for shared-store failure.

# fundamentals/fastapi/safe_and_scalable_api_calls/10_llm_token_economics.md (471 lines)
ORDERING: payoff line 118/471 (0.251, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 1:12 (PASS; 1 marker/12 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 2 high, 0 med, 1 low

FIX-CRITICAL: Lines 29, 49–56, and 183–202 identify that failed calls may consume provider tokens but then fully refund every failed reservation, enabling quota evasion and under-accounting. Reconcile with provider usage when available or conservatively charge an explicit failure reservation; never blindly full-refund an unknown-cost attempt.
FIX-HIGH: Move the first complete reserve-call-reconcile trace with exact token balances above line 80; the operational payoff is at line 118.
FIX-HIGH: Add `## The short version` with counted token/cost/quota inputs, one reservation/reconciliation sequence and exact balances, plus linked deferrals for streaming, pricing tables, and distributed ledgers.
FIX-LOW: Add exactly one `> **Key insight**:` about token admission reserving an upper bound before work and reconciling actual billable usage afterward.

# fundamentals/fastapi/safe_and_scalable_api_calls/11_idempotency.md (360 lines)
ORDERING: payoff line 55/360 (0.153, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:7 (PASS; 0 markers/7 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: Move the complete idempotency-key replay result slightly earlier so it lands within the first 15%; its current payoff is line 55/360 (0.153).
FIX-HIGH: Add `## The short version` with one key/request/result set, exact first-call/replay/conflict outputs, and linked deferrals for persistence, expiry, concurrency, and downstream effects.
FIX-LOW: Add exactly one `> **Key insight**:` about idempotency binding one stable operation identity to one committed outcome across retries.

# fundamentals/fastapi/safe_and_scalable_api_calls/README.md (200 lines)
ORDERING: payoff line 61/200 (0.305, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 8:1 (FAIL; 8 markers/1 explanatory paragraph); restatement PASS; unglossed first uses 0; unexplained rules/defenses 6; intuition-building explanation yes.
Summary: 1 critical, 2 high, 1 med, 1 low

FIX-CRITICAL: The quickstart at lines 94–98 retries the first `asyncio.TimeoutError`, including possible queue-admission overload, contradicting line 110 and amplifying pressure; separate admission from downstream attempt timeouts and retry only eligible failures.
FIX-HIGH: Move the first complete bounded-call result above line 80; this teaching README's payoff is at line 61 by ratio but its actual call/retry behavior is not complete until later.
FIX-HIGH: Add the exact `## The short version` contract with counted limiter/timeout/retry inputs, one safe call and exact success/overload outputs, plus links to the numbered deep dives.
FIX-MED: Add causal prose for the six unexplained operational rules; the 8:1 register ratio exceeds the 2:1 explanation contract.
FIX-LOW: Add exactly one `> **Key insight**:` about admitting work before execution and keeping overload distinct from retryable dependency failure.

# fundamentals/httpx/01_mental_model.md (246 lines)
ORDERING: payoff line 17/246 (0.069, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:0 (PASS; 0 markers/0 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with one client/request/response lifecycle, exact output and closure tell, plus linked deferrals for pooling, timeouts, transports, and aiohttp comparison.
FIX-LOW: Add exactly one `> **Key insight**:` about the client owning reusable connection and configuration state across otherwise independent requests.

# fundamentals/httpx/02_connection_pooling.md (347 lines)
ORDERING: payoff line 9/347 (0.026, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 4:2 (PASS; 4 markers/2 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with counted pool/load inputs, one limits configuration and exact wait/timeout/reuse behavior, plus linked deferrals for sizing, per-host isolation, and observability.
FIX-MED: Line 88 calls `max_keepalive_connections` a “floor during idle”; it is a maximum/ceiling on allowable keep-alive connections. Correct the comparison; checked 2026-08-17 against https://www.python-httpx.org/advanced/resource-limits/.
FIX-LOW: Add exactly one `> **Key insight**:` about pool limits bounding sockets while a separate application limiter bounds admitted coroutines.

# fundamentals/httpx/03_timeouts.md (410 lines)
ORDERING: payoff line 9/410 (0.022, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 3:1 (FAIL; 3 markers/1 explanatory paragraph); restatement PASS; unglossed first uses 0; unexplained rules/defenses 1; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: Lines 164–168 say a read timeout does not cover server processing before the first byte. HTTPX defines it as the maximum wait to receive a chunk, so it also bounds waiting for the first response bytes; distinguish inactivity from a total end-to-end deadline. Checked 2026-08-17 against https://www.python-httpx.org/advanced/timeouts/.
FIX-HIGH: Add `## The short version` with one connect/read/write/pool configuration, exact phase failure types, and linked deferrals for total deadlines, streaming, retries, and metrics.
FIX-MED: Add causal prose for the timeout prescription left unsupported by the 3:1 register ratio, especially how phase timers interact with a total application deadline.
FIX-LOW: Add exactly one `> **Key insight**:` about HTTPX timeouts bounding distinct I/O phases and inactivity, not imposing one total request budget.

# fundamentals/httpx/04_advanced.md (494 lines)
ORDERING: payoff line 33/494 (0.067, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:4 (PASS; 0 markers/4 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 1 high, 0 med, 1 low

FIX-CRITICAL: Line 422 contains executable `verify=False` even though it is labeled “never in production”; remove the runnable insecure shape and keep only inert warning text beside a runnable verified `SSLContext` example.
FIX-HIGH: Add `## The short version` with one advanced client customization, exact request/response effect, and linked deferrals for transports, hooks, proxies, TLS, and testing.
FIX-LOW: Add exactly one `> **Key insight**:` about advanced HTTPX behavior being composed at the client/transport boundary while preserving verification, ownership, and cleanup invariants.

# fundamentals/httpx/05_httpx_vs_aiohttp.md (317 lines)
ORDERING: payoff line 21/317 (0.066, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 20:1 (FAIL; 20 markers/1 explanatory paragraph); restatement PASS; unglossed first uses 0; unexplained rules/defenses 18; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: Line 51 says aiohttp `sock_read` does not reset per chunk, but current aiohttp defines it as the maximum interval between reading new data portions; correct the comparison and version-scope it. Checked 2026-08-17 against https://docs.aiohttp.org/en/stable/client_reference.html.
FIX-HIGH: Add `## The short version` with one equivalent request in both libraries, exact lifecycle/timeout differences, and linked deferrals for streaming, transports, WebSockets, and selection criteria.
FIX-MED: Replace checklist/table-only assertions with causal comparison prose; 20 markers to 1 explanatory paragraph leaves 18 rules/defenses without mechanisms.
FIX-LOW: Add exactly one `> **Key insight**:` about choosing between clients by required protocol/lifecycle features and verified current behavior, not brand-level preference.

# fundamentals/httpx/README.md (70 lines)
ORDERING: n/a — section index, learning map, and decision lookup.
EXPLANATION: n/a — section index, learning map, and decision lookup.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The README provides a compact sequence and decision routes while leaving explanations to the canonical notes.

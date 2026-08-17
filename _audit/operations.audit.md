# operations/README.md (25 lines)
ORDERING: n/a (pure collection index; no teaching sequence).
EXPLANATION: n/a (pure collection index; no central mechanism to restate).
Summary: 0 critical, 0 high, 0 med, 2 low

FIX-LOW: The `pytest-8.x` badge at line 5 is stale now that pytest 9.1.1 is released — update the badge or remove version-bearing badges from this index; https://docs.pytest.org/en/stable/announce/index.html (checked 2026-08-17).
FIX-LOW: The `Gunicorn-22.x` badge at line 8 is stale now that Gunicorn 26.0.0 is current — update the badge or make it version-neutral; https://pypi.org/project/gunicorn/ (checked 2026-08-17).

# operations/deployment/README.md (18 lines)
ORDERING: n/a (pure one-file directory index; no teaching sequence).
EXPLANATION: n/a (pure one-file directory index; no central mechanism to restate).
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index states its scope, names the sole note clearly, and keeps prerequisites concise.

# operations/deployment/docker_and_deployment.md (1322 lines)
ORDERING: payoff line 35/1322 (0.026, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 30:70 (PASS; 30 markers/70 explanatory paragraphs); restatement PASS; unglossed first uses 7; unexplained rules/defenses 16; intuition-building explanation yes.
Summary: 0 critical, 5 high, 5 med, 0 low

FIX-HIGH: The note has no `## The short version` before section 1 — add the required problem/mental model, counted inputs, a 10–25-line runnable container baseline, exact `docker build`/`docker run` success signals, and linked deferrals for non-root execution, health checks, shutdown, dependency locking, secrets, and orchestration.
FIX-HIGH: The readiness implementation at lines 448–476 awaits the database and Redis without deadlines, so a stalled dependency can make `/ready` hang instead of promptly removing the instance from traffic — bound each check with a short timeout and show both the healthy response and the timed-out `503` response.
FIX-HIGH: Lines 92–104 overstate the container-root threat model and prescribe non-root execution without an attacker sequence — explain that container root is namespaced rather than automatically host root, then walk through the capability/runtime escape or writable-mount path whose impact a non-root UID reduces.
FIX-HIGH: Gloss `ASGI` (line 16), PEP/musllinux (line 88), TCP backlog (line 136), PID 1 (line 594), load-balancer draining (line 1247), KEDA (line 1270), and OOM-killed (line 1260) at first prose use so a backend engineer new to deployment does not need external vocabulary lookup.
FIX-HIGH: The 16 `❌`/`✅` conclusions in `## 11. Common Mistakes` (lines 888–987) appear before a local causal explanation — put the failure mechanism before each retained pair or replace duplicated pairs with links to the earlier sections that already earn the rule.
FIX-MED: The file is 1322 lines with no `<!-- length-justification: ... -->` and shifts from a container tutorial into a Kubernetes mini-guide after its summary — split at `## Kubernetes Essentials for Python Services`, and separate the baseline Docker path from the production reference unless a concrete near-top justification explains why one file must own both.
FIX-MED: `await app.state.redis.close()` at line 572 calls an API deprecated since redis-py 5.0.1 — use `await app.state.redis.aclose()` in the copied shutdown path; https://redis.readthedocs.io/en/stable/_modules/redis/asyncio/client.html (checked 2026-08-17).
FIX-MED: Both production uv Dockerfiles copy `ghcr.io/astral-sh/uv:latest` at lines 789 and 1069, defeating the guide's reproducibility claim — pin a specific uv version and, for a supply-chain-hardened example, an image digest as Astral recommends; https://docs.astral.sh/uv/guides/integration/docker/ (checked 2026-08-17).
FIX-MED: Lines 1244–1247 say readiness must start failing before `SIGTERM` and prescribe a sleeping `preStop` hook, but current Kubernetes marks terminating endpoints `ready=false` as part of Pod termination — describe the actual EndpointSlice termination flow, then reserve an explicit drain endpoint/hook for load balancers that need additional propagation time; https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/ (checked 2026-08-17).
FIX-MED: Line 1310 says HPA cannot scale to zero, but current Kubernetes permits `minReplicas: 0` behind the `HPAScaleToZero` alpha gate with Object or External metrics — qualify the default limitation and retain KEDA as the mature event-driven option; https://kubernetes.io/docs/reference/kubernetes-api/autoscaling/horizontal-pod-autoscaler-v2/ (checked 2026-08-17).

# operations/testing/README.md (123 lines)
ORDERING: payoff line 79/123 (0.642, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:4 (PASS; 0 markers/4 explanatory paragraphs); restatement FAIL; unglossed first uses 3; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 0 med, 2 low

FIX-HIGH: The quick start begins at line 79 and there is no `## The short version` — move a self-contained baseline above prerequisites with a counted list covering the app, `/health` route, dependencies, and `asyncio_mode`, then add exact passing output and linked deferrals for lifespan, database isolation, and dependency overrides.
FIX-HIGH: The prose outside code and tables never explains why `ASGITransport` reaches the app in-process or why global dependency overrides must be cleared, so the completed note fails restatement — add the request path and shared-state consequence in causal prose next to the quick start.
FIX-HIGH: Expand and gloss `ASGI` (line 31), `DI` (line 32), and `E2E` (line 112) at first prose use.
FIX-LOW: The `pytest-8.x` badge at line 5 is stale now that pytest 9.1.1 is released — update it or remove the version from this navigational page; https://docs.pytest.org/en/stable/announce/index.html (checked 2026-08-17).
FIX-LOW: Add one transferable `> **Key insight**:` about test layers buying different kinds of confidence rather than repeating a section label.

# operations/testing/01_mental_model.md (135 lines)
ORDERING: payoff line 102/135 (0.756, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:9 (PASS; 0 markers/9 explanatory paragraphs); restatement PASS; unglossed first uses 5; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: The first concrete trace starts at line 102 and the note lacks `## The short version` — open with a counted AAA worked example using the named user/cart values, the observed `90` result, and links deferring the pyramid, doubles, and FIRST principles.
FIX-HIGH: Expand and gloss `CI` (line 21), `E2E` (line 49), `ASGI` (line 60), `AAA` (line 98), and `FIRST` (line 119) at first prose use.
FIX-MED: The rule of thumb at line 63 equates network use or a one-second runtime with integration testing, which teaches the wrong classification boundary — define the level by the real boundary/components exercised, then describe speed and network access as common consequences rather than the definition.
FIX-LOW: Add one `> **Key insight**:` that transfers beyond this example, such as choosing the lowest test layer that can observe the failure being protected against.

# operations/testing/02_setup.md (132 lines)
ORDERING: payoff line 107/132 (0.811, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:4 (PASS; 0 markers/4 explanatory paragraphs); restatement PASS; unglossed first uses 3; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 0 med, 1 low

FIX-HIGH: The first end-to-end sanity check starts at line 107 and no short-version contract exists — put a counted install/config/test baseline first, state the exact three passing test names, and link the currently front-loaded plugins and layout options as deferrals.
FIX-HIGH: The eight-command enumeration under `## Running Tests` (lines 90–99) has no marked entry subset — identify the two or three commands a beginner should use first and show one of those in the sanity check.
FIX-HIGH: Gloss `respx` (line 10), `CI` (line 16), and `ASGI` (line 45) at first prose use instead of leaving package names and acronyms to the later notes.
FIX-LOW: Add a `> **Key insight**:` explaining that separating fast and integration suites is useful only when each command gives a deliberate feedback-time boundary.

# operations/testing/03_unit_testing.md (339 lines)
ORDERING: payoff line 30/339 (0.088, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:22 (PASS; 2 markers/22 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 2; intuition-building explanation yes.
Summary: 0 critical, 4 high, 0 med, 1 low

FIX-HIGH: Add the missing `## The short version` with the pure-function test as a runnable baseline, a counted input list, exact pytest output, and linked deferrals for doubles, patching, exceptions, and Hypothesis.
FIX-HIGH: The six-row `What to Unit-Test` table at lines 11–18 has no marked starter subset — mark pure functions, validators, and service methods as the first defaults and use the pure-function row in the baseline.
FIX-HIGH: The `❌`/`✅` patch pair and rule at lines 245–255 never explain Python's bound module name mechanism — show that `users.py` holds its own reference after import and why replacing only the defining module's attribute leaves that reference unchanged.
FIX-HIGH: Expand `ASGI` at its first use on line 3.
FIX-LOW: Add a transferable `> **Key insight**:` that unit-test value comes from narrowing the causal search space, not merely from avoiding I/O.

# operations/testing/04_endpoint_testing.md (207 lines)
ORDERING: payoff line 27/207 (0.130, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 6:11 (PASS; 6 markers/11 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` using one client path, a counted app/config dependency list, exact response output, and explicit links deferring lifespan, WebSockets, real-server tests, and client selection.
FIX-HIGH: Expand `ASGI` at line 3 and gloss it as the callable application interface before using `ASGITransport` in the decision table.
FIX-LOW: Add one `> **Key insight**:` that in-process HTTP tests exercise protocol/application wiring but not the production network stack.

# operations/testing/05_dependency_overrides.md (257 lines)
ORDERING: payoff line 108/257 (0.420, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 6:17 (PASS; 6 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 2 high, 0 med, 1 low

FIX-CRITICAL: The module-level DB override installed at line 70 is erased permanently by the autouse cleanup at lines 171–175 after the first test, so later tests can silently fall back to the production dependency — install the override inside a per-test fixture before `yield` and restore the prior mapping in `finally` rather than relying on one import-time assignment.
FIX-HIGH: The note has no short-version contract and its first observable override test begins at line 108 — open with a counted per-test auth override, exact `200`/`403` success signals, and links deferring database sessions, nesting, and non-DI dependencies.
FIX-HIGH: Expand `DI` at line 3 and gloss it as FastAPI's dependency-injection resolution mechanism.
FIX-LOW: Add a `> **Key insight**:` explaining that an override changes the dependency resolver's callable mapping, not the implementation object everywhere in the process.

# operations/testing/06_async_testing.md (202 lines)
ORDERING: payoff line 11/202 (0.054, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 4:15 (PASS; 4 markers/15 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with a counted plugin/config/test baseline, exact passing output plus the unawaited-coroutine failure tell, and links deferring fixture loop scope, cancellation, background tasks, AnyIO, and flake diagnosis.
FIX-LOW: Add one `> **Key insight**:` that an async test is correct only when pytest owns and awaits the coroutine on the intended loop.

# operations/testing/07_fixtures.md (268 lines)
ORDERING: payoff line 126/268 (0.470, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:16 (PASS; 0 markers/16 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: The first composed fixture-to-test outcome starts at line 126 and there is no short version — put one counted client fixture plus one passing endpoint test first, state the exact result, and link scopes, factories, authentication, parameterization, and built-ins as deferrals.
FIX-HIGH: Expand `DI` at line 166 before using dependency overrides as the authentication-fixture mechanism.
FIX-LOW: Add a `> **Key insight**:` that fixture scope is an ownership/lifetime decision and must not outlive the state-isolation boundary.

# operations/testing/08_database_testing.md (304 lines)
ORDERING: payoff line 216/304 (0.711, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 0:23 (PASS; 0 markers/23 explanatory paragraphs); restatement PASS; unglossed first uses 4; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 4 high, 0 med, 1 low

FIX-HIGH: The first database assertion with visible output starts at line 216 and no short version exists — open with a counted real-Postgres transaction fixture plus `SELECT 1`/row-round-trip test, then link container startup, async sessions, seeding, mocks, and migrations as deferrals.
FIX-HIGH: The six-row strategy table at lines 13–20 is not visually navigable despite transaction rollback being the prose default — mark transaction rollback plus real Postgres as the default path and show it in the baseline before alternatives.
FIX-HIGH: Strategy 1 at lines 40–69 keeps one SQLite database for the module and merely rolls back each session after application code may already have committed, so copied tests can leak rows between cases — either label it explicitly non-isolated and restrict it to non-committing code or wrap every request in an outer transaction/savepoint as Strategy 2 does.
FIX-HIGH: Gloss `CI` (line 28), `JSONB` and `CTE` (line 22), and `SAVEPOINT` (line 101) at first use with the kind of database feature or transaction boundary each names.
FIX-LOW: Add a `> **Key insight**:` explaining that database-test fidelity and reset strategy are independent choices: use the production dialect while isolating state per test.

# operations/testing/09_mocking_external.md (285 lines)
ORDERING: payoff line 37/285 (0.130, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:17 (PASS; 2 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 2; intuition-building explanation yes.
Summary: 0 critical, 4 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` with a counted `respx` baseline, exact returned value and matched-call signal, and linked deferrals for injected mocks, patching, AWS, real contracts, and layered tests.
FIX-HIGH: The `AsyncMock` example at lines 119–128 calls the mock directly and therefore tests only the value the test configured — call a real application function that accepts the mock as its boundary and assert both the application's returned behavior and the boundary interaction.
FIX-HIGH: The patch `❌`/`✅` pair at lines 164–174 states the import-path rule without explaining bound names — walk through which object `users.py` resolves at call time and why changing the defining module's attribute does not replace that local reference.
FIX-HIGH: Expand `DI` (line 23) and `SDK` (line 203) at first prose use.
FIX-LOW: Add a `> **Key insight**:` that the correct mock boundary is the first interface you do not own, while a real contract test checks whether your model of that interface still matches reality.

# operations/testing/10_test_patterns.md (357 lines)
ORDERING: payoff line 11/357 (0.031, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 4:25 (PASS; 4 markers/25 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 1 low

FIX-HIGH: Add `## The short version` around one happy-path/error-path pair with counted fixtures and inputs, exact pytest output, and links deferring parametrization, snapshots, organization, and the full integration example.
FIX-HIGH: The snapshot examples at lines 193–216 use a synchronous `def` and un-awaited `client.get(...)` even though this collection's canonical client fixture is `httpx.AsyncClient`, and `/users/42` is not seeded — make the tests async, await the request, create the user fixture first, and show the initial snapshot plus subsequent passing output.
FIX-LOW: Add a `> **Key insight**:` that durable tests assert externally meaningful state transitions, while parametrization and snapshots are only compression tools for those contracts.

# operations/testing/11_coverage_and_ci.md (255 lines)
ORDERING: payoff line 15/255 (0.059, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:18 (PASS; 0 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 1 med, 2 low

FIX-HIGH: Add `## The short version` with counted coverage/CI inputs, a runnable command and minimal workflow, the exact terminal/required-check success signals, and links deferring targets, parallelism, pre-commit, flake detection, and speed budgets.
FIX-MED: Line 102 recommends adding `omit` entries when low-value production code lowers coverage, which can make the metric look healthier without increasing confidence — reserve `omit` for generated or intentionally non-executable code and explain that low-value glue should instead be accepted in the threshold or covered through a higher-level test.
FIX-LOW: Update `actions/checkout@v5` at line 153 to the `@v6` major shown in GitHub's current official Python workflow; https://docs.github.com/en/actions/tutorials/build-and-test-code/python (checked 2026-08-17).
FIX-LOW: Add a `> **Key insight**:` that coverage locates unobserved execution paths but cannot establish whether assertions protect the right behavior.

# operations/testing/12_common_mistakes.md (277 lines)
ORDERING: payoff line 9/277 (0.032, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 24:14 (PASS; 24 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 24; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with a counted one-test isolation failure/fix, exact order-dependent failure and passing signals, and links deferring the remaining mistake catalog.
FIX-HIGH: All 24 `❌`/`✅` markers lead their local mechanism instead of following it — add one causal sentence before each bad/good pair describing the state, resolution, or import behavior that produces the failure, then keep the concrete pair as evidence.
FIX-MED: Lines 238–245 say a flaky test should be fixed or deleted, which can erase protection for a real intermittent failure — distinguish invalid/redundant tests from valuable flaky coverage and give the latter a quarantine marker, owner, tracked issue, and re-enable deadline.
FIX-LOW: Add one `> **Key insight**:` that most suite flakes are state-lifetime or boundary errors, so the observed symptom should lead back to the owner of that state.

# operations/testing/13_testing_llm_code.md (410 lines)
ORDERING: payoff line 48/410 (0.117, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 0:39 (PASS; 0 markers/39 explanatory paragraphs); restatement PASS; unglossed first uses 4; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 4 high, 1 med, 1 low

FIX-HIGH: Add `## The short version` with counted prompt-builder/model-adapter inputs, the deterministic unit test as runnable code, exact pytest output, and links deferring provider failures, fake tools, live evals, snapshots, cost, and model upgrades.
FIX-HIGH: Expand and gloss `LLM` and `eval` at line 3, `CI` at line 16, and `SDK` at line 146 before relying on those terms throughout the note.
FIX-HIGH: The live eval at lines 304–333 makes one pass over only three examples and treats `accuracy >= 0.90` as stable evidence, so one model variation flips the entire result — label a true minimal demonstration, then add the production continuation: representative sample sizing, repeated runs or uncertainty bounds, stored per-case results, and a budget-limited regression gate.
FIX-HIGH: The adapter at lines 175–185 returns `response.output_parsed` unconditionally even though the note later names safety refusal and malformed/incomplete output as real failures — handle refusal/incomplete responses explicitly and test the observable application error before presenting this as the provider-adapter pattern.
FIX-MED: Line 342 says OpenAI's Evals platform is deprecated with 2026 shutdown dates, but current official documentation exposes active Evals guides and `/v1/evals` API operations — remove the unsupported shutdown claim or name the exact legacy surface and dates while distinguishing it from the current Evals API; https://developers.openai.com/api/reference/resources/evals/methods/delete (checked 2026-08-17).
FIX-LOW: Add a `> **Key insight**:` that deterministic tests protect the software contract around a model, while evals estimate behavior quality over a dataset rather than proving a single output.

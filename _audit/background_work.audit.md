# background_work/01_overview.md (125 lines)
ORDERING: payoff line 52/125 (0.416, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:12 (PASS; 2 markers/12 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The first complete three-state worked trace is buried at line 52 and there is no `## The short version` — add a <=40-line entry point before section 1 with the problem/mental model, a counted input list, the trace, its observable success signal, and linked delivery/execution/workflow deferrals.

# background_work/02_when_a_task_becomes_a_workflow.md (160 lines)
ORDERING: payoff line 15/160 (0.094, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 3:16 (PASS; 3 markers/16 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that states the decision problem, counts the required decision inputs, reuses the restart trace, names the visible decision outcome, and links deferred modeling/versioning concerns.

# background_work/03_minimal_durable_task.md (247 lines)
ORDERING: payoff line 15/247 (0.061, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 3:24 (PASS; 3 markers/24 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that bounds the job row/request key/input reference, shows one complete submit-to-result trace, gives the exact status/result success signal, and links lease, retry, idempotency, and polling omissions.

# background_work/03_state_machine_design.md (156 lines)
ORDERING: payoff line 30/156 (0.192, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 3:17 (PASS; 3 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The concrete `approve` outcome begins only at line 30 and the note lacks `## The short version` — move the prerequisite below a <=40-line block that counts the three axes, works the named transition through all three, states the zero/one-row success signal, and links advanced alternatives.

# background_work/04_queue_and_worker_architectures.md (217 lines)
ORDERING: payoff line 46/217 (0.212, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 5:33 (PASS; 5 markers/33 explanatory paragraphs); restatement PASS; unglossed first uses 3; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The first complete `job-55` handoff starts at line 46 and there is no `## The short version` — add a <=40-line block before the prerequisite with a counted input list, one database-polling baseline, an oldest-ready/claim success signal, and links to broker, managed-queue, engine, and choreography deferrals.
FIX-HIGH: First uses of `CTE` (line 84), `DLQ` (line 115), and `FIFO` (line 136) are not expanded — add local glosses for common table expression, dead-letter queue, and first-in/first-out at those first prose uses.

# background_work/05_task_execution_models.md (356 lines)
ORDERING: payoff line 52/356 (0.146, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 6:27 (PASS; 6 markers/27 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts workload/resource inputs, runs one bounded representative workload, states the throughput/saturation success signal, and links pool-specific hardening.
FIX-HIGH: `GIL` at line 44 and `OOM` at line 98 appear without expansion — gloss them at first use as the Global Interpreter Lock and out-of-memory termination so the execution mechanism and its failure tell do not depend on Python-runtime shorthand.

# background_work/06_scheduling_and_periodic_work.md (211 lines)
ORDERING: payoff line 15/211 (0.071, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:20 (PASS; 2 markers/20 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts schedule/rule/zone inputs, traces one logical occurrence into one durable job, gives the unique-row success signal, and links DST, misfire, catch-up, and overlap deferrals.
FIX-HIGH: `DST` at line 33 and `IANA` at line 46 are unexpanded first uses — add inline expansions for daylight-saving time and the Internet Assigned Numbers Authority timezone database naming convention.

# background_work/07_durable_fanout_and_join.md (274 lines)
ORDERING: payoff line 27/274 (0.099, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 1:16 (PASS; 1 marker/16 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move prerequisites below a <=40-line block that counts group/item/operation-key inputs, uses the three-child duplicate/concurrent-completion trace, states the one-aggregate success signal, and links bounds, failure policy, and concurrency hardening.

# background_work/08_failure_injection_and_testing.md (348 lines)
ORDERING: payoff line 69/348 (0.198, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:18 (PASS; 2 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 3; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The first runnable race test begins at line 69 and there is no `## The short version` — move the prerequisite below a <=40-line block that counts database/fixture/barrier inputs, runs one claim race, gives the one-winner/stale-token success signal, and links the remaining failure matrix.
FIX-HIGH: `CAS`, `CTE`, and `DLQ` first appear unexpanded in the layer table at lines 34–36 — expand compare-and-set, common table expression, and dead-letter queue in that table.

# background_work/09_decision_guide.md (205 lines)
ORDERING: payoff line 13/205 (0.063, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:28 (PASS; 2 markers/28 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts the four decision inputs, works one compact workload through them, names the chosen ownership/delivery/execution tuple, and links production validation.
FIX-HIGH: `DLQ` at line 102 and `GIL` at line 127 are unexpanded first uses — gloss dead-letter queue and Global Interpreter Lock locally rather than relying on framework notes.

# background_work/README.md (113 lines)
ORDERING: n/a — collection index and reading-path router, not a teaching sequence.
EXPLANATION: n/a — collection index and reading-path router, not a teaching note.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index marks default routes, audiences, outcomes, branch points, and stop conditions without duplicating the owned implementations.

# background_work/frameworks/00_workflow_orchestrator_selection.md (201 lines)
ORDERING: payoff line 15/201 (0.075, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:19 (PASS; 2 markers/19 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts coordination/ownership/effect inputs, applies them to one custom-versus-engine trace, gives the one-authority success signal, and links product-specific limits.
FIX-HIGH: `DAG` at line 82 and `SQS` at line 106 are unexpanded first uses — gloss directed acyclic graph and Amazon Simple Queue Service at those locations.

# background_work/frameworks/README.md (45 lines)
ORDERING: n/a — framework index and role router.
EXPLANATION: n/a — framework index and role router.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index distinguishes schedulers, task runtimes, data orchestrators, workflow engines, and checkpointed graphs and marks the default entry condition.

# background_work/frameworks/airflow/README.md (27 lines)
ORDERING: n/a — one-entry framework index.
EXPLANATION: n/a — one-entry framework index.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index states scope, prerequisite route, and the owned overview without duplicating its content.

# background_work/frameworks/airflow/overview.md (443 lines)
ORDERING: payoff line 93/443 (0.210, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 8:31 (PASS; 8 markers/31 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The first runnable Task SDK DAG starts at line 93 and the note lacks `## The short version` — move the prerequisite/current-version notice below a <=40-line block that counts file/runtime inputs, includes the two-task DAG, gives the parsed-DAG/task-order success signal, and links scheduling, executor, API, and production omissions.
FIX-HIGH: `Task SDK` and `DAG` are used at line 7 before `DAG` is expanded at line 73 — gloss the software development kit and directed acyclic graph at their first prose occurrence.

# background_work/frameworks/apscheduler/README.md (26 lines)
ORDERING: n/a — one-entry framework index.
EXPLANATION: n/a — one-entry framework index.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index states scope and directs readers through the required architecture notes before the overview.

# background_work/frameworks/apscheduler/overview.md (937 lines)
ORDERING: payoff line 154/937 (0.164, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 17:45 (PASS; 17 markers/45 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 0 low

FIX-HIGH: The first runnable scheduler is buried at line 154 and there is no `## The short version` — add a <=40-line entry point before the prerequisite that counts callable/schedule/timezone inputs, runs one interval job, gives the firing log and silent-failure tell, and links persistence, replica, locking, and durable-job deferrals.
FIX-HIGH: `DST` first appears unexpanded at line 67 — spell out daylight-saving time before describing its missing/repeated wall-clock behavior.
FIX-MED: The 937-line tutorial/reference collision has no `<!-- length-justification: ... -->` — split after the local single-process baseline into a production/distributed-operations note, or record why one file is necessary and add `Core`, `Production`, and `Edge case` skip markers.

# background_work/frameworks/celery/README.md (28 lines)
ORDERING: n/a — one-entry framework index.
EXPLANATION: n/a — one-entry framework index.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index gives a clear prerequisite and decision route before the implementation overview.

# background_work/frameworks/celery/overview.md (522 lines)
ORDERING: payoff line 57/522 (0.109, PASS); short version FAIL; length budget FAIL.
EXPLANATION: register 11:36 (PASS; 11 markers/36 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 0 low

FIX-HIGH: The note has no `## The short version` — move prerequisites and the version notice below a <=40-line block that counts broker/module/task inputs, runs the `add` task, gives the exact `5` plus worker-log success signal, and links domain-state, acknowledgement, retry, routing, scheduling, and outbox deferrals.
FIX-HIGH: `SMTP` at line 13 and `GIL` at line 212 are unexpanded first uses — add local expansions for Simple Mail Transfer Protocol and Global Interpreter Lock.
FIX-MED: The 522-line note has no length justification and mixes first-task tutorial, runtime reference, scheduling, security, and testing — split after the hardened task/runtime model into an operations reference, or document why one file must own all sections and add altitude markers.

# background_work/frameworks/dramatiq/README.md (27 lines)
ORDERING: n/a — two-entry framework index.
EXPLANATION: n/a — two-entry framework index.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index preserves the overview-before-integration dependency and points to the reliability prerequisites.

# background_work/frameworks/dramatiq/fastapi_integration.md (1105 lines)
ORDERING: payoff line 770/1105 (0.697, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 20:48 (PASS; 20 markers/48 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 3 high, 1 med, 0 low

FIX-HIGH: The first assembled API/worker deployment arrives at line 770 and there is no `## The short version` — add a <=40-line entry point before prerequisites that bounds the required services/files, composes one canonical durable endpoint/outbox/publisher/claiming actor path, gives row/log/result success signals, and links context, async, testing, health, and scaling deferrals.
FIX-HIGH: The explicitly broken baseline at line 216 performs an unconditional status update and a database/broker dual write before the correct protocol appears — replace it with the smallest correct database-polled job baseline, then introduce the broker/outbox and fenced actor as hardening; a “do not ship” label does not make the first implementation safe to learn from.
FIX-HIGH: `ACL` at line 84 and `GIL` at line 908 are unexpanded first uses — gloss access-control list and Global Interpreter Lock locally.
FIX-MED: The 1,105-line tutorial/reference collision has no length justification — split the canonical durable FastAPI integration from context propagation, tests, container operations, health, and scaling, with an explicit continuation boundary and stop point.

# background_work/frameworks/dramatiq/overview.md (1148 lines)
ORDERING: payoff line 709/1148 (0.618, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 21:55 (PASS; 21 markers/55 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 1 critical, 3 high, 1 med, 0 low

FIX-CRITICAL: The runnable RabbitMQ configuration at line 114 embeds the valid default credential `guest:guest` — replace it with an unmistakable environment-supplied placeholder and a local setup instruction; the later “never ship” warning does not make credential-bearing example code safe.
FIX-HIGH: Actor, send, and worker startup are not composed until line 709 and there is no `## The short version` — add a <=40-line runnable local task before the reference material with counted broker/module inputs, exact worker and send commands, success/failure logs, and linked retry/result/security deferrals.
FIX-HIGH: The first `send_email` actor at lines 131–156 performs a retryable external effect without a stable operation key or nearby deferral contract — make the baseline effect idempotent, or use a harmless deterministic task until the later idempotency mechanism is in place.
FIX-HIGH: `GIL` at line 780 and `WSGI` at line 812 are unexpanded first uses — gloss Global Interpreter Lock and Web Server Gateway Interface at those locations.
FIX-MED: The 1,148-line file has no length justification and gives installation, API reference, composition, middleware, operations, security, and product comparison equal weight — split the first runnable model from the operational/reference material and add altitude/stop-point markers.

# background_work/frameworks/langgraph/README.md (25 lines)
ORDERING: n/a — one-entry framework index.
EXPLANATION: n/a — one-entry framework index.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index states the graph-specific scope and prerequisite without duplicating the overview.

# background_work/frameworks/langgraph/overview.md (173 lines)
ORDERING: payoff line 32/173 (0.185, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:14 (PASS; 2 markers/14 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The runnable interrupt/resume graph starts at line 32 and there is no `## The short version` — move the prerequisite below a <=40-line block that counts graph/checkpointer/thread inputs, includes the minimal graph, gives the `__interrupt__`/resumed-artifact signal, and links durable storage, replay, and migration omissions.

# background_work/frameworks/temporal/README.md (26 lines)
ORDERING: n/a — one-entry framework index.
EXPLANATION: n/a — one-entry framework index.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index states the engine scope and prerequisite path cleanly.

# background_work/frameworks/temporal/overview.md (173 lines)
ORDERING: payoff line 50/173 (0.289, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:10 (PASS; 2 markers/10 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The first complete local workflow starts at line 50 (28.9%) and there is no `## The short version` — move the prerequisite below a <=40-line block with counted service/file/worker inputs, a smaller workflow/activity trace, the exact artifact/restart success signal, and linked timeout/idempotency/versioning deferrals.
FIX-HIGH: `SDK` first appears unexpanded at line 146 — gloss software development kit before contrasting SDK-provided deterministic operations with ordinary calls.

# background_work/operations/01_security_and_authorization.md (173 lines)
ORDERING: payoff line 15/173 (0.087, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 3:19 (PASS; 3 markers/19 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts principal/resource/current-version inputs, traces one cross-tenant denial, gives the zero-durable-work success signal, and links broker, worker, operator, and revocation hardening.
FIX-HIGH: `DLQ` first appears unexpanded at line 121 — introduce it as a dead-letter queue before discussing copied payloads and operator redrive.

# background_work/operations/02_multitenancy_admission_and_fairness.md (278 lines)
ORDERING: payoff line 56/278 (0.201, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 4:27 (PASS; 4 markers/27 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The first complete reservation trace begins at line 56 and there is no `## The short version` — move prerequisites below a <=40-line block that counts tenant/budget/work-unit inputs, traces two competing reservations, gives the one-commit/no-orphan success signal, and links fairness, retry, and distributed-limit deferrals.
FIX-HIGH: `DLQ` at line 42 and `CTE` at line 75 are unexpanded first uses — gloss dead-letter queue and common table expression locally.

# background_work/operations/03_capacity_planning_and_autoscaling.md (204 lines)
ORDERING: payoff line 32/204 (0.157, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 4:18 (PASS; 4 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The first numeric sizing example starts at line 32 and there is no `## The short version` — move prerequisites below a <=40-line block that counts arrival/service/ceiling/SLO inputs, computes one bounded fleet, gives the age-and-saturation success signal, and links burst/retry/autoscaling hardening.
FIX-HIGH: `OOM` first appears unexpanded at line 84 — gloss out-of-memory termination before using it as a capacity failure signal.

# background_work/operations/README.md (29 lines)
ORDERING: n/a — operations index and reading-order list.
EXPLANATION: n/a — operations index and reading-order list.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index preserves the security-to-fairness-to-capacity progression and names prerequisites.

# background_work/reliability/01_atomic_transitions_and_outbox.md (218 lines)
ORDERING: payoff line 30/218 (0.138, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:13 (PASS; 2 markers/13 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts expected state/version and dependent records, shows the one data-modifying statement, gives the zero/one-row success signal, and links publisher/backoff/reconciliation deferrals.
FIX-HIGH: `CTE` first appears unexpanded in the line-26 header — spell out common table expression before using the acronym.

# background_work/reliability/02_leases_heartbeats_and_fencing.md (263 lines)
ORDERING: payoff line 41/263 (0.156, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 3:18 (PASS; 3 markers/18 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The first executable claim starts at line 41 and there is no `## The short version` — move the prerequisite below a <=40-line block that counts job/worker/lease/token inputs, shows claim plus fenced completion, gives the one-current-token success signal, and links heartbeat, recovery, and provider-effect deferrals.

# background_work/reliability/03_idempotency_and_external_effects.md (290 lines)
ORDERING: payoff line 31/290 (0.107, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:17 (PASS; 2 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts operation scope/key/hash inputs, replays `run-42`, gives the one-effect/same-result signal, and links provider records, ambiguity recovery, retention, and crash testing.

# background_work/reliability/04_retries_timeouts_and_cancellation.md (237 lines)
ORDERING: payoff line 15/237 (0.063, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 2:17 (PASS; 2 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts error class/attempt/age/deadline inputs, traces one retry decision, gives the persisted-next-attempt/terminal-reason signal, and links jitter, timeout, cancellation, and compensation hardening.

# background_work/reliability/05_reconciliation_dlq_and_observability.md (247 lines)
ORDERING: payoff line 13/247 (0.053, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 4:17 (PASS; 4 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 1; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts invariant/evidence/batch inputs, traces one expired-lease repair, gives the bounded-age/repair-rate signal, and links redrive, observability, ordering, and drain hardening.
FIX-HIGH: `DLQ` first appears unexpanded in the line-144 header — introduce dead-letter queue before treating it as retained operator evidence.

# background_work/reliability/README.md (32 lines)
ORDERING: n/a — reliability index and reading order.
EXPLANATION: n/a — reliability index and reading order.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index orders atomic intent, ownership, effects, control, and repair by dependency and identifies prerequisites.

# background_work/state_machines/01_application_code_approaches.md (292 lines)
ORDERING: payoff line 32/292 (0.110, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 1:10 (PASS; 1 marker/10 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move prerequisites below a <=40-line block that counts state/event/context inputs, runs the small `match` baseline, gives the legal-result/illegal-event signal, and links registry, state-object, and hierarchy alternatives.

# background_work/state_machines/02_database_backed_state_machine.md (262 lines)
ORDERING: payoff line 32/262 (0.122, PASS); short version FAIL; length budget PASS.
EXPLANATION: register 3:17 (PASS; 3 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 0 med, 0 low

FIX-HIGH: The note has no `## The short version` — move the prerequisite below a <=40-line block that counts run/event/version/evidence inputs, shows one conditional transition plus job/history creation, gives the one-winner/no-orphan signal, and links cancellation and compatibility hardening.
FIX-HIGH: `CTE` at line 122 and `CAS` at line 232 are unexpanded first uses — spell out common table expression and compare-and-set locally.

# background_work/state_machines/03_event_sourced_state_machine.md (229 lines)
ORDERING: payoff line 36/229 (0.157, FAIL); short version FAIL; length budget PASS.
EXPLANATION: register 2:17 (PASS; 2 markers/17 explanatory paragraphs); restatement PASS; unglossed first uses 0; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 1 high, 0 med, 0 low

FIX-HIGH: The runnable fold starts at line 36 and there is no `## The short version` — move the prerequisite below a <=40-line block that counts stream/version/event inputs, folds the named five-event stream, gives the `GENERATION_QUEUED` success signal, and links append, outbox, projection, and schema-evolution hardening.

# background_work/state_machines/04_end_to_end_workflow.md (547 lines)
ORDERING: payoff line 117/547 (0.214, FAIL); short version FAIL; length budget FAIL.
EXPLANATION: register 0:57 (PASS; 0 markers/57 explanatory paragraphs); restatement PASS; unglossed first uses 2; unexplained rules/defenses 0; intuition-building explanation yes.
Summary: 0 critical, 2 high, 1 med, 0 low

FIX-HIGH: The first complete happy-path outcome begins at line 117 and there is no `## The short version` — move the prerequisite below a <=40-line block that counts run/version/job/outbox/operation inputs, follows the six handoffs, gives the one-terminal-job/workflow/effect signal, and links crash-window sections.
FIX-HIGH: `CTE` at line 215 and `DLQ` at line 446 are unexpanded first uses — gloss common table expression and dead-letter queue locally.
FIX-MED: The 547-line walkthrough has no length justification — split after the first-pass successful lifecycle into a baseline note and crash-recovery continuation, or add a concrete justification plus `Core`/`Production` skip boundaries.

# background_work/state_machines/README.md (30 lines)
ORDERING: n/a — state-machine index and reading order.
EXPLANATION: n/a — state-machine index and reading order.
Summary: 0 critical, 0 high, 0 med, 0 low

NO-ACTION: The index orders modeling, relational persistence, event sourcing, and full assembly and names the implementation prerequisite.

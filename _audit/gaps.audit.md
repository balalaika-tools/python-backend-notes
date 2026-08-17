# fundamentals/
Suggested new notes: 1

GAP: Session-cookie authentication and CSRF — the collection compares sessions with bearer tokens and prescribes CSRF defenses, but never teaches a complete server-side session lifecycle from issuance and rotation through revocation and state-changing request verification.
  SIGNAL: leaned-on
  EVIDENCE: `fundamentals/auth/README.md:53` introduces opaque server-side sessions as a valid alternative; `fundamentals/fastapi/01_http_and_parameter_mapping.md:429` says session cookies usually need CSRF protection; `fundamentals/fastapi/11_api_security.md:463` requires CSRF-token or origin/fetch-metadata validation without a note that assembles the mechanism.

# infrastructure/
Suggested new notes: 2

GAP: OpenTelemetry log collection and cross-signal correlation — the observability path promises one model for traces, metrics, and logs but implements only trace and metric pipelines, leaving readers without the log SDK/bridge, Collector pipeline, correlation fields, and verification path.
  SIGNAL: promised
  EVIDENCE: `infrastructure/observability/README.md:15` advertises “the three signals”; `infrastructure/observability/01_opentelemetry_primer.md:40` includes `LoggerProvider → log records`; `infrastructure/observability/01_opentelemetry_primer.md:147-149` promises one SDK/model for traces, metrics, and logs, while the four-file contents list has no log implementation note.

GAP: Trace sampling and telemetry-volume control — the Collector guide recommends architectures partly on tail sampling, but no note explains head-versus-tail decisions, trace completeness, policy placement, or a verifiable sampling configuration.
  SIGNAL: leaned-on
  EVIDENCE: `infrastructure/observability/04_collector_config.md:39` names tail sampling as a Collector capability and `infrastructure/observability/04_collector_config.md:479` recommends a central Collector when tail sampling must see all spans, without teaching or configuring sampling elsewhere in the observability path.

# operations/
Suggested new notes: 1

GAP: Load and performance testing for backend services — deployment and API guidance require tuning from realistic load tests, but the testing collection has no path from workload model and dependency behavior to saturation evidence, latency percentiles, pass criteria, and repeatable tooling.
  SIGNAL: leaned-on
  EVIDENCE: `operations/deployment/docker_and_deployment.md:135-170` makes worker and concurrency settings depend on load testing; `apis/restful/10_testing_observability_and_operations.md:197` requires realistic dependency and database behavior; `background_work/operations/03_capacity_planning_and_autoscaling.md:141-159` defines load-test safety/liveness criteria, while `operations/testing/README.md:24-42` lists no performance-testing owner.

# apis/
NO-GAPS: The shared foundations and REST, WebSocket, and webhook branches each carry concept, implementation/reliability, security, evolution, testing, and operational ownership without leaning on an absent API topic.

# architecture/
NO-GAPS: The folder declares one long-running-task scope and its five-part sequence covers orchestration, workers, client delivery, infrastructure, and advanced reliability; adjacent durable-work depth has a canonical owner in `background_work/`.

# background_work/
NO-GAPS: The framework-neutral course, state-machine and reliability deep dives, operations sequence, and framework-selection material collectively own every responsibility and product boundary named by the folder indexes.

# persNotes/
NO-GAPS: This is review-history material rather than a teaching collection, so it does not promise a curriculum or lean on missing instructional notes.

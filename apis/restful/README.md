# RESTful API Deep Dive

> A production-oriented path from REST constraints and HTTP semantics to secure evolution and operations.

[![HTTP](https://img.shields.io/badge/HTTP-RFC_9110-005C9C.svg)](https://www.rfc-editor.org/rfc/rfc9110)
[![OpenAPI](https://img.shields.io/badge/OpenAPI-3.x-6BA539.svg?logo=openapiinitiative&logoColor=white)](https://spec.openapis.org/oas/)

---

## Contents

| File | Topic | Description |
|------|-------|-------------|
| [01_rest_mental_model.md](01_rest_mental_model.md) | REST mental model | Constraints, resources, representations, state, and maturity |
| [02_http_semantics.md](02_http_semantics.md) | HTTP semantics | Methods, status codes, headers, negotiation, and intermediaries |
| [03_resource_and_uri_design.md](03_resource_and_uri_design.md) | Resource design | Boundaries, URIs, relationships, commands, and long-running work |
| [04_representations_validation_and_errors.md](04_representations_validation_and_errors.md) | Representations and errors | Media types, validation, Problem Details, and partial results |
| [05_pagination_filtering_and_search.md](05_pagination_filtering_and_search.md) | Collections | Cursor/offset pagination, filters, sorting, search, and consistency |
| [06_concurrency_idempotency_and_retries.md](06_concurrency_idempotency_and_retries.md) | Reliability | Preconditions, idempotency keys, ambiguous outcomes, and retry policy |
| [07_caching_and_performance.md](07_caching_and_performance.md) | Caching | Freshness, validators, cache keys, invalidation, and performance |
| [08_security.md](08_security.md) | Security | AuthN/AuthZ, BOLA, fields, CORS/CSRF, abuse, and SSRF |
| [09_versioning_compatibility_and_openapi.md](09_versioning_compatibility_and_openapi.md) | Evolution | Compatibility, versions, OpenAPI, deprecation, and migration |
| [10_testing_observability_and_operations.md](10_testing_observability_and_operations.md) | Operations | Test pyramid, telemetry, SLOs, rollout, and incident diagnosis |

---

## Reading Order

**Working result by entry 2**: explain the REST constraint model and trace one request through shared
HTTP method and response semantics.

1. **Understand:** [REST Mental Model](01_rest_mental_model.md) and [HTTP Semantics](02_http_semantics.md).
2. **Build the baseline:** [Resource and URI Design](03_resource_and_uri_design.md) plus [Representations, Validation, and Errors](04_representations_validation_and_errors.md).

**Stop here if** the API is small, internal, and has no collection, concurrent-write, cache, or
evolution pressure. Continue by requirement:

- Growing collections → [Pagination, Filtering, and Search](05_pagination_filtering_and_search.md)
- Concurrent writes or retries → [Concurrency, Idempotency, and Retries](06_concurrency_idempotency_and_retries.md)
- Shared or client caching → [Caching and Performance](07_caching_and_performance.md)
- Any untrusted caller or tenant boundary → [Security](08_security.md)
- Independently deployed clients → [Versioning, Compatibility, and OpenAPI](09_versioning_compatibility_and_openapi.md)
- Production rollout and support → [Testing, Observability, and Operations](10_testing_observability_and_operations.md)

---

## Prerequisites

- [API Fundamentals](../01_api_fundamentals.md)
- [HTTPX mental model](../../fundamentals/httpx/01_mental_model.md) for Python client transport details

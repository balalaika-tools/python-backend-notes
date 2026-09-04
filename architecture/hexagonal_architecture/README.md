# Hexagonal Architecture for Python Backends

> Design FastAPI services, workers, and AI-enabled backends so business actions outlive their current frameworks and providers.

---

## Contents

| File | Role | Topic | Reader outcome |
|------|------|-------|----------------|
| [01 — Why Hexagonal Architecture](01_why_hexagonal_architecture.md) | Foundation | The coupling pressure behind the pattern | Decide whether the pattern buys enough for a service |
| [02 — Build One Vertical Slice](02_build_one_vertical_slice.md) | Tutorial | A complete application action with two inbound adapters | Run one use case from API- and worker-shaped entry points |
| [03 — Dependency Direction](03_dependencies_point_toward_business_policy.md) | Foundation | Runtime calls versus source dependencies | Draw and audit the dependency rule |
| [04 — Boundary Placement](04_map_code_to_owning_boundaries.md) | Decision guide | Where source files belong | Place ambiguous code by ownership rather than framework |
| [05 — Ports and Adapter Contracts](05_design_ports_and_adapter_contracts.md) | Deep dive | Port admission, types, and failure translation | Define useful contracts without interface ceremony |
| [06 — Runtime Composition](06_compose_the_runtime_at_the_edge.md) | Implementation | Construction, lifespan, and disposal | Build a composition root without leaking policy into bootstrap |
| [07 — APIs and Workers](07_apply_the_pattern_to_apis_and_workers.md) | Implementation | FastAPI, consumers, scheduled work, and hybrids | Reuse an action across process boundaries safely |
| [08 — GenAI Boundary](08_treat_genai_as_an_external_capability.md) | Deep dive | Models, prompts, agents, tools, and typed results | Keep AI mechanics outside business execution |
| [09 — Testing Boundaries](09_test_through_architectural_boundaries.md) | Implementation | Unit, integration, contract, and E2E tests | Test business behavior without patching SDK internals |
| [10 — Flat-First Growth](10_grow_without_package_ceremony.md) | Decision guide | When modules earn packages and abstractions | Grow structure without empty layers or catch-alls |
| [11 — Migration and Review](11_migrate_and_review_an_existing_service.md) | Decision guide | Moving an existing service safely | Produce an ownership map and incremental migration plan |

---

## Reading Order

### First-time path

**Working result by entry 2**: run one ticket-classification action through both an HTTP-shaped
handler and a queue-worker-shaped handler, then observe identical business results.

1. **Do—diagnose the coupled route:** [Why Hexagonal Architecture](01_why_hexagonal_architecture.md) traces concrete change requests and assigns each resulting responsibility an owner.
2. **Do—build the separated result:** [Build One Vertical Slice](02_build_one_vertical_slice.md) runs the smallest complete example.
3. **Understand the mechanism:** [Dependency Direction](03_dependencies_point_toward_business_policy.md) separates runtime call flow from import direction.
4. **Organize:** [Boundary Placement](04_map_code_to_owning_boundaries.md) turns that rule into a Python package tree.
5. **Harden when required:** add [Port Contracts](05_design_ports_and_adapter_contracts.md), [Runtime Composition](06_compose_the_runtime_at_the_edge.md), and [Boundary Testing](09_test_through_architectural_boundaries.md).

**Stop here if** one process, a small action, and direct dependencies remain easy to test and
change. Continue when another transport, costly external capability, complex lifecycle, or
independent failure policy appears.

### FastAPI plus worker path

1. **Do:** run the [vertical slice](02_build_one_vertical_slice.md).
2. **Understand:** trace [dependency direction](03_dependencies_point_toward_business_policy.md).
3. **Extend:** apply the action to [APIs and workers](07_apply_the_pattern_to_apis_and_workers.md).
4. **Harden:** centralize [runtime composition](06_compose_the_runtime_at_the_edge.md) and split [test profiles](09_test_through_architectural_boundaries.md).

### AI backend path

1. **Do:** run the [vertical slice](02_build_one_vertical_slice.md), whose fake classifier represents a nondeterministic external capability.
2. **Understand—revisit the reasoning:** read [Why Hexagonal Architecture](01_why_hexagonal_architecture.md) and map each example boundary back to the change pressure that earned it.
3. **Implement:** place provider code behind the [GenAI boundary](08_treat_genai_as_an_external_capability.md).
4. **Harden:** test deterministic policy separately using [boundary-oriented tests](09_test_through_architectural_boundaries.md).

### Existing-service migration path

1. **Do—map one current action:** use [Why Hexagonal Architecture](01_why_hexagonal_architecture.md) to label the business decisions and external effects in one coupled entry point.
2. **Understand:** audit its [dependency direction](03_dependencies_point_toward_business_policy.md) and assign each file through the [boundary placement test](04_map_code_to_owning_boundaries.md).
3. **Change incrementally:** apply [flat-first growth](10_grow_without_package_ceremony.md) and the [migration sequence](11_migrate_and_review_an_existing_service.md) one vertical slice at a time.

**Stop after the ownership map if** the current structure already preserves one-way dependencies
and clear test seams. Move code only when the map exposes a concrete violation or isolation gain.

---

## Prerequisites

- Comfortable reading typed Python and `async` functions.
- [FastAPI fundamentals](../../fundamentals/fastapi/README.md) are useful for the API chapter but not required for the first example.
- [Testing fundamentals](../../operations/testing/README.md) provide the broader pytest path; this section focuses on tests as architectural evidence.

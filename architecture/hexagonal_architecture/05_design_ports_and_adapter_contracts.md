# Design Ports Around Caller Needs and Failure Decisions

> **Who this is for**: Engineers deciding whether an external dependency deserves a port and what that contract should contain.

A port has a cost: another name, type, implementation, and test seam. Pay that cost when it isolates
behavior the application must reason about—not because every dependency “should have an interface.”

---

## 1. A port earns its cost when the boundary changes application behavior

A classifier is remote, nondeterministic, costly, and capable of transient or invalid-output
failures. The application may retry, defer, or request human review based on those outcomes. That is
a valuable port.

Use this practical admission test. Introduce a port when at least two are true:

1. The dependency is remote, nondeterministic, expensive, or externally controlled.
2. Its failures materially change business behavior and need deterministic tests.
3. Multiple implementations or small local fakes have concrete value.

A clock used to decide expiration, object store, message publisher, remote HTTP service, LLM, or
browser portal often qualifies. Parsing, formatting, validation, and in-memory calculation usually
do not.

> **Core:** a port represents a capability requested by the application, not every collaborator the
> application happens to call.

---

## 2. Name the capability without assuming its implementation

`ClassificationModel` assumes a model. `OpenAIClient` assumes a provider.
`TicketClassifier` states what the caller needs:

```python
@dataclass(frozen=True)
class ClassificationCandidate:
    category: str
    confidence: float


class TicketClassifier(Protocol):
    async def classify(self, body: str) -> ClassificationCandidate: ...
```

An LLM, rules engine, hybrid classifier, or remote API can implement this conversation. Avoid raw
`dict[str, Any]`, unvalidated JSON, SDK messages, and provider response objects when a stable typed
shape exists.

Keep the input narrow as well. Passing the entire FastAPI request or settings object makes the port
depend on the current edge instead of the caller's actual data need.

---

## 3. The port owns stable success and failure contracts

If application code catches an SDK exception, the provider already owns part of the use case.
Define failures in the port according to decisions the caller can make:

```python
class TicketClassifierError(RuntimeError):
    pass


class ClassificationUnavailable(TicketClassifierError):
    """A transient failure may be retried or deferred."""


class InvalidClassification(TicketClassifierError):
    """The provider answered, but no trusted candidate can be produced."""
```

The concrete adapter translates implementation failures:

```python
async def classify(self, body: str) -> ClassificationCandidate:
    try:
        output = await self._model.ainvoke(self._prompt(body))
    except ProviderTimeout as exc:
        raise ClassificationUnavailable("classifier timed out") from exc

    if output.confidence < 0.0 or output.confidence > 1.0:
        raise InvalidClassification("confidence is outside [0, 1]")

    return ClassificationCandidate(
        category=output.category,
        confidence=output.confidence,
    )
```

The port's error message contains no prompt, token, API key, or raw provider body. Exception chaining
preserves diagnostics without making the inner layer import the provider type.

---

## 4. Give the caller only distinctions it can act on

An exhaustive copy of provider errors is not a stable application contract. Suppose the action has
three meaningful outcomes:

| Port result | Application decision |
|-------------|----------------------|
| Candidate with adequate confidence | Accept and persist |
| `ClassificationUnavailable` | Defer according to action policy |
| `InvalidClassification` | Route to human review |

If rate limits and provider timeouts produce the same action decision, they may share one stable
failure even though the adapter records different telemetry. Split errors only when callers need
different behavior.

Conversely, do not return `None` for every failure. It erases whether the ticket was absent, the
classifier was unavailable, or output was rejected.

> **Key insight**: a port is complete only when its success types and failure types let the caller
> make every required decision without importing implementation details.

---

## 5. Database ports are optional rather than ceremonial

A fixed database behind a cohesive repository layer may already isolate query mechanics. Adding a
`Protocol` above every repository can duplicate methods without changing tests or substitution.

Add a repository port when application tests gain a clean fake, multiple persistence strategies
exist, or persistence failures form an application-relevant contract. Otherwise inject the
repository class directly while keeping its SQLAlchemy implementation in `db/`.

This is still dependency-aware design: a concrete repository can accept and return domain types
without leaking ORM sessions through application code.

---

## 6. Contract tests and observability reveal translation mistakes

**Success signal:** an application unit test can drive each meaningful success and failure outcome
using a tiny fake, while the action imports no SDK exceptions. Separately, adapter tests prove each
provider outcome maps to the intended port outcome.

⚠️ The first failure is “leaky typing”: a port looks abstract but exposes `BaseMessage`,
`AsyncSession`, SQS receipt handles, or raw response dictionaries. The leak often appears later
when a fake must reconstruct provider objects just to test one business branch.

Do not create a port for a pure function or a single stable collaborator whose direct injection is
already clear. The interface adds indirection without isolating volatility or failure.

> **Production:** adapters should record provider-specific failure details through safe telemetry
> before translating them, with secrets and sensitive payloads excluded. The application receives
> only the stable contract.

---

**Next**: [Part 6 — Compose the Runtime at the Edge](06_compose_the_runtime_at_the_edge.md)


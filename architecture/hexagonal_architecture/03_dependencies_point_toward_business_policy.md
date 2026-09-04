# Dependencies Point Toward Business Policy

> **Who this is for**: Engineers who ran the vertical slice and want to understand why calls may go outward while imports still point inward.

`ClassifyTicket` invokes a classifier at runtime, yet the application must not import the concrete
LLM classifier. That apparent contradiction is the mechanism at the heart of Hexagonal
Architecture: control flow and source dependency are different graphs.

---

## 1. A direct import gives the provider ownership of the action

Suppose the action constructs its dependency directly:

```python
from ticket_triage.genai.ticket_classification.classifier import LLMClassifier


class ClassifyTicket:
    def __init__(self) -> None:
        self._classifier = LLMClassifier()
```

The action now changes when model construction changes, tests need provider setup unless they patch
the imported symbol, and a rule-based alternative requires editing business code. The runtime call
was always outward; the problematic addition is the inward package importing an outer concrete
choice.

> **Core:** business policy may describe the capabilities it needs, but it must not select or
> construct the technologies that fulfill them.

---

## 2. Runtime flow and import direction form different graphs

At runtime, the action calls an injected implementation:

```text
ClassifyTicket ──call──► LLMClassifier ──HTTP──► model provider
```

In source code, both sides depend on the stable port:

```text
application/classify_ticket.py ──import──► ports/ticket_classifier.py
genai/.../classifier.py         ──import──► ports/ticket_classifier.py
```

The concrete classifier may explicitly implement or merely structurally satisfy the protocol. The
important part is that `application/` does not import `genai/`.

This is **dependency inversion**: high-level policy does not depend on low-level implementation;
both depend on an abstraction shaped around the high-level caller's need.

> **The near-miss**: framework dependency injection and dependency inversion sound alike. FastAPI's
> `Depends` resolves values for a request; dependency inversion decides which source package is
> allowed to know which. A service can use `Depends` everywhere and still couple application code
> directly to SQLAlchemy or an LLM SDK.

---

## 3. The caller owns the conversation shape

A provider-shaped port leaks the wrong owner:

```python
# Provider details force every implementation to speak SDK language.
class ClassificationModel(Protocol):
    async def invoke(self, messages: list[BaseMessage]) -> AIMessage: ...
```

The application actually needs a business candidate:

```python
@dataclass(frozen=True)
class ClassificationCandidate:
    category: str
    confidence: float


class TicketClassifier(Protocol):
    async def classify(self, body: str) -> ClassificationCandidate: ...
```

The second contract permits an LLM, rules engine, hybrid, or remote classification API. More
importantly, it lets the action express business handling of category and confidence without
understanding provider messages.

The abstraction belongs near the caller because the caller determines the smallest stable
conversation. Concrete adapters translate richer provider APIs into that shape.

---

## 4. The composition root is allowed to know concrete choices

Someone must connect the abstract requirement to a concrete implementation. That code belongs at
the process edge, normally `bootstrap/runtime.py`:

```python
repository = SqlAlchemyTicketRepository(session_factory)
classifier = LLMTicketClassifier(model=model)
classify_ticket = ClassifyTicket(
    tickets=repository,
    classifier=classifier,
)
```

This **composition root** is the ordinary runtime location that constructs the dependency graph.
It imports inward-facing actions and outward-facing implementations because choosing between them
is its job. Business packages never import bootstrap back.

Construction is not a loophole for business policy. Bootstrap may choose a classifier from trusted
configuration; the application action still decides what a low-confidence candidate means for a
ticket.

---

## 5. An import audit makes the rule testable

For the representative service, the allowed dependency map is:

```text
main ──► bootstrap ──► api, db, adapters, genai, application
api ─────────────────► application, domain
adapter consumers ───► application, ports
application ─────────► domain, ports
db ──────────────────► domain, ports
genai ────────────────► domain, ports
domain ───────────────► dependency-light Python only
ports ────────────────► domain and dependency-light Python only
```

The highest-value review checks are:

- `application/` imports no `api`, `bootstrap`, `db`, `adapters`, `genai`, ORM, or provider SDK.
- `domain/` and `ports/` import no framework or concrete integration.
- Inbound adapters call public application actions.
- Concrete driven adapters depend inward on the port they fulfill.
- Business code never imports bootstrap.

**Success signal:** replacing `LLMTicketClassifier` in `bootstrap/runtime.py` requires no edit in
`application/`. A silent failure is a type annotation or exception handler in the action that still
imports the old provider even though construction was moved.

> **Key insight**: dependency direction is determined by who owns the contract in source code, not
> by the direction of the runtime method call.

---

## 6. Cycles and pass-through layers expose misplaced ownership

⚠️ If `application/` imports an adapter while that adapter imports the action's types, a circular
import is often the first visible symptom. Moving imports inside functions hides the cycle without
fixing the two-way ownership.

Another smell is a layer that only forwards every argument and return value. An application action
with no policy, sequencing, stable contract, or meaningful operation may not have earned a separate
class yet. Keep the action as a small function, or call the adapter directly from the boundary when
there is genuinely no business use case to preserve.

Do not use this dependency structure when a small integration wrapper is the product and there is
no independent business policy. A cohesive provider client library should expose its own capability
rather than imitate a deployable service shell.

> **Production:** add static import rules with a dependency checker when the service has enough
> contributors that review alone no longer preserves the graph. The rule should encode actual
> forbidden edges, not merely require every possible layer.

---

**Next**: [Part 4 — Map Code to Owning Boundaries](04_map_code_to_owning_boundaries.md)


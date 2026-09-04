# Treat GenAI as an External Capability

> **Who this is for**: Engineers adding structured model calls, agents, tools, retrieval, or LangGraph workflows without turning AI code into the business layer.

A large language model (LLM) is remote, nondeterministic, expensive, and provider-controlled. It is
therefore an unusually strong candidate for a port. The application should receive a typed business
candidate—not model messages, prompt templates, graph state, or raw provider JSON.

---

## 1. A model call is not the classification use case

The application action may load a ticket, enforce eligibility, request a classification candidate,
interpret confidence, persist the decision, and publish the next outcome. The GenAI implementation
may build provider input, invoke the configured handle, validate structured output, and translate
provider failures.

```text
application/classify_ticket.py
    owns eligibility → request candidate → interpret → persist/handoff

genai/ticket_classification/classifier.py
    owns prompt input → invoke model → validate provider output → port result
```

If `genai/` decides whether a ticket is eligible or where low-confidence work goes, provider
mechanics have absorbed business policy. If `application/` constructs prompts or catches SDK
exceptions, the dependency points outward.

> **Core:** every LLM, prompt, agent, AI schema, tool, graph, model binding, and AI middleware lives
> under root `genai/`; business execution remains under `application/`.

---

## 2. A small structured-output task has four owners

```text
genai/
└── ticket_classification/
    ├── llm.py          # Construct and bind the model
    ├── schemas.py      # Validate provider-facing structured output
    ├── prompts.py      # Own prompt text and version, when nontrivial
    └── classifier.py   # Implement TicketClassifier and translate failures
```

Create only responsibilities that exist, but every task keeps model construction in `llm.py`.
Do not name that module `models.py`, which reads as business or persistence entities.

```python
# llm.py
def build_model(*, model_name: str, model_provider: str):
    return init_chat_model(
        model=model_name,
        model_provider=model_provider,
    ).with_structured_output(ClassificationOutput)
```

```python
# classifier.py
class LLMTicketClassifier:
    def __init__(self, model: Runnable) -> None:
        self._model = model

    async def classify(self, body: str) -> ClassificationCandidate:
        output = await self._model.ainvoke(build_prompt(body))
        return ClassificationCandidate(output.category, output.confidence)
```

Bootstrap calls the factory and injects the configured handle into the capability implementation.
No model, agent, checkpointer, or Model Context Protocol (MCP) client is constructed at module import.

---

## 3. Agent factories assemble harnesses but do not invoke them

An agent task adds `agent.py`:

```text
genai/pricing_agent/
├── llm.py
├── schemas.py
├── prompts.py
├── tools.py
├── agent.py
└── pricer.py
```

`agent.py` accepts constructed models and explicit tools, then returns the harness. `pricer.py`
implements the application-facing `TicketPricer` capability by invoking the harness and
translating its result.

A custom `graph/` package is justified only when the service defines graph state, nodes, routing,
or edges. Using an agent library that internally has a graph does not create a project-owned graph
responsibility.

---

## 4. Tools cross trust boundaries and need narrow authority

An AI tool is an adapter over a port or public application action. It validates typed input, applies
authorization from trusted application context, calls bounded behavior, and returns a safe result.

```python
async def get_ticket(ticket_id: str, context: ApplicationContext) -> TicketView:
    context.require_tenant_access()
    return await ticket_reader.get_for_tenant(
        ticket_id=ticket_id,
        tenant_id=context.tenant_id,
    )
```

The agent must not invent `tenant_id` from prompt text. Tool discovery must not silently broaden
permissions. A tool should not query a database directly if doing so bypasses application
authorization or auditing.

Prompt injection is the attack: untrusted ticket text tells the model to retrieve another tenant's
ticket; an overpowered tool obeys. The defense is server-supplied identity, authorization inside the
tool boundary, and a capability narrow enough that model text cannot choose wider authority.

---

## 5. Retrieval and prompts follow semantic ownership

Keep retrieval local to one AI capability until another genuinely reuses the same retrieval,
reranking, and context semantics. Application-owned ingestion and index-refresh actions remain in
`application/`; vector-index contracts remain in `ports/`; concrete persistence belongs in
`db/` or the appropriate adapter.

Prompts are versioned implementation details of their AI task. Persist or emit the version used
when reproducibility matters. Similar wording is not enough to justify `genai/shared/prompts/`;
promote only demonstrated shared semantics.

> **Key insight**: GenAI belongs outside the application not because it is unimportant, but because
> its nondeterminism, trust boundary, cost, and provider mechanics must not define business policy.

---

## 6. Test the seam before paying for a live call

Test prompt assembly, schema rejection, factories, capability invocation with a fake model handle,
failure translation, graph routing, and authorization propagation separately. Ordinary unit tests
make no live model call and require no provider credentials.

**Success signal:** `ClassifyTicket` can be tested with a six-line fake `TicketClassifier`, while
`LLMTicketClassifier` can be tested with a fake model handle returning structured output. Changing
model provider edits `genai/`, configuration, and bootstrap—not application policy.

⚠️ The first failure is raw provider output crossing the port. The symptom is application code
reading message content, tool-call arrays, or provider refusal fields. Translate them into stable
typed outcomes inside `genai/`.

Do not create a GenAI abstraction when the product is intentionally a thin provider-specific client
library with no independent business action. In a deployable business service, however, even one
small model call belongs under the explicit `genai/` boundary.

> **Production:** add timeouts, bounded attempts, token/cost limits, safe telemetry, refusal
> handling, prompt versioning, and optional live tests according to the failure each prevents.
> Never log secrets or sensitive prompts by default.

---

**Next**: [Part 9 — Test Through Architectural Boundaries](09_test_through_architectural_boundaries.md)


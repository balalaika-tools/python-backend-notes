# Build One Vertical Slice Before Adding Layers

> **Who this is for**: Python backend engineers who want a runnable first example of one application action shared by two inbound adapters.

The example below classifies two support tickets. An HTTP-shaped function and a worker-shaped
function both call the same `ClassifyTicket` action. The only requirement is Python 3.11 or newer;
save the block as `slice.py` and run `python slice.py`.

---

## 1. Run the complete baseline

```python
from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Ticket:
    ticket_id: str
    body: str


@dataclass(frozen=True)
class Classification:
    ticket_id: str
    category: str


class TicketRepository(Protocol):
    async def get(self, ticket_id: str) -> Ticket: ...


class TicketClassifier(Protocol):
    async def classify(self, body: str) -> str: ...


class ClassifyTicket:
    def __init__(
        self,
        tickets: TicketRepository,
        classifier: TicketClassifier,
    ) -> None:
        self._tickets = tickets
        self._classifier = classifier

    async def execute(self, ticket_id: str) -> Classification:
        ticket = await self._tickets.get(ticket_id)
        category = await self._classifier.classify(ticket.body)
        return Classification(ticket.ticket_id, category)


class InMemoryTickets:
    def __init__(self, tickets: list[Ticket]) -> None:
        self._tickets = {ticket.ticket_id: ticket for ticket in tickets}

    async def get(self, ticket_id: str) -> Ticket:
        return self._tickets[ticket_id]


class KeywordClassifier:
    async def classify(self, body: str) -> str:
        return "billing" if "invoice" in body.lower() else "general"


async def http_handler(ticket_id: str, action: ClassifyTicket) -> dict[str, str]:
    result = await action.execute(ticket_id)
    return {"ticket_id": result.ticket_id, "category": result.category}


async def worker_handler(message: dict[str, str], action: ClassifyTicket) -> None:
    result = await action.execute(message["ticket_id"])
    print(f"worker classified {result.ticket_id} as {result.category}")


async def main() -> None:
    tickets = InMemoryTickets(
        [
            Ticket("T-100", "My invoice contains the wrong amount"),
            Ticket("T-200", "How do I change my email address?"),
        ]
    )
    action = ClassifyTicket(tickets=tickets, classifier=KeywordClassifier())

    response = await http_handler("T-100", action)
    print(f"http response: {response}")

    await worker_handler({"ticket_id": "T-200"}, action)


asyncio.run(main())
```

Expected output:

```text
http response: {'ticket_id': 'T-100', 'category': 'billing'}
worker classified T-200 as general
```

**Success signal:** both lines appear, and both entry points use the same constructed `action`.
If you see `KeyError`, the requested ticket ID is not present in `InMemoryTickets`; that is the
baseline's deliberately small failure contract, not a transport problem.

> **Production:** this baseline intentionally defers typed failure contracts, persistence,
> transactions, provider timeouts, retries, telemetry, and lifecycle management. The later notes
> add each concern after its need becomes visible.

---

## 2. Three kinds of code cooperate without knowing everything

The example has three architectural roles:

```text
Driving adapters              Application core              Driven adapters
────────────────              ────────────────              ───────────────
http_handler ────────────────► ClassifyTicket ─────────────► InMemoryTickets
worker_handler ──────────────►       │                      KeywordClassifier
                                  contracts
```

A **driving adapter** translates an external trigger into an application call. A **driven adapter**
fulfills a capability requested by the application. The word “adapter” means translation at a
boundary; it does not imply inheritance from a framework base class.

`ClassifyTicket` coordinates the use case. It knows that classification requires loading a ticket
and obtaining a category. It does not know whether the trigger was HTTP or a queue message, or
whether ticket loading uses memory or PostgreSQL.

> **Core:** the application action is the stable center of the example. Handlers translate into
> it, and external implementations satisfy the contracts it consumes.

---

## 3. Structural typing keeps the first port small

Python's `Protocol` defines behavior by shape. `ClassifyTicket` accepts any object with the declared
async method, without requiring concrete adapters to inherit from the protocol.

```python
class TicketClassifier(Protocol):
    async def classify(self, body: str) -> str: ...
```

`KeywordClassifier` satisfies this contract because it has a compatible `classify` method. A future
LLM-backed implementation can satisfy the same caller need while hiding model messages and provider
responses.

The protocol is worthwhile here because classification is a replaceable, potentially remote and
nondeterministic capability. A pure `normalize_subject()` function would not earn a port; call and
test deterministic calculations directly.

---

## 4. The adapters translate rather than decide policy

The two inbound functions differ only where their transports differ:

```python
async def http_handler(ticket_id: str, action: ClassifyTicket) -> dict[str, str]:
    result = await action.execute(ticket_id)
    return {"ticket_id": result.ticket_id, "category": result.category}


async def worker_handler(message: dict[str, str], action: ClassifyTicket) -> None:
    result = await action.execute(message["ticket_id"])
    print(f"worker classified {result.ticket_id} as {result.category}")
```

An actual FastAPI route would translate path parameters and results. An actual broker consumer
would parse an envelope and translate application outcomes to acknowledge, retry, or dead-letter
behavior. Neither should decide what category is valid or whether a ticket is eligible.

If the worker later applies different business policy, that is evidence for a different application
action or an explicit policy input—not permission to hide the branch in queue code.

---

## 5. Replace an adapter without editing the action

Change only the constructed classifier:

```python
class AlwaysEscalateClassifier:
    async def classify(self, body: str) -> str:
        return "human_review"


action = ClassifyTicket(
    tickets=tickets,
    classifier=AlwaysEscalateClassifier(),
)
```

Both handlers now return `human_review`; `ClassifyTicket` and its callers are unchanged. That is the
smallest observable proof that the dependency is inverted around a caller-owned capability.

> **Key insight**: the first useful hexagon is one application action whose external effects can be
> replaced through small contracts; the directory tree is only a way to preserve that property as
> the service grows.

---

## 6. Know what breaks first and when to stop

⚠️ The first real failure is the untyped `KeyError` from the repository. Once callers need to choose
between not-found, transient storage failure, and invalid state, define stable port-owned errors as
shown in [Port Contracts](05_design_ports_and_adapter_contracts.md).

Do not split this example into eleven production packages yet. If this were the whole service, a
few cohesive modules would be clearer. Introduce the physical boundaries from [Boundary Placement](04_map_code_to_owning_boundaries.md)
when frameworks, providers, lifecycle, or independent ownership make the dependency rule hard to
see in a flat package.

**How you know the design still works:** add a second handler or classifier without changing
`ClassifyTicket`. If every new transport forces branches into the action, or every provider forces
its types into the port, revisit which side owns the translation.

---

**Next**: [Part 3 — Dependencies Point Toward Business Policy](03_dependencies_point_toward_business_policy.md)


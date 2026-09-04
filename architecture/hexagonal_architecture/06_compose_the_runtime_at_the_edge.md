# Compose the Runtime at the Process Edge

> **Who this is for**: Engineers wiring settings, database engines, clients, model handles, application actions, and deterministic shutdown.

Moving constructors out of an action is incomplete if concrete dependencies become module globals
spread across routes and workers. A **composition root** is the one ordinary runtime location that
knows which implementations satisfy which application needs.

---

## 1. Import-time construction hides failure and disposal

This module opens a client as a side effect of import:

```python
# Wrong owner: importing the module starts runtime construction.
settings = Settings()
http_client = httpx.AsyncClient(timeout=settings.timeout)
classifier = LLMTicketClassifier(http_client)
```

Tests importing one symbol now require configuration. Reload behavior can duplicate handles.
Shutdown ownership is unclear, and startup failures happen before the process can report readiness
cleanly.

Construct resources explicitly inside `bootstrap/runtime.py`, after configuration is validated and
before the process accepts work.

> **Core:** configuration describes policy, factories construct technology-specific objects, and
> bootstrap decides when construction and disposal occur.

---

## 2. A typed runtime exposes already-composed entry points

This explanatory excerpt shows the shape; the concrete factories belong to their technical owners:

```python
@dataclass(frozen=True)
class Runtime:
    classify_ticket: ClassifyTicket
    session_factory: async_sessionmaker[AsyncSession]


@asynccontextmanager
async def build_runtime(settings: Settings) -> AsyncIterator[Runtime]:
    engine = create_async_engine(settings.database_url)
    session_factory = async_sessionmaker(engine, expire_on_commit=False)
    model = build_model(
        model_name=settings.classification_model,
        model_provider=settings.model_provider,
    )
    classifier = LLMTicketClassifier(model=model)
    repository = SqlAlchemyTicketRepository(session_factory)
    action = ClassifyTicket(repository, classifier)

    try:
        yield Runtime(action, session_factory)
    finally:
        await engine.dispose()
```

The runtime container exposes useful constructed dependencies, not the whole settings object or a
generic dictionary. FastAPI dependencies and worker consumers receive the action; they do not
rebuild it.

If the model handle or HTTP client owns an async close operation, bootstrap closes it too. Disposal
runs in reverse dependency order: stop new intake, await bounded in-flight work, then close the
resources that work uses.

---

## 3. Factories retain technology-specific construction knowledge

Bootstrap coordinates factories; it should not absorb their internals:

```python
# genai/ticket_classification/llm.py
def build_model(*, model_name: str, model_provider: str):
    return init_chat_model(
        model=model_name,
        model_provider=model_provider,
    ).with_structured_output(ClassificationOutput)
```

```python
# bootstrap/runtime.py
model = build_model(
    model_name=settings.classification_model,
    model_provider=settings.model_provider,
)
classifier = LLMTicketClassifier(model=model)
```

The task-level factory knows how to bind structured output. Bootstrap knows which validated values
and lifecycle dependencies to supply. Neither application code nor a module import chooses the
provider.

---

## 4. FastAPI lifespan enters the same runtime

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with build_runtime(load_settings()) as runtime:
        app.state.runtime = runtime
        yield


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(ticket_router)
    return app
```

`bootstrap/app.py` owns the FastAPI instance, lifespan, router registration, and framework
instrumentation. `api/dependencies.py` may retrieve the already-built action from app state and
present it to routes.

A worker process can enter the same `build_runtime()` context without importing FastAPI. That is
why runtime composition belongs above process adapters rather than inside a route.

---

## 5. Supervisors own loops; actions own work

A long-running worker needs task creation, stop events, health, and graceful shutdown. Put those
mechanics in `bootstrap/supervisor.py`:

```python
async def supervise(consumer: TicketConsumer, stop: asyncio.Event) -> None:
    async with asyncio.TaskGroup() as tasks:
        tasks.create_task(consumer.run(stop))
        tasks.create_task(report_health(stop))
```

The supervisor controls process lifetime. The consumer translates deliveries. `ClassifyTicket`
owns business execution. Business stage order does not belong in the supervisor merely because it
runs actions sequentially.

> **Key insight**: bootstrap may know every concrete object while knowing no business decision; its
> job is to create, connect, start, and dispose the graph.

---

## 6. Readiness and shutdown prove lifecycle ownership

**Success signal:** startup builds one shared graph, readiness becomes true only after required
dependencies initialize, and shutdown stops intake before closing those dependencies. Tests can
replace constructors and assert creation/disposal without executing business behavior.

⚠️ The first failure is a use-after-close during shutdown: the database engine or HTTP client closes
while a consumer task is still processing. The symptom is a burst of connection or cancellation
errors exactly when the deployment terminates.

Do not centralize short-lived request transactions in the process runtime. Bootstrap owns the
session factory or engine lifetime; the repository or request dependency owns each transaction's
narrower lifetime.

> **Production:** give graceful shutdown a bounded deadline. Once it expires, record unfinished work
> and rely on durable redelivery or reconciliation instead of waiting forever.

---

**Next**: [Part 7 — Apply the Pattern to APIs and Workers](07_apply_the_pattern_to_apis_and_workers.md)


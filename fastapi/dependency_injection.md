# FastAPI Dependency Injection — A Practical Guide

## 1. What Is Dependency Injection in FastAPI?

FastAPI has **built-in dependency injection (DI)** that allows you to:

* Share logic across endpoints
* Manage resources (DB sessions, auth, configs)
* Keep endpoints clean and testable

In FastAPI, dependencies are defined as **callables** (usually functions) and declared using `Depends`.

---

## 2. The Core Concept: `Depends`

At its simplest, a dependency is just a function.

```python
from fastapi import Depends

def get_user():
    return {"username": "alice"}
```

You inject it into an endpoint using `Depends`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/profile")
def profile(user=Depends(get_user)):
    return user
```

FastAPI:

* Calls `get_user`
* Injects its return value into `user`
* Handles execution order automatically

---

## 3. Why FastAPI DI Is Powerful

FastAPI’s DI system:

* Is **type-aware**
* Works with **async and sync**
* Supports **scopes & lifetimes**
* Is **framework-level**, not a third-party container

You get clean code without manual wiring.

---

## 4. Dependencies for Shared Logic

### Example: Query Parameter Validation

```python
def pagination_params(limit: int = 10, offset: int = 0):
    return {"limit": limit, "offset": offset}
```

```python
@app.get("/items")
def list_items(pagination=Depends(pagination_params)):
    return pagination
```

Used across multiple endpoints without duplication.

---

## 5. Dependencies with Classes

You can use **classes as dependencies**.

```python
class Settings:
    def __init__(self):
        self.debug = True
```

```python
def get_settings():
    return Settings()
```

```python
@app.get("/debug")
def debug(settings=Depends(get_settings)):
    return {"debug": settings.debug}
```

This is useful for configuration, services, and clients.

---

## 6. Dependency Injection for Databases

### Basic DB Session Pattern

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

```python
@app.get("/users")
def get_users(db=Depends(get_db)):
    return db.query(User).all()
```

Key points:

* `yield` enables **setup + teardown**
* FastAPI guarantees cleanup
* One session per request

---

## 7. Dependency Injection for Authentication

```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(status_code=401)
    return user
```

```python
@app.get("/me")
def me(user=Depends(get_current_user)):
    return user
```

Authentication becomes:

* Reusable
* Centralized
* Automatically enforced

---

## 8. Dependency Hierarchies (Dependencies of Dependencies)

Dependencies can depend on other dependencies.

```python
def get_token(token: str = Header(...)):
    return token

def get_user(token=Depends(get_token)):
    return decode_token(token)
```

```python
@app.get("/secure")
def secure_endpoint(user=Depends(get_user)):
    return user
```

FastAPI builds a **dependency graph** and resolves it efficiently.

---

## 9. Caching Dependencies (`use_cache`)

By default, dependencies are **cached per request**.

```python
def get_settings():
    return Settings()
```

Used multiple times → executed once.

To disable caching:

```python
Depends(get_settings, use_cache=False)
```

Useful when:

* You need fresh data
* The dependency is stateful

---

## 10. Global Dependencies

You can apply dependencies to:

* An entire app
* A router
* A group of endpoints

```python
app = FastAPI(dependencies=[Depends(authenticate)])
```

```python
router = APIRouter(dependencies=[Depends(authenticate)])
```

Perfect for:

* Authentication
* Rate limiting
* Logging

---

## 11. Async Dependencies

FastAPI supports async dependencies naturally.

```python
async def get_redis():
    redis = await create_redis()
    try:
        yield redis
    finally:
        await redis.close()
```

FastAPI ensures:

* Proper awaiting
* Correct cleanup
* No event-loop misuse

---

## 12. Dependency Injection and Testing

You can **override dependencies** in tests.

```python
def fake_get_db():
    return FakeDB()
```

```python
app.dependency_overrides[get_db] = fake_get_db
```

This allows:

* No real DB
* No external services
* Fast and isolated tests

---

## 13. Common Anti-Patterns

❌ Creating resources inside endpoints
❌ Using globals instead of dependencies
❌ Putting business logic directly in routes
❌ Overusing dependencies for trivial values

---

## 14. Best Practices

* Keep endpoints thin
* Move logic into dependencies or services
* Use `yield` for resource management
* Depend on abstractions, not implementations
* Compose dependencies at the router/app level

---

## 15. Mental Model

Think of FastAPI dependencies as **request-scoped wiring**:

* Each request builds a dependency graph
* FastAPI resolves it top-down
* Cleanup happens automatically

You describe *what you need* — FastAPI handles *how and when* it’s provided.

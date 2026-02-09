# Concurrency & Parallelism in Python

Understanding threads, processes, async, and when to use each.

---

## Contents

| File | Topic | Description |
|------|-------|-------------|
| [threads_vs_processes_vs_async.md](threads_vs_processes_vs_async.md) | Overview | GIL, when to use threads vs processes vs async |
| [threads_and_processes.md](threads_and_processes.md) | Executors | `ThreadPoolExecutor`, `ProcessPoolExecutor`, `submit`, `map`, `as_completed` |
| [async_tutorial.md](async_tutorial.md) | Asyncio | Event loop, coroutines vs tasks, `TaskGroup`, `run_in_executor` |

---

## Reading Order

1. **Threads vs Processes vs Async** — understand the landscape and the GIL
2. **Threads and Processes** — learn the executor APIs
3. **Async Tutorial** — learn asyncio patterns

---

## Prerequisites

- Basic Python
- Understanding of I/O-bound vs CPU-bound work

## Next

After this section, proceed to:
- **[HTTPX Guide](../httpx/README.md)** — async HTTP in practice
- **[Safe API Calls](../fastapi/Safe_and_Scalable_API_calls/README.md)** — production concurrency patterns

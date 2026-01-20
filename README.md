# Python Backend Development Notes

A collection of practical notes and patterns for building backend applications with Python, focused on AI projects.

## 📚 Contents

### HTTP Clients
- **[HTTPX Guide](httpx/README.md)** - Comprehensive guide to HTTPX internals
  - [Mental Model](httpx/01_mental_model.md) - Request lifecycle, sockets, connection pools
  - [Connection Pooling](httpx/02_connection_pooling.md) - Pool limits and configuration
  - [Timeouts](httpx/03_timeouts.md) - Phase-based timeout configuration
  - [Advanced Features](httpx/04_advanced.md) - HTTP/2, streaming, error handling
  - [HTTPX vs aiohttp](httpx/05_httpx_vs_aiohttp.md) - When to choose which

### Core Concepts
- **[Decorators](core_concepts/decorators.md)** - Understanding Python decorators and their practical applications
- **[Exceptions](core_concepts/exceptions.md)** - Exception handling patterns and best practices
- **[Logging](core_concepts/logging.md)** - Comprehensive logging setup and configuration

### Concurrency & Parallelism
- **[Threads vs Processes vs Async](concurrency/threads_vs_processes_vs_async.md)** - When to use each approach
- **[Threads and Processes](concurrency/threads_and_processes.md)** - Detailed guide to ThreadPoolExecutor and ProcessPoolExecutor
- **[Async Tutorial](concurrency/async_tutorial.md)** - Understanding asyncio, event loops, and async patterns

### FastAPI
- **[Dependency Injection](fastapi/dependency_injection.md)** - Practical guide to FastAPI's built-in dependency injection system
- **[Safe and Scalable API Calls](fastapi/Safe_and_Scallable_API_calls/README.md)** - Production guide for calling LLMs and external services
  - [Part 1: Core Concepts](fastapi/Safe_and_Scallable_API_calls/01_core_concepts.md) - Mental models, the real concurrency limit
  - [Part 2: Concurrency & Timeouts](fastapi/Safe_and_Scallable_API_calls/02_concurrency_and_timeouts.md) - Timeout layers, asyncio vs httpx
  - [Part 3: Call Patterns](fastapi/Safe_and_Scallable_API_calls/03_call_patterns.md) - Gold standard pattern, retry logic
  - [Part 4: Kubernetes](fastapi/Safe_and_Scallable_API_calls/04_kubernetes.md) - Multi-pod concerns, local vs global
  - [Part 5: Production Architecture](fastapi/Safe_and_Scallable_API_calls/05_production_architecture.md) - Complete stack, execution order
  - [Part 6: Advanced Patterns](fastapi/Safe_and_Scallable_API_calls/06_advanced_patterns.md) - Circuit breakers, priority queues, load shedding
  - [Part 7: Streaming Patterns](fastapi/Safe_and_Scallable_API_calls/07_streaming_patterns.md) - SSE, streaming timeouts, semaphore duration
  - [Part 8: Streaming Advanced](fastapi/Safe_and_Scallable_API_calls/08_streaming_advanced.md) - Multi-stream, aggregation, partial recovery

### Background Tasks
- **[Background Tasks and Queues](background_tasks/background_tasks_and_queues.md)** - Celery vs FastAPI BackgroundTasks vs AsyncIOScheduler

---

## 📖 Reading Order

### For External API / LLM Calls

1. **Start with HTTPX** — Understand how the HTTP client works
   - Read [HTTPX Mental Model](httpx/01_mental_model.md)
   - Read [Connection Pooling](httpx/02_connection_pooling.md)
   - Read [Timeouts](httpx/03_timeouts.md)

2. **Then Safe API Calls** — Apply the knowledge to production systems
   - Read [Core Concepts](fastapi/Safe_and_Scallable_API_calls/01_core_concepts.md)
   - Read [Concurrency & Timeouts](fastapi/Safe_and_Scallable_API_calls/02_concurrency_and_timeouts.md)
   - Continue through the guide

---

## 🎯 Focus Areas

This repository focuses on patterns and practices for:
- Backend API development with FastAPI
- AI/ML project backends
- Production-ready code patterns
- Concurrency and parallelism
- Error handling and logging
- Background task processing

## 📝 Notes

These notes are written from a practical engineering perspective, focusing on:
- Real-world use cases
- Production considerations
- Common pitfalls and how to avoid them
- Mental models for understanding concepts

---

*Last updated: January 2026*

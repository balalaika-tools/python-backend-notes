# Python Backend Development Notes

A collection of practical notes and patterns for building backend applications with Python, focused on AI projects.

## 📚 Contents

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
- **[Production Guide: Safe and Scalable LLM & Agent Calls](fastapi/README.md)** - Comprehensive guide for safely calling LLMs and external services from FastAPI
  - [Part 1: Fundamentals](fastapi/01_fundamentals.md) - Core concepts, mental models, and foundational patterns
  - [Part 2: Production Implementation](fastapi/02_production_implementation.md) - FastAPI integration and production patterns
  - [Part 3: Kubernetes & Distributed Systems](fastapi/03_kubernetes_and_distributed_systems.md) - Multi-pod concerns and distributed thinking
  - [Part 4: Complete Production Architecture](fastapi/04_complete_production_architecture.md) - Full stack from API Gateway to vendor calls
  - [Part 5: Advanced Topics](fastapi/05_advanced_topics.md) - Pod-aware resilience patterns (circuit breakers, priority queues, adaptive retry)

### Background Tasks
- **[Background Tasks and Queues](background_tasks/background_tasks_and_queues.md)** - Celery vs FastAPI BackgroundTasks vs AsyncIOScheduler

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

*Last updated: 2025*

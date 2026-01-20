# HTTPX: Practical Guide to Async HTTP

> **Purpose**: Understand how HTTPX works at runtime before using it in production systems.

This guide explains HTTPX internals — **connection pooling**, **timeouts**, **HTTP/2**, and how this differs from aiohttp.

---

## Prerequisites

Basic understanding of:
- Python async/await
- TCP/HTTP fundamentals
- What a socket is

---

## Guide Structure

| File | Topic | Read if you need to understand... |
|------|-------|-----------------------------------|
| `01_mental_model.md` | Request lifecycle | What happens when you make a request |
| `02_connection_pooling.md` | Pool limits | How connections are reused and limited |
| `03_timeouts.md` | Phase-based timeouts | What each timeout controls |
| `04_advanced.md` | HTTP/2, streaming, errors | Advanced features and error handling |
| `05_httpx_vs_aiohttp.md` | Library comparison | When to choose which |

---

## Quick Reference

### Minimal Production Client

```python
import httpx

client = httpx.AsyncClient(
    limits=httpx.Limits(
        max_connections=50,
        max_keepalive_connections=10
    ),
    timeout=httpx.Timeout(
        connect=5.0,
        pool=5.0,
        write=10.0,
        read=30.0
    ),
    http2=True
)
```

### Key Concepts

| Concept | What it controls |
|---------|------------------|
| `max_connections` | Peak concurrent sockets |
| `max_keepalive_connections` | Idle sockets retained |
| `connect` timeout | DNS + TCP + TLS handshake |
| `pool` timeout | Waiting for free socket |
| `read` timeout | Response data reception |

---

## After This Guide

Once you understand HTTPX internals, proceed to:

**[Safe and Scalable API Calls Guide](../fastapi/Safe_and_Scallable_API_calls/)**

That guide builds on HTTPX knowledge to create production-grade external API call patterns.

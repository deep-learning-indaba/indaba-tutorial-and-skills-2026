# 03 / From Prototype to Production

*Deep Learning Indaba 2026 / Introduction to Agentic AI*

In notebooks `00` to `02` you built a small but complete memory-backed agent: an agent loop
with a tool, short-term memory you manage and compress, and persistent long-term memory with
vector embeddings. Everything ran locally, on open models, with no API key and nothing
leaving the machine.

This note connects those classroom patterns to what a production system adds on top, so you
can see that what you built is the genuine article, just smaller.

## The same four moves, at scale

Every memory-backed agent, however large, rests on the four moves from notebook `02`:
**embed, store, retrieve by similarity, augment the prompt.** Production mainly changes the
plumbing around them.

| Your prototype | A real production system |
|---|---|
| `all-MiniLM-L6-v2` embeddings | A managed or self-hosted embedding model |
| A Python list and a cosine loop | A vector database with a fast index, such as HNSW |
| `saga_memory.json` on disk | A store split into short-term (with a TTL) and permanent memory |
| Retrieve the top-k events | A context step that fetches several sources in parallel |
| One saga, a few events | Thousands of items and many concurrent users |

## What to add when you outgrow the notebook

1. **A real vector database.** Swap the in-memory list for Redis, Qdrant, or pgvector, and
   keep the same `add` and `search` interface so the rest of your code does not change.
2. **A short-term and long-term split.** Hold the current session in a cache with a
   time-to-live, and keep durable facts (a user's preferences, the world of the story) in a
   permanent store.
3. **Retrieval you can trust.** Measure whether the right memories come back, watch for
   stale or contradictory facts, and tune how many you inject.
4. **Operational basics.** Rate limits, latency budgets, caching, and a sensible cap on how
   much history you resend, because memory design is also cost design.

## The sovereignty angle

Everything in this tutorial runs on open models you can host yourself. That is the practical
core of the "sovereign intelligence" idea: you choose the infrastructure, you keep the data,
and you are not dependent on a single external provider or a metered API. A small open model
plus a local vector store is enough to build a real, useful, memory-backed agent that an
African team can own end to end, and scale up on its own terms.

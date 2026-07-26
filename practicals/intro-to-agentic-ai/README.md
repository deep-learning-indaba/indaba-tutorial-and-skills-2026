# Introduction to Agentic AI: Building Conversational Agents with Persistent Memory

**Deep Learning Indaba 2026 tutorial** (Sunday 02 August, 13:30 to 16:00).
**Session leader:** David Agbolade ([@dagbolade](https://github.com/dagbolade))

## Summary

A hands-on, code-forward tutorial for undergraduates from any ML background. You build a
conversational agent from scratch in Python, give it a tool and both short-term and persistent
long-term memory (with vector embeddings), and run the whole thing on small open models with no
API key. To make the ideas stick, the agent is a **griot**, a storyteller that must remember an
evolving folktale across turns and across sessions. It doubles as a concrete take on the Indaba
theme, *Sovereign Intelligence*: agents you can host and own yourself.

## Notebooks (recommended order)

| Notebook | What you do | Open in Colab |
|---|---|---|
| [`00_minimal_agent.ipynb`](00_minimal_agent.ipynb) | Build a minimal agent: model, instructions, a tool, in-session memory | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deep-learning-indaba/indaba-tutorial-and-skills-2026/blob/main/practicals/intro-to-agentic-ai/00_minimal_agent.ipynb) |
| [`01_short_term_memory.ipynb`](01_short_term_memory.ipynb) | Manage the story history, watch the context window fill, then summarise | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deep-learning-indaba/indaba-tutorial-and-skills-2026/blob/main/practicals/intro-to-agentic-ai/01_short_term_memory.ipynb) |
| [`04_agent_tools.ipynb`](04_agent_tools.ipynb) | Give the agent a real tool: a live weather API (no key) it calls for current data | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deep-learning-indaba/indaba-tutorial-and-skills-2026/blob/main/practicals/intro-to-agentic-ai/04_agent_tools.ipynb) |
| [`02_vector_memory.ipynb`](02_vector_memory.ipynb) | Persistent long-term memory with embeddings; the saga survives a restart | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/deep-learning-indaba/indaba-tutorial-and-skills-2026/blob/main/practicals/intro-to-agentic-ai/02_vector_memory.ipynb) |
| [`03_from_prototype_to_production.md`](03_from_prototype_to_production.md) | How these patterns scale to a real system (read, not run) | (n/a) |

## How to run

- **Colab (easiest):** click an *Open in Colab* badge and choose *Run all*. For speed, enable a
  GPU first (Runtime > Change runtime type > T4). There is no API key; the first cell downloads a
  small open model.
- **Locally:** `pip install -r requirements.txt`, then `jupyter lab`.

## Models used

`Qwen/Qwen2.5-0.5B-Instruct` (text) and `all-MiniLM-L6-v2` (embeddings). Both are open, free, and
download automatically on first run. No large files are committed.

## Slides

[`Introduction-to-Agentic-AI-slides.pdf`](Introduction-to-Agentic-AI-slides.pdf)

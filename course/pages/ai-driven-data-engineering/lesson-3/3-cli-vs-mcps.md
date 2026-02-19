---
title: "Lesson 3: CLI vs MCPs"
module: 'ai_driven_data_engineering'
lesson: '3'
---

# CLI vs MCPs

Like many others, we experimented with an **MCP (Model Context Protocol) server** when it looked like MCP might become the primary interface for AI assistants. MCPs can serve a purpose—exposing tools and context to the model in a structured way—but we’ve found that **CLIs often work better than MCPs** for the kind of workflows we care about.

---

## Why we favor a quality CLI

**CLIs give you high quality with less surface area.** LLMs tend to go off the rails when they’re given too much context or too many overlapping tools. A well-designed CLI:

- **Narrows the action space** — The agent chooses from a small set of commands (`dg scaffold`, `dg check`, `dg list`, `dg launch`) instead of reasoning over arbitrary file edits and API calls.
- **Encodes best practices** — Scaffolding and validation are implemented once in the CLI, so the agent doesn’t have to “know” our project layout or validation rules from long docs.
- **Is easy to validate** — Exit codes and stdout are simple to parse and assert on, in both human and automated evaluation.
- **Reduces context and token usage** — A CLI doesn’t require the model to load large schemas, API docs, or tool descriptions. The agent gets a compact set of commands and short help; responses are typically small (exit code + stdout). That means less context in the prompt and far fewer tokens per interaction than a broad MCP tool set with rich payloads and documentation.

So we invest in making **`dg`** a solid, opinionated CLI and have our skills teach the agent when and how to use it, rather than relying on a large MCP surface that could overload the model.

---

## When MCPs still help

MCPs can still be useful for things like exposing a running Dagster instance’s state or serving dynamic context. For the core loop of “scaffold → edit → check → list → launch,” we’ve found that a **good CLI + skills that reference it** keeps behavior more reliable and easier to evaluate than a big MCP tool set.

In short: we use a **quality CLI as the main interface** for agents working with Dagster projects, and use skills to guide the agent to that CLI instead of to a broad, high-context MCP surface.

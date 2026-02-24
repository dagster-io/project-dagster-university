---
title: "Lesson 7: Subagents and context isolation"
module: 'ai_driven_data_engineering'
lesson: '7'
---

# Subagents and context isolation

Every Claude conversation has a context window—a limit on how much it can hold in active memory at once. For a long, complex session, earlier details get compressed as the conversation grows. This is fine for most work, but it means that in a large implementation, the agent's recall of decisions made early in the session may be less precise by the end.

Subagents solve a different problem than plan mode does. Plan mode handles complexity within a single task. Subagents handle situations where two genuinely independent workstreams would otherwise be sequential: you'd finish one completely before starting the other.

---

## What a subagent is

A subagent is an isolated agent process that runs concurrently with the main conversation. It starts fresh—no prior conversation history—and works on its assigned task independently. Its output is returned to the main agent when complete.

This has two practical benefits:

**Context isolation** — the subagent's work doesn't consume the main context window. If the subagent reads 20 files and writes detailed test code, none of that occupies space in the main conversation.

**Parallelism** — the subagent runs concurrently. Work that would otherwise be sequential—finish implementation, then write tests—becomes simultaneous.

---

## When subagents are worth using

The right time to launch a subagent is when a workstream is:

- Large enough to meaningfully consume context (reading many files, writing substantial code)
- Independent enough that it doesn't need the main agent's in-progress output

If a task is small or tightly coupled to the main agent's current work, a subagent adds overhead without benefit. The value is specifically in separating workstreams that are genuinely independent.

---

## Example: Implementation and testing in parallel

Consider asking for the NewsAPI integration *and* tests at the same time:

```
Implement the NewsAPI integration and write tests for the new resource and asset in parallel.
```

From a single message:

1. **Main agent** — begins implementation: writes all 8 files, runs `uv sync`, validates with `dg check defs`
2. **Background subagent** — launched simultaneously with a focused prompt: "Write pytest tests for `NewsApiResource.get_client()` and the `trending_events` asset, following the existing test patterns in `tests/`"

The subagent only needs the *design* to write tests—the interface for `NewsApiResource` and the asset contract—not the implementation files themselves. It can start immediately, from a clean context, in parallel with the main agent's writes.

What each context holds:

```
Main agent context                  Subagent context
─────────────────────────────────   ─────────────────────────────────
Full conversation history           Fresh start — design brief only
8 file writes                       Test file research + writing
uv sync output                      Existing test patterns
dg check defs output                pytest fixtures and mocks
                                    Final test file
```

By the time the main agent finishes validation, the subagent returns a complete test file. The main agent reviews it, places it in `tests/`, and runs `pytest`—no sequential waiting required.

---

## The core value

Implementation and testing are normally sequential phases: you finish the code, then you write tests for it. With a subagent, they become parallel workstreams with isolated contexts. Neither pollutes the other, and the total time is closer to the longer of the two rather than their sum.

This is the same principle as parallel file writes within a single plan, scaled up to entire workstreams. When you can describe the interface clearly enough that another agent can work from the design alone, the two workstreams can proceed simultaneously.

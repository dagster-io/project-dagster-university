---
title: "Lesson 8: Parallel sessions and context isolation"
module: 'ai_driven_data_engineering'
lesson: '8'
---

# Parallel sessions and context isolation

Every AI agent conversation has a context window -- a limit on how much it can hold in active memory at once. For a long, complex session, earlier details get compressed as the conversation grows. This is fine for most work, but it means that in a large implementation, the agent's recall of decisions made early in the session may be less precise by the end.

Parallel sessions solve a different problem than plan mode does. Plan mode handles complexity within a single task. Parallel sessions handle situations where two genuinely independent workstreams would otherwise be sequential: you'd finish one completely before starting the other.

## What a parallel session is

A parallel session is a separate agent conversation you start alongside your main one. It begins fresh (no prior conversation history) and works on its assigned task independently. When it finishes, you bring the output back into the main session manually.

This has two practical benefits:

**Context isolation**: the parallel session's work doesn't consume the main context window. If it reads 20 files and writes detailed test code, none of that occupies space in the main conversation.

**Parallelism**: while the main session is writing implementation files, the parallel session can work simultaneously. Work that would otherwise be sequential becomes concurrent.

## When parallel sessions are worth using

The right time to open a parallel session is when a workstream is:

- Large enough to meaningfully consume context (reading many files, writing substantial code)
- Independent enough that it doesn't need the main session's in-progress output

If a task is small or tightly coupled to what the main session is doing, a second session adds switching overhead without much benefit. The value is specifically in separating workstreams that are genuinely independent.

## Example: Implementation and testing in parallel

Consider asking for the NewsAPI integration *and* tests at the same time. Rather than finishing the implementation and then writing tests sequentially, you can run both simultaneously.

Open your main session and a parallel session at the same time. Give the main session the full implementation task. Give the parallel session a focused prompt:

```text
Write pytest tests for `NewsApiResource.get_client()` and the `trending_events` asset,
following the existing test patterns in `tests/`. The resource will have an `api_key`
field and a `get_client()` method returning an `EventRegistry` instance. The asset will
write to a `trending_events` table in DuckDB with daily partitions.
```

The parallel session only needs the *design* to write tests: the interface for `NewsApiResource` and the asset contract, not the implementation files themselves. It can start from the same planning output the main session is working from.

What each context holds:

```text
Main session context                Parallel session context
─────────────────────────────────   ─────────────────────────────────
Full conversation history           Fresh start -- design brief only
8 file writes                       Test file research + writing
uv sync output                      Existing test patterns
dg check defs output                pytest fixtures and mocks
                                    Final test file
```

By the time the main session finishes validation, the parallel session has returned a complete test file. You review it, place it in `tests/`, and run `pytest`. No sequential waiting required.

## The core value

Implementation and testing are normally sequential phases: you finish the code, then you write tests for it. With a parallel session, they become concurrent workstreams with isolated contexts. Neither pollutes the other, and the total time is closer to the longer of the two rather than their sum.

This is the same principle as parallel file writes within a single plan, scaled up to entire workstreams. When you can describe the interface clearly enough that a second session can work from the design alone, the two workstreams can proceed simultaneously.

## The writer/reviewer pattern

Parallel sessions are also useful for a different kind of isolation: code review that carries no bias toward the code being reviewed.

When the agent that wrote the code also reviews it, it tends to find what it was looking for: validation of the approach it already chose. A fresh session, given the same file and no prior involvement, reads it without anchoring to the original intent. It's more likely to catch convention violations, unexpected patterns, or decisions that looked reasonable in context but read strangely from the outside.

The pattern is straightforward:

**Session A (writer):** implements the feature, validates with `dg check defs`, commits

**Session B (reviewer):** starts fresh, receives the relevant files and a focused review prompt:

```text
Review defs/assets/trending_events.py and defs/resources.py for the following:
- Does the asset use the _make_raw_asset() factory (not a direct function definition)?
- Are there any hardcoded values that should come from environment variables or resources?
- Does the resource follow the same pattern as the other resources in resources.py?
- Any DuckDB connections instantiated outside of the DuckDBResource?
```

The reviewer has no memory of the implementation session, no attachment to any particular approach, and no context noise from debugging rounds. Its only job is to read the code against explicit criteria.

You can also run a reviewer in parallel with the end of an implementation session: while Session A finishes validation, open Session B to review the already-written files. By the time the main session is ready to commit, the review is complete.

The writer/reviewer split is particularly useful in Dagster projects because convention violations are subtle: a raw asset that works correctly but skips the factory pattern, a resource that's structured correctly but uses a different naming convention than the rest. Those won't surface in `dg check defs`. They require deliberate review against project conventions.

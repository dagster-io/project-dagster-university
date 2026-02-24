---
title: "Lesson 8: Signs of degradation"
module: 'ai_driven_data_engineering'
lesson: '8'
---

# Signs of degradation

Recall degradation is observable. The signals are specific enough that you can recognize them as they happen—not just in hindsight.

These examples are grounded in the course project, but the patterns generalize to any working session.

---

## Re-asking for information it already has

Early in the session, you told the agent where the DuckDB database lives: `data/staging/data.duckdb`. Fifteen exchanges later, it asks again—or defaults to a different path without asking.

Same with the `trending_events` table schema. If the agent re-reads `stg_trending_events.sql` to check the column names it already verified, that's a signal. It's not wrong to re-read files, but if it's re-reading things it demonstrably had in context, earlier details are getting crowded out.

---

## Fixes that regress

You corrected a pattern in exchange 8: the agent was skipping the `_make_raw_asset()` factory and writing raw asset definitions directly. It acknowledged the correction and fixed the file.

In exchange 22, new code appears without the factory again.

This is the clearest signal. A pattern the agent had right—and explicitly confirmed—has drifted back to the earlier incorrect version. The correction is still in the history, but the context around it has been compressed enough that it's not influencing new output at the same weight.

---

## Inconsistent descriptions of project state

The agent describes `NewsApiResource` as having a `get_client()` method in one message, then refers to it as `get_session()` two exchanges later. Nothing changed. The project is in the same state. The inconsistency is coming from imprecise recall of the resource's interface.

This matters because inconsistent descriptions of your own project state often precede inconsistent code: the agent will write a call to `get_session()` in a new asset, which won't match the actual method name.

---

## Hedging on project-specific details

A reliable indicator: the agent starts qualifying statements about your specific project.

- "I believe the resource was named `NewsApiResource`..."
- "The DuckDB path should be around `data/staging/`..."
- "If I recall correctly, the schedule was configured for daily..."

These hedges mean the agent is uncertain about facts it knew precisely earlier. It's not making things up—it's flagging that it can't retrieve the detail with confidence. That uncertainty is worth taking seriously.

---

## New code drifting from established conventions

The project has clear conventions: the `_make_raw_asset()` factory for raw assets, the DuckDB connection pattern via `DuckDBResource`, the staging path structure. These conventions were established and followed consistently early in the session.

Later in the session, new code that should follow these conventions starts to drift: the factory is skipped, the connection is instantiated differently, the path format changes. The conventions still exist in the codebase—the agent could read them if it re-read the files—but it's generating from memory rather than from the current source.

---

## What to do when you see these signals

Seeing one of these signals doesn't mean the session is unusable. It means you should take stock:

- How far into the session are you?
- Is the task you're on now related to what you started with?
- Would starting fresh and pasting a handoff summary get you to the same place faster?

The next page covers when to make that call and how to carry state forward cleanly.

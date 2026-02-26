---
title: "Lesson 6: Session habits"
module: 'ai_driven_data_engineering'
lesson: '6'
---

# Session habits

These habits keep sessions productive by preventing the accumulation patterns that degrade recall. They're not rules—they're the cost-benefit reasoning behind each decision.

## One task per session

The most effective habit: finish one task, validate it, commit it, then start fresh.

A session that starts with "add the `trending_events` asset" should end when `dg check defs` is passing and the changes are committed. The next task—adding a sensor, extending the dbt project, fixing a failing test—belongs in a new session.

This isn't about being rigid. It's about avoiding the accumulated noise that builds when a session spans multiple tasks: the stack trace from a debug that's now resolved, the file reads for a task that's long done, the revised decisions that don't apply to the current work. None of that helps the current task. It only occupies context that the current task needs. Starting a new session also keeps token usage lower than continuing a long, noisy one—so the habit helps both quality and cost.

## Keep validation loops short

Each `dg check defs` cycle is a natural checkpoint. After the agent writes code and you validate it, you have a clean decision point: continue in this session or start a new one.

If the validation passes cleanly, the task is probably done. Commit and start fresh.

If the validation fails and the fix is straightforward, stay in the session—the debugging context is exactly what the fix needs.

If the validation fails and the debugging has been going on for several exchanges without resolution, consider whether starting fresh with a focused prompt ("this specific `dg check defs` error...") would be faster than continuing in a session that's accumulated noise.

## Avoid backtracking in long sessions

Backtracking—reversing a decision made several exchanges ago—is expensive in a long session. The earlier decision is in context, the reversal is in context, and the new approach is building on top of both. That layering makes it harder for the agent to track which version of the decision is current.

If you catch a bad decision early (within a few exchanges), reversal is clean. The session hasn't built much on top of the wrong choice.

If you're reversing a decision from many exchanges ago, ask: is it cleaner to reverse in this session, or to start fresh and bring only the correct approach forward? Starting fresh doesn't lose progress—it loses noise.

## When to start fresh

This is a cost-benefit decision, not a rule. Start fresh when:

**A new unrelated task begins.** If the next thing you're doing has no direct connection to what you just finished, there's no reason to carry the history of the finished task. Start clean.

**You're reversing an early decision.** If the approach from exchange 5 is being undone in exchange 25, the session has accumulated 20 exchanges of context built on a foundation that's being replaced. Starting fresh with the correct approach is usually cleaner.

**The agent has shown inconsistent recall.** If you've seen two or three of the degradation signals from the first page of this lesson ("What is context")—hedging, regressions, inconsistent descriptions—the session has accumulated enough noise that continuing is likely to produce more of the same. The cost of starting fresh is small; the cost of unreliable output is higher.

**Debugging has generated significant noise.** Stack traces, failed attempts, dead ends. If the debugging session produced a lot of irrelevant history and the issue is now resolved, starting fresh for the fix (rather than applying it in the noisy session) gives the agent a cleaner context for the actual change.

## Carrying context forward: the handoff pattern

Starting fresh doesn't mean losing progress. The handoff pattern lets you compress what matters and bring it forward cleanly.

Before closing a long session, ask the agent to produce a structured summary:

```
Before we close, produce a session handoff summary:
- What was built or changed in this session
- Key decisions made and the reasoning
- The current state of the project
- What the next task is and what context it needs
```

Open the new session with that summary as your first message. The new session starts with exactly the context it needs—no noise, no dead ends, no debugging history.

### Example handoff summary

This is what a handoff summary looks like using the actual project:

```
Session handoff — NewsAPI integration

What was built:
- NewsApiResource added to resources.py with api_key field and get_client() returning
  an EventRegistry instance
- trending_events asset added to defs/assets/trending_events.py using _make_raw_asset()
  factory pattern (same as existing raw assets)
- raw job split into two jobs in daily_raw.py: one for CSV assets, one for trending_events
- Daily partitioned schedule added for trending_events
- dbt staging model (stg_trending_events.sql) and source registration added

Key decisions:
- Used EventRegistry (eventregistry library) rather than direct HTTP requests
- _make_raw_asset() factory used for consistency with existing assets — skipping it was
  corrected in this session, factory is required for new raw assets
- DuckDB path: data/staging/data.duckdb (same convention as all other raw assets)

Current state:
- dg check defs passing
- uv sync completed, eventregistry installed
- Changes committed: "Add NewsAPI trending_events integration"

Next task:
- Add dbt tests for stg_trending_events beyond the existing not_null checks
- Suggested start: /dagster-integrations Add referential integrity and accepted_values
  tests to stg_trending_events in schema.yml
```

The new session opens with this and immediately has the full picture: what exists, what decisions were made (and which ones were corrected), the current state, and what to do next. No re-reading files to reconstruct project state, no re-explaining conventions.

## The handoff is a compressed state snapshot

A good handoff isn't a full replay of the session. It's a snapshot of current state: what decisions are in effect, what the project looks like right now, what comes next. The session history that produced that state isn't useful to a new agent—the outcome of that history is.

Write the handoff to be useful to someone who wasn't in the session. If you can read it and know exactly where to start, it's complete.

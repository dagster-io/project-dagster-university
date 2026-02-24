---
title: "Lesson 4: Debugging strategies"
module: 'ai_driven_data_engineering'
lesson: '4'
---

# Debugging strategies

The debugging page earlier in this lesson showed one specific pattern: a DuckDB path error, fixed in the resource with the skill's help. That pattern—give the error to the agent, use the right skill, fix in the right place—covers many cases. But debugging goes wrong in predictable ways, and knowing how to handle them keeps the workflow moving.

---

## Structure the error for the agent

An unstructured debugging prompt ("something broke, can you fix it") forces the agent to diagnose before it can fix. Give it what it needs directly:

- The full error text (not a paraphrase)
- Which command produced it and where in the output the error appeared
- What you expected to happen

```
/dagster-expert Running dg launch --assets trending_events gives this error:

  AttributeError: 'NewsApiResource' object has no attribute 'get_session'

The resource is defined in resources.py and should have a get_client() method.
The asset is calling get_session() by mistake.
```

This prompt tells the agent where to look (`NewsApiResource` in `resources.py`), what the correct state is (`get_client()`), and what's wrong (`get_session()` in the asset). It can go directly to the fix rather than reading every file to reconstruct the situation.

---

## Confirm first, then fix

For errors that aren't immediately obvious, ask the agent to confirm it can reproduce the problem before changing anything:

```
/dagster-expert Before fixing anything, run dg check defs and show me the output.
I want to confirm we're looking at the same error.
```

This matters when the error description is ambiguous, or when you want to verify that the session's picture of the project state is accurate. If `dg check defs` shows a different error than you described, something is out of sync—better to catch that before the agent starts making changes.

---

## Use `dg list defs` as a diagnostic tool

When the error is at the definitions level rather than the runtime level—an asset isn't appearing in the UI, a schedule isn't being picked up—`dg list defs` tells you what Dagster thinks is registered:

```bash
dg list defs
```

Ask the agent to run this and interpret the output if what you see in the UI doesn't match what you expect in the code. Discrepancies between "what's in the file" and "what `dg list defs` shows" usually point to a registration problem (missing from `Definitions`, wrong `__init__.py`, import error suppressed somewhere).

---

## When debugging is circular

If you've made three different changes and the error hasn't moved, stop and reassess. The problem is probably not where you've been looking.

Signs that debugging has become circular:
- The same error appears after different fixes
- The agent keeps suggesting variations of approaches that haven't worked
- You've lost track of which changes are currently in place and which were reverted

When this happens, the most effective move is to reset. Undo changes back to the last known-good state (the last `dg check defs` passing), then approach the problem with a fresh diagnostic prompt rather than a fix prompt:

```
/dagster-expert I'm getting this error when I run the trending_events asset.
Before suggesting any fixes, explain what could cause it and where to look.
```

Getting the agent to explain the problem first—rather than jumping to a fix—often surfaces the real cause. Fixes to the wrong place don't surface the right cause.

---

## Debugging and session state

Long debugging sessions accumulate noise: stack traces, failed attempts, reverted changes, "try this instead" exchanges. That history doesn't help the current fix—it occupies context that the fix needs.

Once you've solved a debugging problem, consider whether to continue in the same session or start fresh. If the fix is small and the session is short, continue. If the session has accumulated several rounds of wrong approaches, apply the fix in a fresh session: open new, paste the handoff summary plus the error and its solution, make the targeted change, validate, commit. The fix lands cleanly without carrying the debugging noise into the project history.

This isn't a rule—it's a cost-benefit judgment the same way all session management decisions are.

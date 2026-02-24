---
title: "Lesson 8: How context fills up"
module: 'ai_driven_data_engineering'
lesson: '8'
---

# How context fills up

You already know what a context window is from the subagents lesson. The relevant point there was that subagents use a fresh context so they don't consume the main conversation's space. This lesson is about what happens inside the main conversation across a real working session.

---

## What accumulates

A session doesn't just grow with your messages and the agent's replies. Everything the agent reads or writes becomes part of the context:

**File reads** — when the agent reads `resources.py` to understand how resources are structured, that file's contents are now in context. If it reads `schema.yml`, `sources.yml`, and three asset files to plan an implementation, all of that is present.

**Code writes** — when the agent writes a new asset, the full file content enters the context along with the write confirmation. If it writes 8 files, all 8 are part of the history.

**Validation output** — `dg check defs` produces multi-line output. When you paste that output into the conversation, or the agent runs it and reads the result, that output occupies context space. Stack traces are especially large.

**Dead ends** — if the agent tries an approach, it fails, and you correct course, the failed attempt is still in context. The reversal is recorded, but the original approach doesn't disappear.

**Revised decisions** — "actually, let's use a monthly partition instead of daily" adds an instruction and a prior plan to the history. Both are still visible.

---

## What this means in practice

For a short session—one focused task, a few exchanges—none of this matters. The context is lightly loaded and the model has clear access to everything.

For a longer session—multiple tasks, several rounds of debugging, some backtracking—the picture is different. Earlier file reads and decisions are still technically in context, but they're compressed and weighted less heavily than recent content. The model can still work from them, but recall is less precise.

This isn't a failure mode—it's the expected behavior of a context that has grown. The practical question is: at what point does that degradation meaningfully affect the quality of the work?

---

## The gradient

The shift isn't sudden. A session doesn't cross a threshold where everything falls apart. It's a gradient:

- Short session (one task, a few exchanges): full recall, consistent output
- Medium session (2-3 tasks, some debugging): mostly reliable, occasional hedging on specifics
- Long session (many tasks, multiple reversals, accumulated noise): measurably less reliable on early details

Knowing the gradient exists is what lets you act before the degradation becomes a problem rather than after.

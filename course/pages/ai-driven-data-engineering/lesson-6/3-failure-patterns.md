---
title: "Lesson 6: Common session failure patterns"
module: 'ai_driven_data_engineering'
lesson: '6'
---

# Common session failure patterns

Good session habits prevent degradation. But degradation can also develop because of specific patterns that are easy to fall into and hard to notice from inside the session. These patterns have predictable shapes—naming them makes them easier to self-diagnose before they compound.

---

## Kitchen sink session

**What it looks like:** A single session starts with "add the `trending_events` asset," and three hours later it also contains: a debugging round for the DuckDB path, a refactor of `resources.py`, a question about partitions, and the start of a new dbt model.

**Why it's a problem:** Each completed task leaves residue—file reads, stack traces, revised decisions, resolved errors. That residue doesn't help the current task. It occupies context that the current task needs, and it gives the agent an increasingly blurry picture of what "the current state" actually is.

**The tell:** You're explaining the current state of the project to the agent as if reminding it of something, not building on shared context.

**Reset:** One task per session. When `dg check defs` passes and you've committed, the task is done. The next task starts in a new session.

---

## Correction loop

**What it looks like:** The agent produces code with a pattern you've already corrected twice. You correct it again. It acknowledges and fixes it. In the next message, the same pattern appears.

**Why it's a problem:** The correction is in context, but it's being outweighed by earlier content or by the agent generating from a compressed version of the session. You're spending energy on the same correction instead of making forward progress.

**The tell:** You've written "like I mentioned earlier" or "again, please use the factory pattern" more than once in the same session.

**Reset:** Stop correcting in-session. Use `/clear` to drop the conversation history (keeping the current file state), or start a fresh session and lead with the correction as a standing constraint in the opening prompt. If the correction is structural, lead with it as a constraint in the opening prompt of every new session rather than correcting it repeatedly mid-session.

---

## Trust-then-verify gap

**What it looks like:** The agent returns code that looks right. The file structure matches, the logic seems reasonable, and you move on. Two tasks later, you discover the asset was never registered in `Definitions`, or the resource is missing a field, or `dg check defs` would have caught something you didn't run.

**Why it's a problem:** Plausible-looking output is not the same as correct output. The agent can produce code that passes a quick visual scan but fails at load time. The longer the delay between code generation and validation, the harder it is to identify which change caused the problem.

**The tell:** You're running `dg check defs` reactively (when something breaks) rather than as a routine step after every implementation.

**Reset:** Run `dg check defs` after every substantive change. Include it as a step in the prompt itself (see the prompting lesson). Don't commit code you haven't validated.

---

## Infinite exploration

**What it looks like:** You ask the agent to "investigate why the schedule isn't running" or "explore whether partitions would help here." The agent reads a dozen files, reasons through several possibilities, and produces a long analysis—most of which isn't actionable.

**Why it's a problem:** Open-ended investigation tasks have no natural stopping point. The agent keeps reading and reasoning until context pressure forces it to stop. The result is a context-heavy session with a diffuse output that's hard to act on.

**The tell:** The agent's response is longer than the task warrants, covers multiple hypotheses without recommending one, or keeps re-reading files you've already discussed.

**Reset:** Scope investigation prompts explicitly. "Before suggesting fixes, tell me the three most likely causes of this error" is better than "investigate this error." Or use a subagent for the investigation so it doesn't consume the main context window—get the findings, then decide what to act on.

---

## Using the patterns

These patterns aren't failure modes reserved for bad sessions. They're tendencies that develop naturally in any working session, especially ones that span more than an hour or more than one task. The value of naming them is not to avoid them entirely but to recognize them earlier—before a single correction loop turns into ten, or a kitchen sink session turns into one you have to abandon and reconstruct.

The degradation signals from the first page of this lesson ("What is context") tell you the session *is* degrading. These patterns tell you *why* it's degrading and what to do about it.

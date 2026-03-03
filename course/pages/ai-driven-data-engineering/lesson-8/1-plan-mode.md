---
title: "Lesson 8: Plan mode"
module: 'ai_driven_data_engineering'
lesson: '8'
---

# Plan mode

Plan mode is an explicit instruction to the agent: design the approach first, don't write code yet. You enter it by asking:

```text
Before implementing, draft a plan for adding a NewsAPI integration.
```

The agent will read the relevant files, identify everything that needs to change, and present a step-by-step implementation strategy. It waits for your approval before writing anything.

## When to use it

Not every task needs a plan. For small, reversible changes (renaming a variable, fixing a typo, adding a single field), plan mode adds overhead without value.

The signal is complexity and reversibility. Use plan mode when:

- **The task touches more than 2-3 files**: the more files involved, the more likely an inconsistent choice in one propagates to others
- **Multiple approaches are valid**: if there are real trade-offs between approaches, you want to choose before implementation is underway
- **Architectural decisions are involved**: new resources, new integration patterns, schema changes that affect downstream models
- **You want to understand the blast radius**: before committing to changes that are hard to undo

The harder something is to reverse, the more valuable upfront planning becomes.

## What it looks like in practice

A typical plan-mode session has a clear shape:

1. You describe the task and ask for a plan first
2. The agent reads the relevant files (resources, assets, schedules, dbt models) without changing any of them
3. It produces a structured plan: every file that needs to change, what changes in each, and any dependencies between them
4. You review, ask questions, or redirect if the approach isn't what you wanted
5. You approve, and the agent begins implementation

This upfront review is valuable precisely because it happens before anything is written. If the plan surfaces a decision you hadn't considered (do we want daily or hourly partitions? should the new resource go in `resources.py` or a new file?), resolve it at planning time, not mid-implementation when reverting is messier.

## The key constraint

Plan mode only works if you ask for it explicitly. The agent won't automatically pause before complex tasks; it will proceed with implementation unless you tell it otherwise.

Treat it as a habit for any task where you'd feel uncomfortable if the agent just started writing. If you wouldn't want to see the code before reviewing the approach, ask for the plan first.

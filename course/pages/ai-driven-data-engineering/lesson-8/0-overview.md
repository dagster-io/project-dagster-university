---
title: "Lesson 8: Overview — Complex tasks with plan mode and subagents"
module: 'ai_driven_data_engineering'
lesson: '8'
---

# Overview

The workflow so far has been mostly conversational: describe what you want, let the agent write the code, run `dg check defs` to verify. That pattern works well for focused tasks—adding an asset, tweaking a schedule, fixing a type error. The agent can hold the full picture in a single exchange.

But some tasks don't fit that shape. Adding a new data integration might touch 8 files at once. Refactoring the project structure might require making decisions across resources, assets, schedules, and dbt models simultaneously. For tasks like these, jumping straight into code generation creates risk: the agent may make inconsistent choices across files, or you may realize mid-implementation that you wanted a different approach.

This lesson covers two tools for handling that complexity:

**Plan mode** — a way of asking the agent to explore the codebase and design an implementation strategy *before* writing any code. The agent maps out every file that needs to change, identifies dependencies between changes, and presents the plan for your review. Only after you approve does it begin writing.

**Subagents** — isolated agent processes that run concurrently with the main conversation. They let you parallelize genuinely independent workstreams (like implementation and testing) while keeping each context focused on one thing.

These aren't advanced features reserved for large teams or complex infrastructure. They're practical habits for any task where the blast radius is large enough that you want to see the plan before it runs.

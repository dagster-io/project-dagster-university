---
title: "Lesson 8: Complex tasks with plan mode and parallel sessions"
module: 'ai_driven_data_engineering'
lesson: '8'
---

# Overview

The workflow so far has been mostly conversational: describe what you want, let the agent write the code, run `dg check defs` to verify. That pattern works well for focused tasks, such as adding an asset, tweaking a schedule, or fixing a type error. The agent can hold the full picture in a single exchange.

But some tasks don't fit that shape. Adding a new data integration might touch 8 files at once. Refactoring the project structure might require making decisions across resources, assets, schedules, and dbt models simultaneously. For tasks like these, jumping straight into code generation creates risk: the agent may make inconsistent choices across files, or you may realize mid-implementation that you wanted a different approach.

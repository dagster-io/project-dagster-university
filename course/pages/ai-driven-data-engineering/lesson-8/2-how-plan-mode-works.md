---
title: "Lesson 8: How plan mode works"
module: 'ai_driven_data_engineering'
lesson: '8'
---

# How plan mode works

A plan-mode session has two distinct phases before any code is written: exploration and planning. Understanding what happens in each makes it easier to evaluate whether the plan is good before approving it.

## Phase 1: Exploration

The agent reads the codebase to understand the patterns already in use.

For a Dagster project, that typically means reading how resources are defined and registered, how existing assets are structured, what the dbt layer looks like, and how schedules reference jobs and assets. This isn't just to understand what exists; it's to ensure new code is consistent with what's already there.

A plan built without this exploration risks inventing patterns that conflict with the existing project structure. Exploration is what makes the plan coherent with the codebase rather than coherent in isolation.

## Phase 2: Planning

With the codebase understood, the agent maps out the full implementation:

- Every file that needs to change and what changes in each
- Which changes are independent of each other
- Which changes must wait for another step to complete

The output is effectively a dependency graph, even when it isn't drawn explicitly. The key distinction is between two kinds of changes:

**Independent changes**: files that don't depend on each other's output can be written simultaneously. If the design is fully known at planning time (the interface for a new resource, the DuckDB table schema, the partition definition), there's no reason to write the files one at a time.

**Sequential changes**: validation steps like `dg check defs` or `dbt compile` must wait until the files they validate are complete. These can't be parallelized with the file writes because they depend on them.

## File writes and validation are different phases

This is the key insight for complex tasks: *writing* files and *validating* files are distinct phases with different dependencies.

All file writes can often happen in parallel: the design is fully known from the plan, so there's nothing to discover mid-write that would change another file. Validation is then a single sequential pass at the end.

This isn't just faster; it's also easier to reason about. If validation fails after all writes are complete, you know exactly which files are in scope. There's no ambiguity about which write introduced the problem.

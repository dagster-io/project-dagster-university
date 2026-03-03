---
title: "Lesson 6: Code quality with dignified-python"
module: 'ai_driven_data_engineering'
lesson: '6'
---

# Overview

In earlier lessons we improved code quality along the way. The last Dagster skill worth discussing is `dignified-python`: a collection of our internal best practices and philosophies as they relate to Python.

These patterns influence the Dagster codebase but can be applied to any Python codebase. This lesson covers what the skill does, what some of the rules look like, how to use it on the code you’ve written, how it differs from (and works with) traditional linters like Ruff, and how to apply test-driven development to verify agent output with running assertions rather than visual inspection.

---
title: "Lesson 6: Overview — Managing AI sessions"
module: 'ai_driven_data_engineering'
lesson: '6'
---

# Overview

AI sessions degrade over time. Context fills with file reads, stack traces, and revised decisions—most of which aren't relevant to the current task. Understanding this gradient, recognizing when it's affecting output, and managing sessions accordingly is what separates productive multi-hour work from sessions that produce inconsistent results.

This lesson covers three things. First, how context windows actually work and what accumulates as a session grows. Second, the habits that keep sessions productive: one task per session, short validation loops, and the handoff pattern for carrying context forward without carrying noise. Third, the failure patterns that develop naturally in working sessions—kitchen sink sessions, correction loops, the trust-then-verify gap, and infinite exploration—and how to recognize and reset from each.

These habits apply to any AI-assisted development, but they're especially important in Dagster projects where sessions span asset creation, debugging, dbt models, and resource configuration across many files.

---
title: 'Lesson 5: Overview'
module: 'dagster_testing'
lesson: '5'
---

# Overview

By this point you should feel comfortable writing unit tests for your assets. Even tests that rely on external systems.

However while it's helpful to know how tests function with expected results, it can still be good to have tests that can connect to other systems. These tests require more setup and are not as commonly invoked as unit tests but they add another critical layer to testing data applications.

In this lesson, you'll learn about:

1. **Integration tests** - Tests that connect to real systems (like databases) to validate your code works in production-like conditions
2. **Smoke tests** - A powerful technique that runs all your transformations on empty or synthetic data to catch structural errors quickly

Both techniques complement unit tests and help ensure your data pipelines are robust before deploying to production.
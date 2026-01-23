---
title: 'Lesson 3: Overview'
module: 'dagster_testing'
lesson: '3'
---

# Overview

In the previous lesson, you learned that there are many different types of testing. This lesson will focus on unit tests and creating the fundamental tests for your Dagster assets. We will discuss the various aspects of writing tests for your assets before we cover other Dagster concepts in future lessons.

Tests in Dagster leverage conventional Python tooling and methodology. Learning about tests in Python generally is relevant to implementing tests in Dagster. The Dagster-specific learning curve is limited to efficiently using Dagster’s built-in tests features and a practical working knowledge of which tests to use when with reference examples. If this is your first time writing tests in Python, most of this lesson will carry over to your general Python knowledge.

## Decision tree: Where should my test go?

When writing a test, use this decision tree to determine the appropriate testing approach:

```
┌─ I need to test...
│
├─ BUSINESS LOGIC in an asset (calculations, transformations)
│  └─> Direct function test (call the asset function directly)
│
├─ ASSET INTERACTIONS (graph execution, dependencies)
│  └─> Asset graph test with dg.materialize() and mocked resources
│
├─ RESOURCE BEHAVIOR (configs, partitions, IO managers)
│  └─> Asset graph test with build_asset_context()
│
└─ REAL SERVICE CONNECTION or CRITICAL E2E WORKFLOW
   └─> Integration test (use sparingly)
```

**Default**: Start with a direct function test. Only use `dg.materialize()` when you need to test Dagster-specific behavior. Only use integration tests for critical paths where mock behavior might diverge from reality.

This lesson will cover direct function tests and asset graph tests. Integration tests are covered in Lesson 5.
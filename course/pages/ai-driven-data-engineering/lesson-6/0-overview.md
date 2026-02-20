---
title: "Lesson 6: Overview — Code quality with dignified-python"
module: 'ai_driven_data_engineering'
lesson: '6'
---

# Overview: Code quality with dignified-python

In Lesson 5 we ended by improving code quality—refining the asset check to use the S3 resource instead of boto3 directly. The last Dagster skill worth discussing is `dignified-python`: a collection of our internal best practices and philosophies as they relate to Python.

These patterns influence the Dagster codebase but can be applied to any Python codebase. This short lesson covers what the skill does, what some of the rules look like, how to use it on the code you’ve written, and how it differs from (and works with) traditional linters like Ruff.

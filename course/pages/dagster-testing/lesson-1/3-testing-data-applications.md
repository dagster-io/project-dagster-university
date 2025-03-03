---
title: "Lesson 1: Testing data applications"
module: 'dbt_testing'
lesson: '1'
---

# Testing data applications

Testing is particularly important in data applications, but unfortunately, many data engineers do not always keep testing in mind, partly because writing proper tests for data applications can be difficult. But avoiding tests leads to problems:

- **Slow feature development** - When data applications do not have proper testing in place, it becomes much riskier to make changes. Given the complexity of modern data systems, many users avoid making any changes rather than risk making a breaking change.

- **Complex externalities** - Data applications touch a large number of different systems. If you don't fully understand all the dependencies across these systems, it can be hard to know all the externalities.

- **Risky testing life cycle** - Without a proper testing environment, changes need to be made in production environments. Developing this way tends to have a poor feedback loop as entire deployments are necessary to iterate. Coupled with the risks associated with working directly in production.

The good news is that a lot of these issues can be avoided. Writing tests in Dagster can help catch issues early on in a safe environment with no risk of data corruption.

We will show how writing tests around Dagster is very similar to writing tests in standard Python. There are also aspects of Dagster that make it easier to handle situations that are common in data engineering that are difficult to test when using other frameworks.

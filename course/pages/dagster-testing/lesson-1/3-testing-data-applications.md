---
title: "Lesson 1: Testing data applications"
module: 'dbt_testing'
lesson: '1'
---

Testing is particularly important in data applications. Unfortunately, many data applications do not always have proper testing in place. Partly this is because writing proper tests for data frameworks can be difficult. But avoiding tests leads to problems:

- **Slow feature development** When data applications do not have proper testing in place, it becomes much riskier to make any changes. Especially given the complexity of data systems, many users avoid making any changes.

- **Dependencies** As data applications become increasingly complex with the number of systems they touch. Making a change with some frameworks can have hidden externalities and impact unintended systems.

- **Testing life cycle** Without a proper testing environment, changes need to be made in production environments. Developing this way tends to have a poor feedback loop as entire deployments are necessary to iterate. Coupled with the risks associated with working directly in production.

The good news is that a lot of this can be avoided. Writing tests around Dagster can help front load your development process and catch issues early on in much safer environments.

We will show how writing tests around Dagster behave very similar to writing tests for standard Python code. There are even aspects of Dagster that make it easier to handle situations where you have to mock out external dependencies or change which system your application is looking at for integration tests.

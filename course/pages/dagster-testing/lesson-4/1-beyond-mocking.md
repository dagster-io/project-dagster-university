---
title: 'Lesson 4: Beyond mocking'
module: 'dagster_testing'
lesson: '4'
---

Mocking can be very helpful to quickly check that your code is working as expected with predetermined results. However, especially in data engineering, you will also want to ensure your code works when interacting with other systems directly.

Imagine you are writing an asset that executes SQL queries against the production data warehouse. You can set mocks to ensure a query is registered as expected. But without an actual query parser, you cannot ensure the SQL itself is valid. For example mocks would not catch an error with our SQL like this:

```sql
SELECT
   category,
   SUM(price), -- trailing comma
FROM orders
GROUP BY 1
```

This is where we might want to use integration tests to ensure that our assets work as expected.

## Integration testing

Integration testing verifies that different components of a system work together correctly. It helps identify issues in data flow, communication, and interaction between integrated units before system-wide testing.

Usually we do not do integration testing directly against production. This is important to have a system that seamlessly substitutes different systems when executing our code.

Dagster was designed specifically to allow for this type of developer flow.

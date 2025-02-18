---
title: 'Lesson 4: Beyond Mocking'
module: 'dagster_testing'
lesson: '4'
---

Mocking can be very helpful to quickly check that your code is working as you designed it. However, especially in data engineering, you will want to ensure your code works with other systems.

Imagine we are writing assets that execute SQL queries against our production data warehouse in Snowflake. We can set mocks to ensure a query is registered as expected. But without an actual query parser, we cannot ensure the SQL itself is valid. For example using mocks would not catch an error with our SQL like this:

```sql
SELECT
    category,
    SUM(price), -- trailing comma
FROM orders
GROUP BY 1
```

This is where we might want to use integration tests to ensure that our assets work as expected while not connecting to the actual production systems. Luckily when using resources this is easy to do.
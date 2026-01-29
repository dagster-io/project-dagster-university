---
title: 'Lesson 5: The limits of mocks'
module: 'dagster_testing'
lesson: '5'
---

# The limits of mocks in testing

Mocking can be very helpful to check that your code is working as expected. But in data engineering, you also need to ensure your code can interact with systems in production.

In this lesson we will update our assets once again and now pull the city population data from a database. We could accomplish all of this with mocks but it would be advisable to have some part of our testing use a real database connection.
Using a real database will catch more issues before we push code to production as it will more closely resemble how the code will actually run.

Also using a real database will help catch issues that would be arduous to configure ourselves with mocks. Having a SQL parser would help catch syntax issues in our database queries. For example a mock may not catch:

```sql
SELECT
   city_name,
   population
FROM data.city_population
WHERE state_name = "NY"; -- Incorrect quotation marks
```

This is where we can use integration tests to ensure everything work as expected.

## Integration testing

Integration tests verify that different components of a system work together. It helps identify issues in data flow, communication, and interaction between integrated units in an application.

Usually we do not do integration testing directly against production systems. Instead we want something that substitutes an equivalent of the production system.

Integration testing can be tricky. However, Dagster was designed with this type of workflow in mind. You will see how easily you can substitute different dependencies for testing purposes without having to change the core logic of your code.

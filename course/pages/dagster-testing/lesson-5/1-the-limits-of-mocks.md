---
title: 'Lesson 5: The limits of mocks'
module: 'dagster_testing'
lesson: '4'
---

# The limits of mocks in testing

Mocking can be very helpful to quickly check that your code is working as expected with predetermined results. But in data engineering, you will also want to ensure your code can interact with the systems it will rely on in production.

Now we will update our assets once again and instead of pulling the city population data from an API, we will query it from a database. We can pretend that in production our data warehouse holds all of this information.

We could accomplish all of this with mocks but it would be more accurate, and we will catch more issues, if we performed these tests with an actual database. This does. For example mocks would not catch an error with our SQL syntax like:

```sql
SELECT
   city_name,
   population
FROM data.city_population
WHERE state_name = "NY"; -- Incorrect quotation marks
```

This is where we can use integration tests to ensure our assets work as expected.

## Integration testing

Integration tests verify that different components of a system work together. It helps identify issues in data flow, communication, and interaction between integrated units in an application.

Usually we do not do integration testing directly against production (we would not want to use our production data warehouse). Instead we want something that seamlessly substitutes different systems when executing our code.

Dagster was designed specifically to allow for this type of developer flow.

---
title: "Lesson 1: Testing"
module: 'dbt_testing'
lesson: '1'
---

Dagster believes that data engineering should feel like software engineering. And anyone who has been involved in software engineering knows the importance of testing.

With proper testing, potential issues can be discovered much earlier in the development process. This helps to minimize risk as you are building out your platform and gives developers more confidence iterating.

## Types of testing

There are many different types of testing. Each requires focuses on a specific aspect of engineering and requires its own unique approach.

| Type | Description |
| --- | --- |
| Unit Testing | Tests individual components or functions in isolation |
| Integration Testing | Ensures that different modules or services work together as expected |
| Regression Testing | Confirms that recent code changes haven’t broken existing functionality |
| Performance Testing | Evaluates software speed, scalability, and stability under load |
| Security Testing | Identifies vulnerabilities and ensures data protection |

There are many other subdisciplines. Depending on your role within an organization you may be more concerned with different aspects of testing. It is usually not the responsibility of one person to manage the entire testing stack.

This course will primarily focus on the aspects of testing more closely tied with the building applications (unit and integration testing).
---
title: 'Lesson 8: Component usage'
module: 'dbt_dagster'
lesson: '8'
---

# Component usage

By using components, we were able to integrate dbt into our Dagster project much more quickly than if we had coded everything from scratch. You might be wondering when it's best to use components in general.

Components are most helpful for integrating with well-defined workflows. Many Dagster users work with dbt in a fairly standardized way, and the same is true for other tools like [Sling](https://slingdata.io/) and [dlt](https://dlthub.com/). Dagster Components streamline the integration of these tools with your other assets, reducing manual effort.

However, for custom assets like `airport_trips`, it's often better to use regular Dagster assets, since the code is tailored to a specific use case.

A complete Dagster deployment may include both custom code and several different components. The key is understanding where components can save you time and how to effectively incorporate them into your existing workflows.

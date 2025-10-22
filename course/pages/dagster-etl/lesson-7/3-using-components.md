---
title: "Lesson 7: Using components"
module: 'dagster_etl'
lesson: '7'
---

# Using components

When using Dagster Components, one best practice is to treat each component as an isolated, testable, and versioned unit of logic. This means encapsulating not just asset definitions, but their dependencies, such as resources, config schemas, and even environment setup—within the component itself.

```
.
└── src
    └── dagster_and_etl
        └── defs
            ├── dashboard # Looker component
            │   ├── defs.yam
            ├── ingest_files # Sling component
            │   ├── defs.yaml
            │   └── replication.yaml
            └── transform # dbt component
                └── defs.yaml
 ```

To ensure maintainability, avoid having components implicitly rely on external context or shared state unless explicitly passed in. It’s also important to define clear interfaces. Use typed config models and input/output schemas so that consumers of a component understand how to configure and integrate it without digging into the internals.

## Reuse

Another best practice is to design for composability and reuse, much like you would with modules or packages in traditional software engineering. components should be small enough to be meaningful on their own (e.g., a set of assets to extract data from a specific source), but flexible enough to be combined with others in different DAGs or projects. Use version control and semantic naming to track changes, and maintain compatibility boundaries when updating shared components. When possible, validate components independently through unit tests or local runs before integrating them into larger pipelines, ensuring that failures are caught early and in isolation.

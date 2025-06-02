---
title: "Lesson 7: Using components"
module: 'dagster_etl'
lesson: 'extra-credit'
---

# Using components

When using Components in Dagster, a key best practice is to treat each Component as an isolated, testable, and versioned unit of logic. This means encapsulating not just asset definitions, but also their dependencies, such as resources, config schemas, and even environment setup—within the Component itself. To ensure maintainability, avoid having Components implicitly rely on external context or shared state unless explicitly passed in. It’s also important to define clear interfaces: use typed config models and input/output schemas so that consumers of a Component understand how to configure and integrate it without digging into the internals.

Another best practice is to design for composability and reuse, much like you would with modules or packages in traditional software engineering. Components should be small enough to be meaningful on their own (e.g., a set of assets to extract data from a specific source), but flexible enough to be combined with others in different DAGs or projects. Use version control and semantic naming to track changes, and maintain compatibility boundaries when updating shared Components. When possible, validate Components independently through unit tests or local runs before integrating them into larger pipelines, ensuring that failures are caught early and in isolation.
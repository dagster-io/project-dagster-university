---
title: "Lesson 7: Organizing our project"
module: 'dagster_etl'
lesson: 'extra-credit'
---

# Organizing our project

Organizing your Dagster project with components brings structure, scalability, and clarity to your data platform. Instead of building one large codebase where assets, resources, and configurations are tightly coupled, components allow you to break your project into self-contained modules. Each component bundles together related logic—such as a data source, transformation, or model training step—along with its resources and config schemas. This modular layout makes it easier to onboard new team members, reuse functionality across pipelines, and iterate on parts of your system without risking unrelated functionality.

A well-organized component-based project typically follows a pattern where each component lives in its own directory or package, complete with its own virtual environment, tests, and documentation. For example, you might have components/snowflake_ingestion, components/ml_training, and components/reporting_pipeline, each representing a logical slice of your platform. This structure encourages encapsulation and reduces dependency sprawl, allowing individual components to evolve at their own pace. By centralizing composition in your definitions.py file (or similar), you can declaratively stitch components together to build end-to-end workflows without compromising maintainability. As your team and projects grow, components provide the foundation for a scalable and collaborative development model.

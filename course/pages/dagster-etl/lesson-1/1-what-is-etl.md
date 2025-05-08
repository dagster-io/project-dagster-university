---
title: "Lesson 1: What is ETL?"
module: 'dagster_etl'
lesson: '1'
---

# What is ETL?

ETL stands for Extract, Transform, Load and is the process of consolidating data from various upstream sources into a single storage layer. These upstream sources often span multiple systems and data formats: including application databases, third-party services, and raw files. To fully leverage this data, it’s typically best to bring everything into one centralized location, traditionally a data warehouse or data lake, where it can be standardized and made usable across the organization.

![ETL](/images/dagster-etl/lesson-1/what-is-etl.png)

## ETL vs ELT

A quick note on definitions. If you're familiar with ETL, you may have also encountered ELT. The two approaches are very similar, but as the acronym suggests, the key difference is when the transformation happens. In ELT, data is loaded first into the destination system, and transformed afterward.

With the rise of modern data warehouses and lakes that support semi-structured and unstructured data, it's become less critical to transform data into a strict schema before loading. As a result, ETL and ELT are increasingly used interchangeably. Throughout this course, we’ll refer to the process as ETL, even if some examples technically follow the ELT pattern.

## The Importance of ETL

No matter the industry, ETL is foundational to data systems and applications. When implemented effectively, your data becomes a strategic moat that powers everything from operational dashboards to machine learning pipelines. Whether you're building classic BI reports or cutting-edge AI products, the value lies less in the tools and more in the quality and structure of your data.

Even in emerging areas like large language models (LLMs), it's not the model itself that defines success, but the clean, curated datasets used to generate embeddings and provide meaningful context. In short, great data makes great systems.

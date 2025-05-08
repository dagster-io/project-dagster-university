---
title: "Lesson 1: What is ETL?"
module: 'dagster_etl'
lesson: '1'
---

# What is ETL?

ETL stands for extract, transform, load and is the way most companies consolidate their data from various upstream sources into a single storage layer. Often these upstreams sources span multiple data sources and different types of systems. They could be application databases, third party systems or even just raw files. In order to take full advantage of this data, it is usually best to first bring it all into one place, traditionally a data warehouse or data lake where these various systems can be standardized.

![ETL](/images/dagster-etl/lesson-1/what-is-etl.png)

**Note**: If you have heard of ETL, you may have also heard of ELT. The two are very similar to each other. The difference, as the reordering of the acronym would suggest, loading the data happens before the transformation.

Recently as data warehouses and data lakes have become more flexible in supporting semi-structured and unstructured data, it is less critical to transform data to a strict schema before ingestion.

Given the increase in flexibility, ETL and ELT have become somewhat interchangeable. Throughout this course we will simply use ETL, even if some of our projects lend themselves more to ELT. 

## The Importance of ETL

Regardless of industry, ETL is at the core of most companies and is foundational to data applications. When used effectively, data serves as your moat and being able to leverage it is critical to whatever you are designing. This can traditional like reporting dashboards or new verticals like AI. However even for something as cutting edge as LLMs, the true value your specific organization will find is not so much in the model but in curating clean datasets that will be used as the embeddings to fuel the models.
---
title: "Lesson 5: dlt"
module: 'dagster_etl'
lesson: '5'
---

# dlt

One ETL framework we’re particularly excited about is [data load tool (dlt)](https://dlthub.com/docs/intro). dlt is an open-source, lightweight Python library designed to simplify data loading. It takes care of many of the more tedious aspects of ETL, including schema management, data type handling, and normalization, so you can focus on what matters most.

dlt supports a wide range of popular sources and destinations, which means you can move data between systems without having to build and maintain all the supporting infrastructure yourself. While it still gives you the flexibility to handle custom or complex data workflows, it eliminates much of the boilerplate code you'd otherwise need to write, making your pipelines cleaner, more maintainable, and faster to develop.

![dlt](/images/dagster-etl/lesson-5/dlt.png)

Let's look at a simple dlt example.

---
title: "Lesson 5: dlt"
module: 'dagster_etl'
lesson: '5'
---

# dlt

One ETL framework we are particuarly excited about is [data load tool (dlt)](https://dlthub.com/docs/intro). dlt is an open-source and lightweight Python library for loading data. It handles many of the messier parts of ETL like schemas, data types, and normalization. It also supports a variety of popular sources and destinations.

This means that we are able to move data around without having to do so much unnecessary work ourselves. dlt still offers the flexibility to process just about any incoming data but removes most of the boilerplate code we would need to write.

![dlt](/images/dagster-etl/lesson-5/dlt.png)

Let's look at a simple dlt example.

---
title: "Lesson 4: APIs"
module: 'dagster_etl'
lesson: '4'
---

# APIs

Building ETL pipelines for APIs is highly dependent on the specific API, as not all APIs handle data access and delivery in the same way. Each API has its own structure, endpoints, authentication requirements, and query parameters which can all vary significantly.

Basic APIs often return data in JSON format as part of a GET request. When dealing with larger datasets, responses are typically paginated, meaning multiple requests must be made to retrieve the full set of results.

For APIs that manage large-scale or asynchronous data processing, direct responses may not be feasible. Instead, you may initiate a request that triggers a data export, with the resulting data landing in a separate storage layer (like S3) once it's ready. These types of APIs require polling or callback logic to track data readiness.

Because there's no universal standard for how APIs return data, the first step in building any ETL pipeline around an API is to carefully understand the API's structure and behavior.

## NASA API

For this lesson, we’ll use one of the publicly available NASA APIs, specifically, the NeoWs (Near Earth Object Web Service), which provides information about asteroids. This is a relatively simple API that returns data in a JSON payload and doesn't require pagination or asynchronous processing, making it ideal for learning. It gives us a clean example of how to build an ETL pipeline from an external API into our DuckDB warehouse.

**Note**: This API requires an access key, but the process is quick and free. To get started, simply fill out a [short form](https://api.nasa.gov/) on NASA’s API portal. Once submitted, you’ll receive an API key that we’ll use later in the course to authenticate our requests.

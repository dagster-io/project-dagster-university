---
title: "Lesson 4: APIs"
module: 'dagster_etl'
lesson: '4'
---

# APIs

Building out ETL pipelines for APIs is very dependent on the API as not all APIs handle data processing the same way. Each API will have it's own endpoints and parameters that need to be set and not all APIs return data in the same way.

Basic APIs will usually return JSON as part of a get request. Depending on the volume of data, the results may be paginated and multiple API calls will need to be made to retrive all the necessary information.

For APIs that process a larger amounts of data, returning the data via requests is not suitable. In these cases you may make an API call that generates data that eventually lands in some storage layer.

There is no set standard with how APIs must return their data, so the first step in building out any ETL process around and API is understanding the details of that API.

## NASA API

For this course we will be using one of the NASA APIs, specifically the NeoWs (Near Earth Object Web Service) which provides information about asteroids. This is a relatively simple API that returns a JSON payload (as the data is not that large).

**Note**: This API requires an API key. The NASA API is completely free, you just need to fill out a [short form](https://api.nasa.gov/). This will generate an API key which we will use later on.
---
title: "Lesson 4: ETL with API"
module: 'dagster_etl'
lesson: '4'
---

# ETL with APIs

The `NASAResource` gives us the ability to extract data. But we are left in a slightly more ambigious place than when were importing files. With static files there is a clear demacaration between one file and another. When extracting data from an API it is less clear how to structure our assets.

## Time bounding

If we think about the NASA API and our resource, we need to provide the date range for when we pull data. Some APIs let you pull data at points in time down to the minute or even second, the NASA API allows us to filter data at the day level so it makes sense to pull a day's worth of data. The question then is when to run the process. If we want to pull today's data, we cannot be sure if we have collected all the data until the day is over. So the best idea would be to query the API for a day's worth of data, for the previous day. This would be a rolling, non overlapping window.

![Rolling window](/images/dagster-etl/lesson-4/rolling-windows.png)

It would be possible to also do a rolling window with overlaps.

![Rolling window overlap](/images/dagster-etl/lesson-4/rolling-windows-overlap.png)

This can be useful in one of two situations:

* Either when there are updates to data (for example some APIs that work with order data may issue corrections for events like returns).
* Adding resiliency in the case of failures where if a day gets missed, the next run will hopefully execute correctly and process data for the failed run.

![Rolling window overlap failure](/images/dagster-etl/lesson-4/rolling-windows-overlap-failure.png)

Rolling windows with overlaps do add some complexity. Because the same data gets processed more than once in each overlap, it needs to be accounted for in the destination. This can either be in the form of hard deletes where the overlap data is removed before new data is loaded or a soft delete where the previous data still exists but is marked in some way as being less current than the new data that has been ingested.

For the purposes of this class we will just be dealing with rolling windows without overlaps.
---
title: "Lesson 6: Database replication"
module: 'dagster_etl'
lesson: '6'
---

# Database replication

Similar to pulling data from an API, you first need to know some of the details of the database you are pulling from. As we mentioned databases encompass a range of possibilites.

| Database Type | Query | Examples |
| --- | --- | --- |
| Relational | SQL | Postgres, MySQL, Oracle, SQLite |
| NoSQL | Varies | MongoDB, Redis, DynamoDB |
| Graph | Neo4j, Gremlin | Neo4j, Neptune, ArangoDB |
| Vector | Semantic | FAISS, Pinecone, Weaviate |
| Time-series | SQL-like | InfluxDB, Prometheus |

It would be too much for one course to cover all of these so we will focus on Relational databases, specifically Postgres.

## Full refresh replication

Relational databases store their data within table. Say there is an `customers` table that contains the following rows.

| customer_id | first_name | last_name | email                        | created_at          |
|-------------|------------|-----------|------------------------------|---------------------|
| 1           | Alice      | Johnson   | alice.johnson@example.com    | 2024-05-01 10:15:00 |
| 2           | Bob        | Smith     | bob.smith@example.com        | 2024-05-02 08:42:00 |
| 3           | Charlie    | Lee       | charlie.lee@example.com      | 2024-05-03 13:30:00 |
| 4           | Dana       | Martinez  | dana.martinez@example.com    | 2024-05-04 09:50:00 |
| 5           | Evan       | Thompson  | evan.thompson@example.com    | 2024-05-05 11:22:00 |

The easiest way to extract that data is to run a `SELECT * FROM customers` and move it into the destination. This is known as *full refresh* or *snapshot* replication. It is relatively simple and works with any database that supports `SELECT` synatx but you can probably tell the issue. How do we ensure the source table and destination remain in sync?

Using only *full refresh* means that we have to do this operation every time we want to sync the databases. With larger tables this can be prohoibitively long to run. It can also put unnecessary strain on the source database, degrading perfomance while the sync is occuring.

It is possible to do full refresh replication more efficiently by filtering queries. For example the `customers` table has a `created_at` column. So we can filter the data to just query rows since the last time we queried the table. Though this introduces complexity and ambguity.

- What happens when there is an update?
- How does it track hard deletes?
- What happens if a row arrives late in the database?
- How would this work if there was not a `created_at` column?

Because of the limiations around full refreshes, it is best to use other stratedgies to replicate data from relational databases.

## Change data capture

The more common approach to keep the source and destination tables in sync is through *Change Data Capture (CDC)*. Most relational databases maintain some type of log that records the recent events that have occurred in the database. In Postgres this is the Write-Ahead Log (WAL). This log is used for diaster recovery in case of a crash so the database can ensure it recovers correctly and does not corrupt data. It is also ideal for replication.

ETL processes that use CDC can monitor the database log for any changes that happen in the database. This is similar to when we discussed CSVs and ingestion with schedules vs sensors. Full refreshes serve much more like schedules and wait to poll the source while CDC is event based and reacts to events as they occur (most ETL serves do batch the CDC events rather than continously ingesting them but the pattern still holds).

Doing ETL with CDC is much more efficient and less taxing on both the source and destination. However it does have some draw backs. CDC logs do not retain full history. Usually they only hold data for the last few days. This means you cannot get the full state of a databsae with just CDC (unless you set up CDC before data is added to the database). Also you need some application to concosile the CDC events.

Logs usually just contain the straem of events in the database (inserts, updates, deletes). So you will need to apply those events in the correct order to ensure that data in the destination properly matches its state in the source.

| Event Type | Timestamp           | customer_id | first_name | last_name | email                       | created_at          |
|------------|---------------------|-------------|------------|-----------|-----------------------------|---------------------|
| INSERT     | 2024-05-01 10:00:00 | 101         | Alice      | Johnson   | alice.johnson@example.com   | 2024-05-01 10:00:00 |
| UPDATE     | 2024-05-02 14:30:00 | 101         | Alicia     | Johnson   | alice.johnson@example.com   | 2024-05-01 10:00:00 |
| UPDATE     | 2024-05-03 09:10:00 | 101         | Alicia     | Thompson  | alicia.thompson@example.com | 2024-05-01 10:00:00 |

## Building database replication systems

Most ETL tools that handle database replication actually do a combination of the *full refreshes* and *CDC*. When a database or table is initially synced they will use a full refresh and then after the data has been synced, switch to CDC. There need to be steps to ensure that nothing is losed during the cutover.

Hopefully this is all to disuade you from designing your own database replication system from scratch. There are a lot of considerations when replicating data between databases and as already mentioned, this is a very common workflow so the best option is to rely on existing tools and frameworks.

So let's dive back into dlt.
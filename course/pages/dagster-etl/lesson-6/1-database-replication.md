---
title: "Lesson 6: Database replication"
module: 'dagster_etl'
lesson: '6'
---

# Database replication

We’ve talked about many different ways to ingest data from external sources. One method we haven’t discussed yet is moving data between databases. While this is a broad topic, covering many database types, the most common scenario in ETL is replicating data from an OLTP database (like Postgres or MySQL) into a data warehouse (such as Snowflake or Redshift).

Despite being a very common workflow, database replication is nuanced and full of potential pitfalls.

## Understanding your source
Just like with APIs, replicating data from a database starts with understanding the system you're pulling from. Databases vary widely in structure, capabilities, and query patterns.

| Database Type | Query | Examples |
| --- | --- | --- |
| Relational | SQL | Postgres, MySQL, Oracle, SQLite |
| NoSQL | Varies | MongoDB, Redis, DynamoDB |
| Graph | Neo4j, Gremlin | Neo4j, Neptune, ArangoDB |
| Vector | Semantic | FAISS, Pinecone, Weaviate |
| Time-series | SQL-like | InfluxDB, Prometheus |

Since it's too much to cover all of these in a single course, we’ll focus on relational databases, specifically Postgres.

Full Refresh Replication
Relational databases store data in tables. Imagine a customers table with the following data:

| customer_id | first_name | last_name | email                        | created_at          |
|-------------|------------|-----------|------------------------------|---------------------|
| 1           | Alice      | Johnson   | alice.johnson@example.com    | 2024-05-01 10:15:00 |
| 2           | Bob        | Smith     | bob.smith@example.com        | 2024-05-02 08:42:00 |
| 3           | Charlie    | Lee       | charlie.lee@example.com      | 2024-05-03 13:30:00 |
| 4           | Dana       | Martinez  | dana.martinez@example.com    | 2024-05-04 09:50:00 |
| 5           | Evan       | Thompson  | evan.thompson@example.com    | 2024-05-05 11:22:00 |

The most straightforward way to extract this data is with:

```sql
SELECT * FROM customers;
```

This method is known as full refresh or snapshot replication. It’s simple and works with any database that supports SELECT queries. But as you can imagine, there’s a major drawback: how do we keep the source and destination in sync?

If we rely solely on full refreshes, we have to run the entire extraction process every time. This can be prohibitively expensive for large tables and can strain the source database, impacting performance during the sync.

You can optimize full refreshes by filtering with a column like created_at:

```sql
SELECT * FROM customers WHERE created_at > '2024-05-01';
```

But this raises additional questions:

1. What happens if a row is updated, not newly created?
2. How do you track deletions?
3. What if a row is delayed in appearing in the database?
4. What if there’s no timestamp column to filter on?

These limitations are why full refresh alone isn’t ideal for production replication.

## Change data capture (CDC)

A more reliable approach is Change Data Capture (CDC). Relational databases like Postgres maintain a log of changes — in Postgres, this is the Write-Ahead Log (WAL) — which records inserts, updates, and deletes for recovery and replication purposes.

With CDC, an ETL pipeline listens to the database log and reacts to changes. It’s similar to the difference between scheduled vs. event-driven pipelines. Full refreshes are like schedules: they poll periodically. CDC is like sensors: they respond to events as they happen (though typically in small batches).

1. CDC is more efficient and much less taxing on the source database. But it comes with trade-offs:
2. CDC logs are not retained forever — typically only for a few days.
3. CDC doesn’t provide full historical context, so it can’t be used alone to initialize a replica.

You need to apply the log events in order to reconstruct the current state of the data.

Here’s what a stream of CDC events might look like:

| Event Type | Timestamp           | customer_id | first_name | last_name | email                       | created_at          |
|------------|---------------------|-------------|------------|-----------|-----------------------------|---------------------|
| INSERT     | 2024-05-01 10:00:00 | 101         | Alice      | Johnson   | alice.johnson@example.com   | 2024-05-01 10:00:00 |
| UPDATE     | 2024-05-02 14:30:00 | 101         | Alicia     | Johnson   | alice.johnson@example.com   | 2024-05-01 10:00:00 |
| UPDATE     | 2024-05-03 09:10:00 | 101         | Alicia     | Thompson  | alicia.thompson@example.com | 2024-05-01 10:00:00 |

## Building database replication systems

Most modern ETL tools that handle database replication use a hybrid approach:

* Perform a full refresh to establish the initial snapshot of the table.
* Switch to CDC to capture all changes moving forward.

This approach provides both completeness and efficiency but it requires careful coordination during the cutover to ensure that no data is lost or duplicated.

If this sounds complex, that’s because it is. Replicating data between databases is challenging and full of edge cases, which is why we strongly recommend using a dedicated framework instead of trying to build one from scratch.

So with that in mind… let’s dive back into dlt and see how it can help us solve this problem with less effort and more reliability.

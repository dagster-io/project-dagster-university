---
title: "Lesson 6: dlt database replication"
module: 'dagster_etl'
lesson: '6'
---

```bash
dlt init sql_database duckdb
```


```
[sources.sql_database.credentials]
drivername = "postgresql"
database = "test_db"
password = "test_pass"
username = "test_user"
host = "localhost"
port = 5432
```
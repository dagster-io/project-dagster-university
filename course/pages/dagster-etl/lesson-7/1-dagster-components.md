


```bash
dg list plugins
```

```
dagster_dlt.DltLoadCollectionComponent
```

```
│ dagster_dlt   │ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━┓ │
│               │ ┃ Symbol                                 ┃ Summary            ┃ Features            ┃ │
│               │ ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━┩ │
│               │ │ dagster_dlt.DltLoadCollectionComponent │ Expose one or more │ [component,         │ │
│               │ │                                        │ dlt loads to       │ scaffold-target]    │ │
│               │ │                                        │ Dagster as assets. │                     │ │
│               │ └────────────────────────────────────────┴────────────────────┴─────────────────────┘ │
```


```bash
dg scaffold dagster_dlt.DltLoadCollectionComponent ingestion --source sql_database --destination duckdb
```

**Issue**
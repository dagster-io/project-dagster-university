import json
from datetime import date, datetime, timezone

import dagster as dg
from dagster_duckdb import DuckDBResource
from eventregistry import QueryEvents, RequestEventsInfo

from ai_driven_data_engineering.defs.resources import NewsApiResource

daily_partitions = dg.DailyPartitionsDefinition(
    start_date=date.today().replace(day=1).isoformat(),
)


@dg.asset(group_name="raw", partitions_def=daily_partitions)
def trending_events(
    context: dg.AssetExecutionContext,
    duckdb: DuckDBResource,
    newsapi: NewsApiResource,
) -> dg.MaterializeResult:
    partition_date = context.partition_key  # "YYYY-MM-DD"

    er = newsapi.get_client()
    q = QueryEvents(dateStart=partition_date, dateEnd=partition_date)
    q.setRequestedResult(RequestEventsInfo(count=50, sortBy="size", sortByAsc=False))
    response = er.execQuery(q)

    events_data = response.get("events") or {}
    events = events_data.get("results", [])

    ingested_at = datetime.now(timezone.utc)
    rows = []
    for event in events:
        title = event.get("title", {})
        summary = event.get("summary", {})
        concept_labels = []
        for c in event.get("concepts", []):
            if not isinstance(c, dict):
                continue
            label = c.get("label", "")
            concept_labels.append(
                label.get("eng", "") if isinstance(label, dict) else str(label)
            )
        rows.append(
            (
                event.get("uri", ""),
                title.get("eng", "") if isinstance(title, dict) else str(title),
                summary.get("eng", "") if isinstance(summary, dict) else str(summary),
                event.get("eventDate", ""),
                event.get("totalArticleCount", 0),
                json.dumps(concept_labels),
                ingested_at,
                partition_date,
            )
        )

    with duckdb.get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trending_events (
                uri TEXT,
                title TEXT,
                summary TEXT,
                event_date TEXT,
                article_count INTEGER,
                concepts TEXT,
                ingested_at TIMESTAMP,
                partition_date TEXT
            )
        """)
        conn.execute(
            "DELETE FROM trending_events WHERE partition_date = ?",
            [partition_date],
        )
        if rows:
            conn.executemany(
                "INSERT INTO trending_events VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                rows,
            )
        row_count = conn.execute(
            "SELECT COUNT(*) FROM trending_events WHERE partition_date = ?",
            [partition_date],
        ).fetchone()[0]

    context.log.info(
        f"Loaded {row_count} trending events for partition {partition_date}"
    )
    return dg.MaterializeResult(metadata={"row_count": dg.MetadataValue.int(row_count)})

with source as (
    select * from {{ source('dagster', 'trending_events') }}
),

renamed as (
    select
        uri                                   as event_uri,
        title,
        summary,
        cast(event_date as date)              as event_date,
        article_count,
        concepts,
        partition_date,
        ingested_at
    from source
)

select * from renamed

select
    date_of_business,
    pct_over_30_min
from {{ ref('daily_metrics') }}
where pct_over_30_min > 0.1
order by pct_over_30_min desc
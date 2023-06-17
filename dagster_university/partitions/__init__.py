from dagster import MonthlyPartitionsDefinition, WeeklyPartitionsDefinition
from os import environ

start_date = environ.get("START_DATE", "2023-01-01")
end_date = environ.get("END_DATE", "2023-04-01")

monthly_partition = MonthlyPartitionsDefinition(
    start_date=start_date,
    end_date=end_date
)

weekly_partition = WeeklyPartitionsDefinition(
    start_date=start_date,
    end_date=end_date
)
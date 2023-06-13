from dagster import MonthlyPartitionsDefinition

monthly_partitions = MonthlyPartitionsDefinition(
    start_date="2023-01-01",
    end_date="2023-04-01"
)


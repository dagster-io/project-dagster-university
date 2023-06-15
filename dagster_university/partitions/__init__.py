from dagster import MonthlyPartitionsDefinition

monthly_partition = MonthlyPartitionsDefinition(
    start_date="2023-01-01",
    end_date="2023-04-01"
)


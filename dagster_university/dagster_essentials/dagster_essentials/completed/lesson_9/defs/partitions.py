import dagster as dg

from dagster_essentials.completed.lesson_9.defs.assets import constants

start_date = constants.START_DATE
end_date = constants.END_DATE

monthly_partition = dg.MonthlyPartitionsDefinition(
    start_date=start_date, end_date=end_date
)

weekly_partition = dg.WeeklyPartitionsDefinition(
    start_date=start_date, end_date=end_date
)

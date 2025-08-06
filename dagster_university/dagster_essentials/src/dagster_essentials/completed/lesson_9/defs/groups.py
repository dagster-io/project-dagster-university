import dagster as dg

from dagster_essentials.completed.lesson_9.defs.assets import requests

request_assets = dg.load_assets_from_modules(
    modules=[requests],
    group_name="requests",
)

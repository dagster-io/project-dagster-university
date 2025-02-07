import os

TAXI_ZONES_FILE_PATH = os.path.join("data", "raw", "taxi_zones.csv")
TAXI_TRIPS_TEMPLATE_FILE_PATH = os.path.join("data", "raw", "taxi_trips_{}.parquet")

TRIPS_BY_AIRPORT_FILE_PATH = os.path.join("data", "outputs", "trips_by_airport.csv")
TRIPS_BY_WEEK_FILE_PATH = os.path.join("data", "outputs", "trips_by_week.csv")
MANHATTAN_STATS_FILE_PATH = os.path.join("data", "staging", "manhattan_stats.geojson")
MANHATTAN_MAP_FILE_PATH = os.path.join("data", "outputs", "manhattan_map.png")

DATE_FORMAT = "%Y-%m-%d"

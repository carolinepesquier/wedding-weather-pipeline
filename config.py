# Location
WEDDING_PLACE = (51.5540, 0.2520, 22)
LOCATION_LABEL = "Upminster"

# Open-Meteo cache:
CACHE_EXP_BACKFILL = 0    # never expire — same dates never change
CACHE_EXP_DAILY = 3600     # 1 hour — recent data may update

# BigQuery
PROJECT_ID = "wedding-weather-496115"
METEOSTAT_TABLE = f"{PROJECT_ID}.bronze.meteostat_hourly_bronze"
OPEN_METEO_TABLE = f"{PROJECT_ID}.bronze.open_meteo_hourly_bronze"
VISUAL_CROSSING_TABLE = f"{PROJECT_ID}.bronze.visual_crossing_hourly_bronze"
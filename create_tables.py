from google.cloud import bigquery

client = bigquery.Client(project="wedding-weather-496115")

dataset = bigquery.Dataset("wedding-weather-496115.bronze")
dataset.location = "EU"
client.create_dataset(dataset, exists_ok=True)
print("Dataset created")

# Meteostat table:
table_id = "wedding-weather-496115.bronze.meteostat_hourly_bronze"

schema = [
    bigquery.SchemaField("datetime", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("location_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("station_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("temperature", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("dew_point", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("relative_humidity", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("rainfall", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("snowfall", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("snow_depth", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("wind_direction", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("wind_speed_avg", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("wind_gust_peak", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("air_pressure_avg", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("sunshine_duration", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("cloud_cover_avg", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("visibility", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("weather_code", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("rare_weather_description", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="datetime"
)
table = client.create_table(table, exists_ok=True)  
print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))

# Add apparent_temperature to existing Meteostat table:
client.query("""
    ALTER TABLE `wedding-weather-496115.bronze.meteostat_hourly_bronze`
    ADD COLUMN IF NOT EXISTS apparent_temperature FLOAT64
""").result()
print("Added apparent_temperature column to meteostat_hourly_bronze")

# Open-Meteo table:
table_id = "wedding-weather-496115.bronze.open_meteo_hourly_bronze"

schema = [
    bigquery.SchemaField("datetime", "DATETIME", mode="REQUIRED"),
    bigquery.SchemaField("location_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("station_id", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("temperature", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("dew_point", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("relative_humidity", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("rainfall", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("snowfall", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("snow_depth", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("wind_direction", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("wind_speed_avg", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("wind_gust_peak", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("air_pressure_avg", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("sunshine_duration", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("cloud_cover_avg", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("visibility", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("weather_code", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("rare_weather_description", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("apparent_temperature", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
]

table = bigquery.Table(table_id, schema=schema)
table.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.DAY,
    field="datetime"
)
table = client.create_table(table, exists_ok=True)  
print("Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id))

destination_table = client.get_table(table_id)
print("Loaded {} rows.".format(destination_table.num_rows))
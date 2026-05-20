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

# Silver tables
METEOSTAT_SILVER = f"{PROJECT_ID}.silver.meteostat_hourly_silver"
OPEN_METEO_SILVER = f"{PROJECT_ID}.silver.open_meteo_hourly_silver"
VISUAL_CROSSING_SILVER = f"{PROJECT_ID}.silver.visual_crossing_hourly_silver"

# GCS
GCS_BUCKET = "wedding-weather-ml-artefacts"
GCS_MLFLOW_URI = f"gs://{GCS_BUCKET}/mlflow"

# MLflow
MLFLOW_TRACKING_URI = "sqlite:///ml/mlflow.db"
MLFLOW_ARTIFACT_URI = GCS_MLFLOW_URI
EXPERIMENT_RAINFALL = "rainfall_prediction"
EXPERIMENT_TEMPERATURE = "temperature_prediction"

# Temporal split
TRAIN_END = "2023-12-31 23:00:00"
TEST_START = "2024-01-01 00:00:00"
TEST_END = "2025-12-31 23:00:00"

# Targets
TARGET_RAINFALL = "rainfall"
TARGET_TEMPERATURE = "temperature"

# Sources
SOURCES = ["meteostat", "open_meteo", "visual_crossing", "average", "weighted"]
MODELS = ["baseline", "linear", "xgboost", "sarimax", "prophet"]
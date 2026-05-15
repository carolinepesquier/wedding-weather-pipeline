from datetime import date, timedelta
from extractors.fetch_meteostat import fetch_meteostat
from extractors.fetch_open_meteo import fetch_open_meteo
from extractors.fetch_visual_crossing import fetch_visual_crossing
from load_bronze import load_to_bigquery
from config import WEDDING_PLACE, METEOSTAT_TABLE, OPEN_METEO_TABLE, VISUAL_CROSSING_TABLE, CACHE_EXP_DAILY
from dotenv import load_dotenv
import os

yesterday = date.today() - timedelta(days = 1)

# Meteostat daily run: fetch yesterday's data
df_ms = fetch_meteostat(
    coordinates = WEDDING_PLACE,
    start_date = yesterday,
    end_date = yesterday
)
load_to_bigquery(df_ms, METEOSTAT_TABLE)

# Open-Meteo daily run: fetch yesterday's data
df_om = fetch_open_meteo(
    cache_exp = CACHE_EXP_DAILY,
    coordinates = WEDDING_PLACE,
    start_date = yesterday,
    end_date = yesterday
)
load_to_bigquery(df_om, OPEN_METEO_TABLE)

# Visual_Crossing daily run: fetch yesterday's data
load_dotenv()
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
if not API_KEY:
    raise ValueError("Visual Crossing API key not found. Please set the VISUAL_CROSSING_API_KEY environment variable.")
df_vc = fetch_visual_crossing(
    api_key=API_KEY,
    coordinates = WEDDING_PLACE,
    start_date = yesterday,
    end_date = yesterday
)
load_to_bigquery(df_vc, VISUAL_CROSSING_TABLE)
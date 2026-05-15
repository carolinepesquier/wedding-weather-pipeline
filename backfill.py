from datetime import date
from dateutil.relativedelta import relativedelta
from extractors.fetch_meteostat import fetch_meteostat
from extractors.fetch_open_meteo import fetch_open_meteo
from extractors.fetch_visual_crossing import fetch_visual_crossing
from load_bronze import load_to_bigquery
from config import WEDDING_PLACE, METEOSTAT_TABLE, CACHE_EXP_BACKFILL, OPEN_METEO_TABLE, VISUAL_CROSSING_TABLE
from dotenv import load_dotenv
import os

start = date(2006, 1, 1)
end = date(2026, 5, 14)
load_dotenv()
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
if not API_KEY:
    raise ValueError("Visual Crossing API key not found. Please set the VISUAL_CROSSING_API_KEY environment variable.")

# Loading in chunks to not hit Big Query 4,000 partition limit:
current = start
while current < end:
    chunk_end = min(current.replace(year = current.year + 1) - relativedelta(days = 1), end)
    print(f"Fetching {current} to {chunk_end}...")

    # Meteostat backfill: 20 years - DONE
    df_ms = fetch_meteostat(
            coordinates=WEDDING_PLACE,
            start_date = current,
            end_date = chunk_end
    )
    load_to_bigquery(df_ms, METEOSTAT_TABLE)

    # Open-Meteo backfill: 20 years - DONE
    #df_om = fetch_open_meteo(
    #    cache_exp = CACHE_EXP_BACKFILL,
    #    coordinates = WEDDING_PLACE,
    #    start_date = current,
    #    end_date = chunk_end
    #)
    #load_to_bigquery(df_om, OPEN_METEO_TABLE)

    # Visual_Crossing backfill test - HANDLED IN run_vc_backfill_scheduled.py (backfill automated as only 1,000 API calls available per day).
    #df_vc = fetch_visual_crossing(
    #    api_key = API_KEY,
    #    coordinates = WEDDING_PLACE,
    #    start_date = current,
    #    end_date = chunk_end
    #)
    #load_to_bigquery(df_vc, VISUAL_CROSSING_TABLE)

    current = chunk_end + relativedelta(days=1)

print("Backfill complete")
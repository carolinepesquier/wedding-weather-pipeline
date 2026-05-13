from datetime import date, timedelta
from extractors.fetch_meteostat import fetch_meteostat
from extractors.fetch_open_meteo import fetch_open_meteo
from load import load_to_bigquery
from config import WEDDING_PLACE, METEOSTAT_TABLE, OPEN_METEO_TABLE, CACHE_EXP_DAILY

#yesterday = date.today() - timedelta(days = 1)

# Meteostat daily run: fetch yesterday's data
#df_ms = fetch_meteostat(
#    coordinates = WEDDING_PLACE,
#    start_date = yesterday,
#    end_date = yesterday
#)

#load_to_bigquery(df_ms, METEOSTAT_TABLE)

# Open-Meteo test load: 
df_om = fetch_open_meteo(
    cache_exp = CACHE_EXP_DAILY,
    coordinates = WEDDING_PLACE,
    start_date = date(2026, 5, 4),
    end_date = date(2026, 5, 11)
)
load_to_bigquery(df_om, OPEN_METEO_TABLE)
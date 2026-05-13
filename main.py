from datetime import date, timedelta
from extractors.fetch_meteostat import fetch_meteostat
from load import load_to_bigquery
from config import WEDDING_PLACE, METEOSTAT_TABLE

# Daily run: fetch yesterday's data
yesterday = date.today() - timedelta(days = 1)

df = fetch_meteostat(
    coordinates = WEDDING_PLACE,
    start_date = date(2026, 5, 11),
    end_date = date(2026, 5, 12)
)

load_to_bigquery(df, METEOSTAT_TABLE)
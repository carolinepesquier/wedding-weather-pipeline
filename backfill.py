from datetime import date
from dateutil.relativedelta import relativedelta
from extractors.fetch_meteostat import fetch_meteostat
from load import load_to_bigquery
from config import WEDDING_PLACE, METEOSTAT_TABLE

start = date(2006, 1, 1)
end = date(2026, 5, 3)

current = start
while current < end:
    chunk_end = min(current.replace(year = current.year + 1) - relativedelta(days = 1), end)
    print(f"Fetching {current} to {chunk_end}...")
    
    df = fetch_meteostat(
        coordinates=WEDDING_PLACE,
        start_date=current,
        end_date=chunk_end
    )
    
    load_to_bigquery(df, METEOSTAT_TABLE)
    current = chunk_end + relativedelta(days=1)

print("Backfill complete")
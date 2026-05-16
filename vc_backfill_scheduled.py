import pandas as pd
from datetime import date
from extractors.fetch_visual_crossing import fetch_visual_crossing
from load_bronze import load_to_bigquery
from config import WEDDING_PLACE, VISUAL_CROSSING_TABLE
from dotenv import load_dotenv
import os

# Visual Crossing API key retrieve:
load_dotenv()
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
if not API_KEY:
    raise ValueError("Visual Crossing API key not found. Please set the VISUAL_CROSSING_API_KEY environment variable.")

# Today's date:
today = date.today()
today = pd.to_datetime(today)

# Retrieve csv schedule:
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, "vc_backfill_schedule.csv")
schedule = pd.read_csv(csv_path, sep = "\t")

# Forcing date format with day first:
schedule['Start'] = pd.to_datetime(schedule['Start'], dayfirst=True).astype('datetime64[us]')
schedule['End'] = pd.to_datetime(schedule['End'], dayfirst=True).astype('datetime64[us]')
schedule['Run_date'] = pd.to_datetime(schedule['Run_date'], dayfirst=True).astype('datetime64[us]')


print(schedule['Start'].iloc[0])
print(schedule.info())

# Trigger action on today's date only:
match_found = False

for i in range(len(schedule)):
    if today == schedule["Run_date"].iloc[i]:
        match_found = True
        df_vc = fetch_visual_crossing(
        api_key = API_KEY,
        coordinates = WEDDING_PLACE,
        start_date = schedule["Start"].iloc[i].date(),
        end_date = schedule["End"].iloc[i].date()
        )
        load_to_bigquery(df_vc, VISUAL_CROSSING_TABLE)
        print(f"Backfill for {schedule['Start'].iloc[i].date()} to {schedule['End'].iloc[i].date()} completed.")
        break 
if not match_found:
    print(f"It seems no backfill is scheduled for today ({today.date()}).")
    
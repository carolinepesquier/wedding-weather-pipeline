import requests
import pandas as pd
import json
from datetime import datetime
from .utils import get_location_name
from dotenv import load_dotenv

def fetch_visual_crossing(api_key, coordinates, start_date, end_date):

    location = get_location_name(coordinates)
    url = (
        f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
        f"{coordinates[0]},{coordinates[1]}/{start_date}/{end_date}"
        f"?key={api_key}&include=hours&unitGroup=metric"
        f"&elements=datetime,stations,temp,dew,humidity,precip,snow,snowdepth,"
        f"winddir,windspeed,windgust,pressure,cloudcover,visibility,"
        f"feelslike,solarradiation,source,conditions&contentType=json"
    )

    response = requests.get(url)
    response.raise_for_status() 
    data = response.json()

    rows = []
    for day in data['days']:
        day_date = day['datetime']
        for hour in day['hours']:
            hour_time = hour['datetime']
            dt = datetime.strptime(f"{day_date} {hour_time}", "%Y-%m-%d %H:%M:%S")
            
            rows.append({
                'datetime': dt,
                'station_id': ','.join(hour.get('stations') or []),
                'temperature': hour.get('temp'),
                'dew_point': hour.get('dew'),
                'relative_humidity': hour.get('humidity'),
                'precipitation': hour.get('precip'),
                'precipitation_type': ','.join(hour.get('preciptype') or []),
                'snowfall': hour.get('snow'),
                'snow_depth': hour.get('snowdepth'),
                'wind_direction': hour.get('winddir'),
                'wind_speed_avg': hour.get('windspeed'),
                'wind_gust_peak': hour.get('windgust'),
                'air_pressure_avg': hour.get('pressure'),
                'cloud_cover_avg': hour.get('cloudcover'),
                'visibility': hour.get('visibility'),
                'apparent_temperature': hour.get('feelslike'),
                'rare_weather_description':hour.get('conditions'),
                'solar_radiation': hour.get('solarradiation'),
                'source': hour.get('source'),
                'ingested_at': pd.Timestamp.now(),
            })


    df = pd.DataFrame(rows)
    df['location_name'] = location
    df['sunshine_duration'] = pd.NA
    df['weather_code'] = pd.NA   # Visual Crossing doesn't provide a standardized weather code.

    df = df.astype({
        'datetime': 'datetime64[us]',
        'station_id': 'string',
        'temperature': 'Float64',
        'dew_point': 'Float64',
        'relative_humidity': 'Float64',
        'precipitation': 'Float64',
        'precipitation_type': 'string',
        'snowfall': 'Float64',
        'snow_depth': 'Float64',
        'wind_direction': 'Float64',
        'wind_speed_avg': 'Float64',
        'wind_gust_peak': 'Float64',
        'air_pressure_avg': 'Float64',
        'sunshine_duration': 'Float64',
        'cloud_cover_avg': 'Float64',
        'visibility': 'Float64',
        'weather_code': 'Float64',
        'location_name': 'string',
        'rare_weather_description': 'string',
        'apparent_temperature': 'Float64',
        'solar_radiation': 'Float64',
        'source': 'string',
        'ingested_at': 'datetime64[us]'
        }
    )

    # Re order date:
    df.sort_values('datetime', inplace = True)

    return df

if __name__ == "__main__":
    import os
    load_dotenv()
    API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
    df = fetch_visual_crossing(
        api_key=API_KEY,
        coordinates=(51.5540, 0.2520, 22),
        start_date="2026-05-13",
        end_date="2026-05-13"
    )
    print(df.head())
    df.info()


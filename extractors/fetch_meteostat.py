import meteostat as ms
import pandas as pd
from datetime import date

def fetch_meteostat(coordinates, start_date, end_date):

    # Retrieve the weather station nearest to given coordinates:
    point = ms.Point(*coordinates)
    station = ms.stations.nearby(point, limit=1)
    station_id = station.index[0]
    station_name = station['name'].iloc[0]

    # Accept either string or date object
    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)
    if isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)

    # Get hourly data:
    ts = ms.hourly(ms.Station(id = station_id), 
                   start_date, 
                   end_date, 
                   parameters=[
                            ms.Parameter.TEMP,
                            ms.Parameter.DWPT,
                            ms.Parameter.RHUM,
                            ms.Parameter.PRCP,
                            ms.Parameter.SNOW,
                            ms.Parameter.SNWD,
                            ms.Parameter.WDIR,
                            ms.Parameter.WSPD,
                            ms.Parameter.WPGT,
                            ms.Parameter.PRES,
                            ms.Parameter.TSUN,
                            ms.Parameter.CLDC,
                            ms.Parameter.VSBY,
                            ms.Parameter.COCO,
                            ]
                   )
    
    df = ts.fetch()

    # Remove index:
    df.reset_index(inplace=True)

    # Rename columns:
    df.rename(columns = {
        'time': 'datetime',
        'temp': 'temperature',
        'dwpt': 'dew_point',
        'rhum': 'relative_humidity',
        'prcp': 'precipitation',
        'snow': 'snowfall',
        'snwd': 'snow_depth',
        'wdir': 'wind_direction',
        'wspd': 'wind_speed_avg',
        'wpgt': 'wind_gust_peak',
        'pres': 'air_pressure_avg',
        'tsun': 'sunshine_duration',
        'cldc': 'cloud_cover_avg',
        'vsby': 'visibility',
        'coco': 'weather_code'
        },
        inplace = True
    )

    # Force columns type:
    df = df.astype({
        'datetime': 'datetime64[us]',
        'temperature': 'Float64',
        'dew_point': 'Float64',
        'relative_humidity': 'Int64',
        'precipitation': 'Float64',
        'snowfall': 'Int64',
        'snow_depth': 'Int64',
        'wind_direction': 'Int64',
        'wind_speed_avg': 'Float64',
        'wind_gust_peak': 'Float64',
        'air_pressure_avg': 'Float64',
        'sunshine_duration': 'Int64',
        'cloud_cover_avg': 'Int64',
        'visibility': 'Float64',
        'weather_code': 'Int64',
        }
    )

    # Add metadata columns:
    df['location_name'] = station_name
    df['station_id'] = station_id
    df[['location_name', 'station_id']] = df[['location_name', 'station_id']].astype('string')
    df['rare_weather_description'] = pd.NA
    df['rare_weather_description'] = df['rare_weather_description'].astype('string')
    df['ingested_at'] = pd.Timestamp.now()

    # Re order date:
    df.sort_values('datetime', inplace = True)

    return df

# Test function:
if __name__ == "__main__":
    wedding_place = (51.5540, 0.2520, 22)
    df = fetch_meteostat(wedding_place, start_date = '2024-01-01', end_date = '2024-02-28')
    print(df.head())
    df.info()
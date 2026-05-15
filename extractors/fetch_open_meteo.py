import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from .utils import get_location_name

def fetch_open_meteo(cache_exp, coordinates, start_date, end_date):

    # Find the location name from coordinates:
    location_name = get_location_name(coordinates)

    # Setup the Open-Meteo API client with cache and retry on error:
    cache_session = requests_cache.CachedSession('.cache', expire_after = cache_exp)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # The order of variables in hourly is important:
    url = "https://archive-api.open-meteo.com/v1/archive"
    params = {
        "latitude": coordinates[0],
        "longitude": coordinates[1],
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ["temperature_2m", "relative_humidity_2m",
                    "dew_point_2m", "precipitation", "snowfall", "snow_depth",
                    "weather_code", "cloud_cover", "wind_speed_10m",
                    "wind_direction_10m", "wind_gusts_10m",
                    "pressure_msl", "sunshine_duration",
                    "apparent_temperature", "direct_radiation", "rain"],
    }
    responses = openmeteo.weather_api(url, params = params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    hourly_snowfall = hourly.Variables(4).ValuesAsNumpy()
    hourly_snow_depth = hourly.Variables(5).ValuesAsNumpy()
    hourly_weather_code = hourly.Variables(6).ValuesAsNumpy()
    hourly_cloud_cover = hourly.Variables(7).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(8).ValuesAsNumpy()
    hourly_wind_direction_10m = hourly.Variables(9).ValuesAsNumpy()
    hourly_wind_gusts_10m = hourly.Variables(10).ValuesAsNumpy()
    hourly_pressure_msl = hourly.Variables(11).ValuesAsNumpy()
    hourly_sunshine_duration = hourly.Variables(12).ValuesAsNumpy()
    hourly_apparent_temperature = hourly.Variables(13).ValuesAsNumpy()
    hourly_direct_radiation = hourly.Variables(14).ValuesAsNumpy()
    hourly_direct_rain = hourly.Variables(15).ValuesAsNumpy()


    hourly_data = {
        "datetime": pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
            end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left"
        ).tz_localize(None)
    }

    hourly_data["temperature"] = hourly_temperature_2m
    hourly_data["dew_point"] = hourly_dew_point_2m
    hourly_data["relative_humidity"] = hourly_relative_humidity_2m
    hourly_data["precipitation"] = hourly_precipitation
    hourly_data["snowfall"] = hourly_snowfall
    hourly_data["snow_depth"] = hourly_snow_depth * 100     # Convert from m to cm to be consistent with Meteostat
    hourly_data["wind_direction"] = hourly_wind_direction_10m
    hourly_data["wind_speed_avg"] = hourly_wind_speed_10m
    hourly_data["wind_gust_peak"] = hourly_wind_gusts_10m
    hourly_data["air_pressure_avg"] = hourly_pressure_msl
    hourly_data["sunshine_duration"] = hourly_sunshine_duration / 60   # Convert from seconds to minutes to be consistent with Meteostat
    hourly_data["cloud_cover_avg"] = hourly_cloud_cover
    hourly_data["visibility"] = pd.NA   # Not available in Open-Meteo, but we want to keep the same schema as Meteostat for easier comparison and potential future enrichment.
    hourly_data["weather_code"] = hourly_weather_code
    hourly_data["rare_weather_description"] =  pd.NA
    hourly_data["apparent_temperature"] = hourly_apparent_temperature
    hourly_data["solar_radiation"] = hourly_direct_radiation
    hourly_data["rainfall"] = hourly_direct_rain
    hourly_data['location_name'] = location_name
    hourly_data['station_id'] = 'Open-Meteo (no station)'
    hourly_data['ingested_at'] = pd.Timestamp.now()
    

    df = pd.DataFrame(data = hourly_data)

    df = df.astype({
        'datetime': 'datetime64[us]',
        'temperature': 'Float64',
        'dew_point': 'Float64',
        'relative_humidity': 'Float64',
        'precipitation': 'Float64',
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
        'station_id': 'string',
        'rare_weather_description': 'string',
        'apparent_temperature': 'Float64',
        'solar_radiation': 'Float64',
        'rainfall': 'Float64',
        'ingested_at': 'datetime64[us]'
        }
    )

    # Re order date:
    df.sort_values('datetime', inplace = True)

    return df

# Test:
if __name__ == "__main__":
    wedding_place = (51.5540, 0.2520, 22)
    df = fetch_open_meteo(
        cache_exp=-1,
        coordinates=wedding_place,
        start_date="2026-05-04",
        end_date="2026-05-12"
    )
    print(df.head())
    df.info()
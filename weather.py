import openmeteo_requests
import requests_cache
import pandas as pd
import numpy as np
import requests
from retry_requests import retry
from datetime import datetime, timedelta
import json


def geocode_location(location_name):
    """Convert location name to coordinates using Nominatim API"""
    base_url = "https://nominatim.openstreetmap.org/search"
    params = {"q": location_name, "format": "json", "limit": 1}
    headers = {"User-Agent": "AgriAI Weather App"}

    response = requests.get(base_url, params=params, headers=headers)
    if response.ok and response.json():
        location = response.json()[0]
        return float(location["lat"]), float(location["lon"])
    return None


def get_weather_data(latitude, longitude, forecast_days=7):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "precipitation_probability_max",
            "windspeed_10m_max",
            "weathercode",
        ],
        "timezone": "auto",
        "forecast_days": forecast_days,
    }

    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    daily = response.Daily()

    start_date = pd.to_datetime(daily.Time(), unit="s")
    date_range = [start_date + timedelta(days=x) for x in range(forecast_days)]

    # Convert NumPy arrays to Python lists
    daily_data = {
        "date": date_range,
        "temp_max": daily.Variables(0).ValuesAsNumpy().tolist(),
        "temp_min": daily.Variables(1).ValuesAsNumpy().tolist(),
        "precipitation": daily.Variables(2).ValuesAsNumpy().tolist(),
        "precipitation_prob": daily.Variables(3).ValuesAsNumpy().tolist(),
        "windspeed": daily.Variables(4).ValuesAsNumpy().tolist(),
        "weathercode": daily.Variables(5).ValuesAsNumpy().tolist(),
    }

    df = pd.DataFrame(data=daily_data)
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    # Convert to dictionary with native Python types
    result = {
        "latitude": float(response.Latitude()),
        "longitude": float(response.Longitude()),
        "timezone": str(response.Timezone()),
        "daily": df.to_dict("records"),
    }

    return result


def get_weather_icon(code):
    weather_codes = {
        0: "sun",  # Clear sky
        1: "sun",  # Mainly clear
        2: "cloud-sun",  # Partly cloudy
        3: "cloud",  # Overcast
        45: "cloud-fog",  # Foggy
        48: "cloud-fog",  # Depositing rime fog
        51: "cloud-rain",  # Light drizzle
        53: "cloud-rain",  # Moderate drizzle
        55: "cloud-rain",  # Dense drizzle
        61: "cloud-showers-heavy",  # Slight rain
        63: "cloud-showers-heavy",  # Moderate rain
        65: "cloud-showers-heavy",  # Heavy rain
        71: "snowflake",  # Slight snow
        73: "snowflake",  # Moderate snow
        75: "snowflake",  # Heavy snow
        77: "snowflake",  # Snow grains
        80: "cloud-rain",  # Slight rain showers
        81: "cloud-rain",  # Moderate rain showers
        82: "cloud-rain",  # Violent rain showers
        85: "snowflake",  # Slight snow showers
        86: "snowflake",  # Heavy snow showers
        95: "cloud-bolt",  # Thunderstorm
        96: "cloud-bolt",  # Thunderstorm with slight hail
        99: "cloud-bolt",  # Thunderstorm with heavy hail
    }
    return weather_codes.get(code, "question")

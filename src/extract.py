import requests
import pandas as pd
import os

CITIES = {
    "London": {"lat": 51.51, "lon": -0.13, "country": "UK"},
    "New York": {"lat": 40.71, "lon": -74.01, "country": "USA"},
    "Tokyo": {"lat": 35.68, "lon": 139.69, "country": "Japan"}
}

def extract_weather_data():
    print("Extracting weather data from Open-Meteo...")
    all_raw_data = []
    
    for city, coords in CITIES.items():
        url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,relative_humidity_2m_max,wind_speed_10m_max&past_days=7&timezone=auto"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Add city name to the dictionary so we know where it came from
        data['city_name'] = city
        data['country'] = coords['country']
        all_raw_data.append(data)
        
    return all_raw_data
import pandas as pd

def transform_data(raw_data_list):
    print("Transforming data into Star Schema...")
    
    dim_city_rows = []
    fact_weather_rows = []
    
    for raw in raw_data_list:
        city_name = raw['city_name']
        country = raw['country']
        lat = raw['latitude']
        lon = raw['longitude']
        
        # Simple hashing/string manipulation for IDs
        city_id = abs(hash(city_name)) % (10 ** 8) 
        
        dim_city_rows.append({
            'city_id': city_id,
            'city_name': city_name,
            'country': country,
            'latitude': lat,
            'longitude': lon
        })
        
        # Loop through the daily data to create fact rows
        daily_data = raw['daily']
        for i in range(len(daily_data['time'])):
            date_str = daily_data['time'][i]
            date_id = int(date_str.replace("-", "")) # e.g., 20231025
            
            # Determine season (Very basic logic for Northern Hemisphere)
            month = int(date_str.split("-")[1])
            if month in [12, 1, 2]: season = "Winter"
            elif month in [3, 4, 5]: season = "Spring"
            elif month in [6, 7, 8]: season = "Summer"
            else: season = "Autumn"
            
            fact_weather_rows.append({
                'date_id': date_id,
                'city_id': city_id,
                'temperature_max_c': daily_data['temperature_2m_max'][i],
                'temperature_min_c': daily_data['temperature_2m_min'][i],
                'rainfall_mm': daily_data['precipitation_sum'][i],
                'humidity_pct': daily_data['relative_humidity_2m_max'][i],
                'wind_speed_max_kmh': daily_data['wind_speed_10m_max'][i]
            })
            
            # We won't create a separate dim_date dataframe here to keep it simple, 
            # but we will insert it directly in the load step via SQL logic.
            # Actually, let's make dim_date properly:
            
    dim_city_df = pd.DataFrame(dim_city_rows)
    fact_weather_df = pd.DataFrame(fact_weather_rows)
    
    # Drop duplicates in case we run this multiple times for the same cities
    dim_city_df = dim_city_df.drop_duplicates(subset=['city_id'])
    fact_weather_df = fact_weather_df.drop_duplicates(subset=['date_id', 'city_id'])
    
    return dim_city_df, fact_weather_df
import sqlite3
import pandas as pd
import os

# Dynamically find the project root folder regardless of where the script is run from
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Gets the src/ folder
PROJECT_ROOT = os.path.dirname(BASE_DIR)              # Goes up one level to project root
DB_DIR = os.path.join(PROJECT_ROOT, 'db')

# Create the db folder if it doesn't exist
os.makedirs(DB_DIR, exist_ok=True)

DB_PATH = os.path.join(DB_DIR, 'weather_dwh.db')

def load_data(dim_city_df, fact_weather_df):
    print("Loading data into SQLite Data Warehouse...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ... (keep the rest of the function exactly the same as before)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Create Tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_city (
            city_id INTEGER PRIMARY KEY,
            city_name TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id INTEGER PRIMARY KEY,
            date TEXT,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            season TEXT
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fact_weather_daily (
            date_id INTEGER,
            city_id INTEGER,
            temperature_max_c REAL,
            temperature_min_c REAL,
            rainfall_mm REAL,
            humidity_pct REAL,
            wind_speed_max_kmh REAL,
            PRIMARY KEY (date_id, city_id),
            FOREIGN KEY (date_id) REFERENCES dim_date(date_id),
            FOREIGN KEY (city_id) REFERENCES dim_city(city_id)
        )
    """)
    
    # 2. Load Dimension City (Insert or Replace handles idempotency)
    for _, row in dim_city_df.iterrows():
        cursor.execute("""
            INSERT OR REPLACE INTO dim_city (city_id, city_name, country, latitude, longitude)
            VALUES (?, ?, ?, ?, ?)
        """, (row['city_id'], row['city_name'], row['country'], row['latitude'], row['longitude']))
        
    # 3. Load Fact Table (Insert or Replace handles idempotency)
    for _, row in fact_weather_df.iterrows():
        # Derive date attributes for dim_date
        date_id = row['date_id']
        date_str = f"{str(date_id)[:4]}-{str(date_id)[4:6]}-{str(date_id)[6:8]}"
        year = int(str(date_id)[:4])
        month = int(str(date_id)[4:6])
        day = int(str(date_id)[6:8])
        
        month_num = month
        if month_num in [12, 1, 2]: season = "Winter"
        elif month_num in [3, 4, 5]: season = "Spring"
        elif month_num in [6, 7, 8]: season = "Summer"
        else: season = "Autumn"
        
        # Insert into dim_date
        cursor.execute("""
            INSERT OR REPLACE INTO dim_date (date_id, date, year, month, day, season)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date_id, date_str, year, month, day, season))
        
        # Insert into fact_weather_daily
        cursor.execute("""
            INSERT OR REPLACE INTO fact_weather_daily 
            (date_id, city_id, temperature_max_c, temperature_min_c, rainfall_mm, humidity_pct, wind_speed_max_kmh)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (row['date_id'], row['city_id'], row['temperature_max_c'], row['temperature_min_c'], 
              row['rainfall_mm'], row['humidity_pct'], row['wind_speed_max_kmh']))
              
    conn.commit()
    conn.close()
    print("Load complete!")

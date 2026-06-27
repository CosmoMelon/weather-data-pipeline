import sqlite3
import pandas as pd
import os

# Dynamically find the database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, 'db', 'weather_dwh.db')

def run_sql_file(filepath):
    print(f"\n--- Running {os.path.basename(filepath)} ---")
    
    # 1. Read the SQL file
    with open(filepath, 'r') as file:
        sql_query = file.read()
        
    # 2. Connect to the database
    conn = sqlite3.connect(DB_PATH)
    
    # 3. Execute the query and load results into a Pandas DataFrame
    df = pd.read_sql_query(sql_query, conn)
    
    # 4. Print the results
    print(df.to_string(index=False))
    
    conn.close()

if __name__ == "__main__":
    # Ask the user which query they want to run
    print("Which query would you like to run?")
    print("1. Hottest Cities")
    print("2. Rainfall Trends")
    print("3. Seasonal Averages")
    
    choice = input("Enter 1, 2, or 3: ")
    
    query_map = {
        '1': '01_hottest_cities.sql',
        '2': '02_rainfall_trends.sql',
        '3': '03_seasonal_averages.sql'
    }
    
    if choice in query_map:
        filepath = os.path.join(BASE_DIR, query_map[choice])
        run_sql_file(filepath)
    else:
        print("Invalid choice.")
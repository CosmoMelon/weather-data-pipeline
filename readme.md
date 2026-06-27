# 🌍 Weather Data Pipeline

A batch-processing ETL pipeline that extracts daily weather metrics (temperature, rainfall, humidity, wind speed) for major global cities, transforms them into a dimensional Star Schema, and loads them into a SQLite Data Warehouse for analytical querying.

---

## 📊 Overview

This project demonstrates core Data Engineering fundamentals:

- **API Integration**: Extracting data from the free Open-Meteo API  
- **Data Modeling**: Designing a Star Schema with Fact and Dimension tables  
- **Idempotency**: Using `INSERT OR REPLACE` logic to ensure pipelines can be rerun without creating duplicate records  
- **Separation of Concerns**: Structuring code into distinct Extract, Transform, and Load (ETL) modules  
- **Analytics**: Writing SQL JOINs to answer business questions  

---

## 🛠️ Tech Stack

- **Language**: Python, SQL  
- **Libraries**: pandas, requests  
- **Database**: SQLite  
- **Data Source**: Open-Meteo API (Historical & Forecast weather data)  

---

## 🗄️ Data Model (Star Schema)

The data is modeled to optimize analytical queries.

- `dim_city`: Contains city metadata (name, country, coordinates)  
- `dim_date`: Contains date attributes (year, month, day, season)  
- `fact_weather_daily`: Central fact table containing measurable weather metrics, linked to dimensions via foreign keys  

## Data Model (Star Schema)

| dim_city (Dimension) | fact_weather_daily (Fact Table) | dim_date (Dimension) |
|----------------------|----------------------------------|----------------------|
| city_id (PK)         | city_id (FK)                    | date_id (PK)         |
| city_name            | date_id (FK)                    | date                 |
| country              | temperature_max_c              | year                 |
| latitude             | temperature_min_c              | month                |
| longitude            | rainfall_mm                    | day                  |
|                      | humidity_pct                   | season               |
|                      | wind_speed_max_kmh            |                      |

https://drawsql.app/draw?t=8f460d20-9fd2-431b-9a5d-8527e86dacda&view=1


---
## 📁 Project Structure

```text
weather-data-pipeline/
│
├── analytics/ # SQL queries for business insights
│   ├── 01_hottest_cities.sql
│   ├── 02_rainfall_trends.sql
│   └── 03_seasonal_averages.sql
│   └── run_query.py
│
├── db/ # Database storage
│   └── weather_dwh.db # SQLite Data Warehouse (auto-generated)
│
├── src/ # ETL source code
│   ├── extract.py # Pulls data from Open-Meteo API
│   ├── transform.py # Cleans data & shapes into Star Schema
│   ├── load.py # Loads data into SQLite (Idempotent)
│   └── pipeline.py # Main orchestration script
│
├── .gitignore
├── requirements.txt
└── README.md
```


---

## 🚀 Setup & Execution

Follow these steps to run the pipeline locally.

### 1. Clone the repository

```bash
git clone https://github.com/cosmomelon/weather-data-pipeline.git
cd weather-data-pipeline
```
---

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

---

### 3. Run the ETL Pipeline

```bash
python src/pipeline.py
```

This will:

- Extract the last 7 days of weather data for:
  - London
  - New York
  - Tokyo

- Transform and load it into:

```text
db/weather_dwh.db
```

---

## 📈 Analytics & Business Insights

Once the pipeline has run, you can execute SQL scripts in the `/analytics` folder using `run_query.py` file or tools like:

- DBeaver  
- VS Code SQLite extension  

---

### 1. Hottest Cities (Last 7 Days)

Finds the average maximum temperature per city.

```sql
SELECT 
    dc.city_name,
    ROUND(AVG(fw.temperature_max_c), 2) as avg_max_temp_c
FROM fact_weather_daily fw
JOIN dim_city dc ON fw.city_id = dc.city_id
GROUP BY dc.city_name
ORDER BY avg_max_temp_c DESC;
```

---

### 2. Rainfall Trends

Tracks total daily rainfall across all tracked cities.

```sql
SELECT 
    dd.date,
    ROUND(SUM(fw.rainfall_mm), 2) as total_rainfall_mm
FROM fact_weather_daily fw
JOIN dim_date dd ON fw.date_id = dd.date_id
GROUP BY dd.date
ORDER BY dd.date ASC;
```

---

### 3. Seasonal Averages

Calculates average temperature and humidity grouped by season.

```sql
SELECT 
    dd.season,
    ROUND(AVG(fw.temperature_max_c), 2) as avg_temp_c,
    ROUND(AVG(fw.humidity_pct), 2) as avg_humidity_pct
FROM fact_weather_daily fw
JOIN dim_date dd ON fw.date_id = dd.date_id
GROUP BY dd.season;
```

---

## 🔮 Future Enhancements

- Orchestration: Integrate Apache Airflow for daily scheduling  
- Cloud Migration: Move SQLite to Snowflake or BigQuery  
- Data Quality Checks: Add Great Expectations for validation (nulls, anomalies, missing data)
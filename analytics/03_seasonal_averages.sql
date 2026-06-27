-- Average temperature and humidity by season
-- (Will only show current season with 7 days of data, but scales as data grows)
SELECT 
    dd.season,
    ROUND(AVG(fw.temperature_max_c), 2) as avg_temp_c,
    ROUND(AVG(fw.humidity_pct), 2) as avg_humidity_pct
FROM fact_weather_daily fw
JOIN dim_date dd ON fw.date_id = dd.date_id
GROUP BY dd.season;
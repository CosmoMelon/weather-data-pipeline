-- Find the average max temperature per city over the last 7 days
SELECT 
    dc.city_name,
    ROUND(AVG(fw.temperature_max_c), 2) as avg_max_temp_c
FROM fact_weather_daily fw
JOIN dim_city dc ON fw.city_id = dc.city_id
GROUP BY dc.city_name
ORDER BY avg_max_temp_c DESC;
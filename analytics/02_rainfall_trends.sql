-- Total rainfall per day across all cities
SELECT 
    dd.date,
    ROUND(SUM(fw.rainfall_mm), 2) as total_rainfall_mm
FROM fact_weather_daily fw
JOIN dim_date dd ON fw.date_id = dd.date_id
GROUP BY dd.date
ORDER BY dd.date ASC;
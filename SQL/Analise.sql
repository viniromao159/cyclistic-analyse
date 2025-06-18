-- Visão geral da análise
WITH overview_by_member_type AS (
	SELECT 
		member_casual,
		ROUND(AVG(EXTRACT(EPOCH FROM trip_length)/60 ), 2)AS avg_trip_duration,
		MODE() WITHIN GROUP(ORDER BY rideable_type) AS most_comum_bike,
		MODE() WITHIN GROUP(ORDER BY start_station_name) FILTER (WHERE start_station_name != 'empty') AS most_comum_start_station,
		MODE() WITHIN GROUP(ORDER BY end_station_name) FILTER (WHERE end_station_name != 'empty') AS most_comum_end_station,
		MODE() WITHIN GROUP(ORDER BY week_start_day) AS most_comum_start_day
	FROM year_tripdata
	GROUP BY member_casual
),

-- Media de tempo das viagens
avg_tripduration AS(
	SELECT
		member_casual,
		ROUND(AVG(EXTRACT(EPOCH FROM trip_length)/60 ), 2) AS avg_tripduration_minutes
	FROM year_tripdata
	GROUP BY member_casual
),

-- Bicicletas mais comuns
bike_count AS (
  SELECT 
    member_casual,
    rideable_type,
    COUNT(*) AS total
  FROM year_tripdata
  GROUP BY member_casual, rideable_type
),

common_bikes AS(
	SELECT 
		member_casual,
		rideable_type,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS bike_rank
	FROM bike_count
),

-- Estações de inicio mais comuns
start_station_count AS (
  SELECT 
    member_casual,
    start_station_name,
    COUNT(*) AS total
  FROM year_tripdata
  WHERE start_station_name != 'empty'
  GROUP BY member_casual, start_station_name
),

common_start_stations AS(
	SELECT 
		member_casual,
		start_station_name,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS station_rank
	FROM start_station_count
),

top5_start_stations AS (
  SELECT *
  FROM common_start_stations
  WHERE station_rank <= 5
),


-- Estações de entregas mais comuns
end_station_count AS (
  SELECT 
    member_casual,
    end_station_name,
    COUNT(*) AS total
  FROM year_tripdata
  WHERE end_station_name != 'empty'
  GROUP BY member_casual, end_station_name
),

common_end_stations AS(
	SELECT 
		member_casual,
		end_station_name,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS station_rank
	FROM end_station_count
),

top5_end_stations AS (
  SELECT *
  FROM common_end_stations
  WHERE station_rank <= 5
),

-- Dias das semanas mais comuns
week_days_count AS (
  SELECT 
    member_casual,
    week_start_day,
    COUNT(*) AS total
  FROM year_tripdata
  GROUP BY member_casual, week_start_day
),

common_week_days AS(
	SELECT 
		member_casual,
		week_start_day,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS week_day_rank
	FROM week_days_count
),

-- Meses com mais viagens
month_count AS (
  SELECT 
    member_casual,
	CASE
		WHEN EXTRACT(MONTH FROM start_date) = 1 THEN 'January'
		WHEN EXTRACT(MONTH FROM start_date) = 2 THEN 'February'
		WHEN EXTRACT(MONTH FROM start_date) = 3 THEN 'March'
		WHEN EXTRACT(MONTH FROM start_date) = 4 THEN 'April'
		WHEN EXTRACT(MONTH FROM start_date) = 5 THEN 'May'
		WHEN EXTRACT(MONTH FROM start_date) = 6 THEN 'June'
		WHEN EXTRACT(MONTH FROM start_date) = 7 THEN 'July'
		WHEN EXTRACT(MONTH FROM start_date) = 8 THEN 'August'
		WHEN EXTRACT(MONTH FROM start_date) = 9 THEN 'September'
		WHEN EXTRACT(MONTH FROM start_date) = 10 THEN  'October'
		WHEN EXTRACT(MONTH FROM start_date) = 11 THEN  'November'
		ELSE 'December'
	END AS month_name,
    COUNT(*) AS total
  FROM year_tripdata
  GROUP BY member_casual, month_name
),

month_trips AS(
	SELECT 
		member_casual,
		month_name,
		total,
		ROW_NUMBER() OVER(PARTITION BY member_casual ORDER BY total DESC) AS month_rank
	FROM month_count
),

top3_month AS (
SELECT * 
FROM month_trips
WHERE month_rank <= 3
)

-- QUERY
SELECT * FROM [CTE]



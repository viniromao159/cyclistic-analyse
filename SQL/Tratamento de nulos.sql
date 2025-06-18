SELECT
  COUNT(*) FILTER (WHERE ride_id IS NULL) AS ride_id,
  COUNT(*) FILTER (WHERE rideable_type IS NULL) AS rideable_type,
  COUNT(*) FILTER (WHERE start_station_name IS NULL) AS start_station_name,
  COUNT(*) FILTER (WHERE end_station_name IS NULL) AS end_station_name,
  COUNT(*) FILTER (WHERE member_casual IS NULL) AS member_casual,
  COUNT(*) FILTER (WHERE start_date IS NULL) AS start_date,
  COUNT(*) FILTER (WHERE start_hour IS NULL) AS start_hour,
  COUNT(*) FILTER (WHERE week_start_day IS NULL) AS week_start_day,
  COUNT(*) FILTER (WHERE week_start_day_num IS NULL) AS week_start_day_num,
  COUNT(*) FILTER (WHERE ended_date IS NULL) AS ended_date,
  COUNT(*) FILTER (WHERE ended_hour IS NULL) AS ended_hour,
  COUNT(*) FILTER (WHERE trip_length IS NULL) AS trip_length
FROM year_tripdata;

UPDATE public."year_tripdata"
SET end_station_name = 'empty'
WHERE end_station_name IS NULL;

UPDATE public."year_tripdata"
SET start_station_name = 'empty'
WHERE start_station_name IS NULL;
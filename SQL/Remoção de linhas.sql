DELETE FROM year_tripdata
WHERE trip_length < INTERVAL '0 seconds'
   OR trip_length > INTERVAL '1 day'
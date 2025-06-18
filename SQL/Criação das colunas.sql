ALTER TABLE public.year_tripdata
ADD COLUMN start_date DATE,
ADD COLUMN start_hour TIME,
ADD COLUMN week_start_day TEXT,
ADD COLUMN week_start_day_num INTEGER,
ADD COLUMN ended_date DATE,
ADD COLUMN ended_hour TIME,
ADD COLUMN trip_length INTERVAL;


UPDATE public.year_tripdata
SET 
    start_date = DATE(started_at),
    start_hour = started_at::TIME,
	week_start_day = TO_CHAR(started_at, 'Day'),
    week_start_day_num = EXTRACT(DOW FROM started_at)::INTEGER,
    ended_date = DATE(ended_at),
    ended_hour = ended_at::TIME,
    trip_length = ended_at - started_at;
    
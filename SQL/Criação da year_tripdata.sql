CREATE TABLE year_tripdata AS
SELECT * FROM public."202401-divvy-tripdata"
UNION ALL
SELECT * FROM public."202402-divvy-tripdata"
UNION ALL
SELECT * FROM public."202403-divvy-tripdata"
UNION ALL
SELECT * FROM public."202404-divvy-tripdata"
UNION ALL
SELECT * FROM public."202405-divvy-tripdata"
UNION ALL
SELECT * FROM public."202406-divvy-tripdata"
UNION ALL
SELECT * FROM public."202407-divvy-tripdata"
UNION ALL
SELECT * FROM public."202408-divvy-tripdata"
UNION ALL
SELECT * FROM public."202409-divvy-tripdata"
UNION ALL
SELECT * FROM public."202410-divvy-tripdata"
UNION ALL
SELECT * FROM public."202411-divvy-tripdata"
UNION ALL
SELECT * FROM public."202412-divvy-tripdata";
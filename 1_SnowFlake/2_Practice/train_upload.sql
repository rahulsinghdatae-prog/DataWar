-- Reusable SQL: upload train.csv to the table stage and verify
-- Connection config lives in C:\Users\user\.snowflake\connections.toml ([default])

-- 1. Upload the file (auto-compress -> train.csv.gz)
PUT 'file:///C:/Users/user/Desktop/DE/Projects/DataWar/1_SnowFlake/5_Data/archive/train.csv' @%TAXI_DRIVE_SMALL_FILES;

-- 2. Verify it reached the stage
LIST @%TAXI_DRIVE_SMALL_FILES;

-- 3. (Optional) load into the table
-- COPY INTO RAHUL_DB.PUBLIC.TAXI_DRIVE_SMALL_FILES
-- FROM @%TAXI_DRIVE_SMALL_FILES/train.csv.gz
-- FILE_FORMAT=(TYPE=CSV SKIP_HEADER=1 FIELD_OPTIONALLY_ENCLOSED_BY='"' NULL_IF=('','NULL','null'))
-- ON_ERROR='CONTINUE';
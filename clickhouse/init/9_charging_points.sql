CREATE TABLE sensors.charging_station
(
    sensor_uuid UUID,
    sensor_name String,
    group_name Nullable(String) default null,
    timestamp   DateTime64,
    is_occupied Bool,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- -- Daily occupied
-- CREATE TABLE sensors.charging_points_daily
-- (
--     sensor_name         String,
--     date                Date,
--     avg_occupancy       Float32,
--     insertion_timestamp DateTime64(6) default now64()
-- ) ENGINE = MergeTree()
--       ORDER BY (sensor_name, date);

-- CREATE MATERIALIZED VIEW sensors.charging_points_daily_mv
--     TO sensors.charging_points_daily AS
-- SELECT sensor_name,
--        toStartOfDay(timestamp) AS date,
--        avg(is_occupied)        AS avg_occupancy
-- FROM sensors.charging_points
-- GROUP BY sensor_name, date;

-- -- Weekly occupied
-- CREATE TABLE sensors.charging_points_weekly
-- (
--     sensor_name         String,
--     date                DateTime64,
--     avg_occupancy       Float32,
--     insertion_timestamp DateTime64(6) default now64()
-- ) ENGINE = MergeTree()
--       ORDER BY (sensor_name, date);

-- CREATE MATERIALIZED VIEW sensors.charging_points_weekly_mv
--     TO sensors.charging_points_weekly AS
-- SELECT sensor_name,
--        toStartOfWeek(timestamp) AS date,
--        avg(is_occupied)         AS avg_occupancy
-- FROM sensors.charging_points
-- GROUP BY sensor_name, date;


-- -- 5m averages
-- CREATE TABLE sensors.charging_points_5m
-- (
--     sensor_name         String,
--     date                DateTime64,
--     avg_occupancy       Float32,
--     insertion_timestamp DateTime64(6) default now64()
-- ) ENGINE = MergeTree()
--       ORDER BY (sensor_name, date);
--
-- CREATE MATERIALIZED VIEW sensors.charging_points_5m_mv
--     TO sensors.charging_points_5m AS
-- SELECT sensor_name,
--        toStartOfFiveMinutes(timestamp) AS date,
--        avg(is_occupied)                AS avg_occupancy
-- FROM sensors.charging_points
-- GROUP BY sensor_name, date;
--

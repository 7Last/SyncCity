CREATE TABLE sensors.parking
(
    sensor_uuid UUID,
    sensor_name String,
    group_name Nullable(String) default null,
    timestamp   DateTime64,
    is_occupied BOOL,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- 5m averages
CREATE TABLE sensors.parking_5m
(
    sensor_name         String,
    date                DateTime64,
    avg_occupancy       Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.parking_5m_mv
    TO sensors.parking_5m AS
SELECT sensor_name,
       toStartOfFiveMinutes(timestamp) AS date,
       avg(is_occupied)                AS avg_occupancy
FROM sensors.parking
GROUP BY sensor_name, date;

-- Weekly occupancy
CREATE TABLE sensors.parking_weekly
(
    sensor_name         String,
    date                DateTime64,
    avg_occupancy       Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.parking_weekly_mv
    TO sensors.parking_weekly AS
SELECT sensor_name,
       toStartOfWeek(timestamp) AS date,
       avg(is_occupied)         AS avg_occupancy
FROM sensors.parking
GROUP BY sensor_name, date;

-- Daily occupancy
CREATE TABLE sensors.parking_daily
(
    sensor_name         String,
    date                Date,
    avg_occupancy       Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.parking_daily_mv
    TO sensors.parking_daily AS
SELECT sensor_name,
       toStartOfDay(timestamp) AS date,
       avg(is_occupied)        AS avg_occupancy
FROM sensors.parking
GROUP BY sensor_name, date;
CREATE TABLE sensors.humidity
(
    sensor_uuid UUID,
    sensor_name String,
    timestamp   DateTime64,
    value       Float32,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- 5m averages
CREATE TABLE sensors.humidity_5m
(
    sensor_name         String,
    date                DateTime64,
    avg_humidity        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.humidity_5m_mv
            TO sensors.humidity_5m AS
SELECT sensor_name,
       toStartOfFiveMinutes(timestamp) AS date,
       avg(value)                      AS avg_humidity
FROM sensors.humidity
GROUP BY sensor_name, date;

-- Weekly humidity
CREATE TABLE sensors.humidity_weekly
(
    sensor_name         String,
    date                DateTime64,
    avg_humidity        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.humidity_weekly_mv
    TO sensors.humidity_weekly AS
SELECT sensor_name,
       toStartOfWeek(timestamp) AS date,
       avg(value)               AS avg_humidity
FROM sensors.humidity
GROUP BY sensor_name, date;

-- Daily humidity
CREATE TABLE sensors.humidity_daily
(
    sensor_name         String,
    date                Date,
    avg_humidity        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.humidity_daily_mv
    TO sensors.humidity_daily AS
SELECT sensor_name,
       toStartOfDay(timestamp) AS date,
       avg(value)              AS avg_humidity
FROM sensors.humidity
GROUP BY sensor_name, date;
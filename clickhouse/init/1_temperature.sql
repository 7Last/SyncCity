CREATE TABLE sensors.temperature
(
    sensor_uuid UUID,
    sensor_name String,
    group_name  Nullable(String) default null,
    timestamp   DateTime64,
    value       Float32,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- 5m averages
CREATE TABLE sensors.temperature_5m
(
    sensor_name         String,
    date                DateTime64,
    avg_temperature     Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.temperature_5m_mv
            TO sensors.temperature_5m AS
SELECT sensor_name,
       toStartOfFiveMinutes(timestamp) AS date,
       avg(value)                      AS avg_temperature
FROM sensors.temperature
GROUP BY sensor_name, date;

-- Weekly temperature
CREATE TABLE sensors.temperature_weekly
(
    sensor_name         String,
    date                DateTime64,
    avg_temperature     Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.temperature_weekly_mv
    TO sensors.temperature_weekly AS
SELECT sensor_name,
       toStartOfWeek(timestamp) AS date,
       avg(value)               AS avg_temperature
FROM sensors.temperature
GROUP BY sensor_name, date;

-- Daily temperature
CREATE TABLE sensors.temperature_daily
(
    sensor_name         String,
    date                Date,
    avg_temperature     Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.temperature_daily_mv
    TO sensors.temperature_daily AS
SELECT sensor_name,
       toStartOfDay(timestamp) AS date,
       avg(value)              AS avg_temperature
FROM sensors.temperature
GROUP BY sensor_name, date;
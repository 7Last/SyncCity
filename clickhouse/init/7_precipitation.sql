CREATE TABLE sensors.precipitation
(
    sensor_uuid UUID,
    sensor_name String,
    timestamp   DateTime64,
    value       Float32,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- Hourly precipitation
CREATE TABLE sensors.precipitation_1h
(
    sensor_name         String,
    date                DateTime64,
    avg_precipitation        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.precipitation_1h_mv
            TO sensors.precipitation_1h AS
SELECT sensor_name,
       toStartOfHour(timestamp) AS date,
       avg(value)                      AS avg_precipitation
FROM sensors.precipitation
GROUP BY sensor_name, date;

-- Daily precipitation
CREATE TABLE sensors.precipitation_daily
(
    sensor_name         String,
    date                DateTime64,
    avg_precipitation        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.precipitation_daily_mv
    TO sensors.precipitation_daily AS
SELECT sensor_name,
       toStartOfDay(timestamp) AS date,
       avg(value)               AS avg_precipitation
FROM sensors.precipitation
GROUP BY sensor_name, date;

-- Monthly precipitation
CREATE TABLE sensors.precipitation_monthly
(
    sensor_name         String,
    date                Date,
    avg_precipitation        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.precipitation_monthly_mv
    TO sensors.precipitation_monthly AS
SELECT sensor_name,
       toStartOfMonth(timestamp) AS date,
       avg(value)              AS avg_precipitation
FROM sensors.precipitation
GROUP BY sensor_name, date;

-- Yearly precipitation
CREATE TABLE sensors.precipitation_yearly
(
    sensor_name         String,
    date                Date,
    avg_precipitation        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.precipitation_yearly_mv
    TO sensors.precipitation_yearly AS
SELECT sensor_name,
       toStartOfYear(timestamp) AS date,
       avg(value)              AS avg_precipitation
FROM sensors.precipitation
GROUP BY sensor_name, date;
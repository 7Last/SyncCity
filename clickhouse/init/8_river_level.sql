CREATE TABLE sensors.river_level
(
    sensor_uuid UUID,
    sensor_name String,
    timestamp   DateTime64,
    value       Float32,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- Hourly river_level
CREATE TABLE sensors.river_level_1h
(
    sensor_name         String,
    date                DateTime64,
    avg_river_level        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.river_level_1h_mv
            TO sensors.river_level_1h AS
SELECT sensor_name,
       toStartOfHour(timestamp) AS date,
       avg(value)                      AS avg_river_level
FROM sensors.river_level
GROUP BY sensor_name, date;

-- Daily river_level
CREATE TABLE sensors.river_level_daily
(
    sensor_name         String,
    date                DateTime64,
    avg_river_level       Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.river_level_daily_mv
    TO sensors.river_level_daily AS
SELECT sensor_name,
       toStartOfDay(timestamp) AS date,
       avg(value)               AS avg_river_level
FROM sensors.river_level
GROUP BY sensor_name, date;

-- Monthly river_level
CREATE TABLE sensors.river_level_monthly
(
    sensor_name         String,
    date                Date,
    avg_river_level        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.river_level_monthly_mv
    TO sensors.river_level_monthly AS
SELECT sensor_name,
       toStartOfMonth(timestamp) AS date,
       avg(value)              AS avg_river_level
FROM sensors.river_level
GROUP BY sensor_name, date;

-- Yearly river_level
CREATE TABLE sensors.river_level_yearly
(
    sensor_name         String,
    date                Date,
    avg_river_level        Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.river_level_yearly_mv
    TO sensors.river_level_yearly AS
SELECT sensor_name,
       toStartOfWeek(timestamp) AS date,
       avg(value)              AS avg_river_level
FROM sensors.river_level
GROUP BY sensor_name, date;
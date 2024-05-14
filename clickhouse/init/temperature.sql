CREATE TABLE sensors.temperatures
(
    sensor_uuid UUID,
    sensor_name String,
    timestamp   DateTime64,
    value       Float32,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- Real-time
CREATE TABLE sensors.temperatures_realtime
(
    sensor_name         String,
    value               Float32,
    insertion_timestamp DateTime64 DEFAULT now()
) ENGINE = MergeTree()
      ORDER BY (sensor_name);

CREATE MATERIALIZED VIEW sensors.temperatures_realtime_mv
    TO sensors.temperatures_realtime AS
SELECT sensor_name,
       avg(value) AS value
FROM sensors.temperatures
WHERE (timestamp >= subtractMinutes(now(), 5) and timestamp <= now())
GROUP BY sensor_name;

-- Monthly temperatures
CREATE TABLE sensors.temperatures_monthly
(
    sensor_name         String,
    date                Datetime64,
    avg_temperature     Float32,
    insertion_timestamp DateTime64 DEFAULT now()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.temperatures_monthly_mv
    TO sensors.temperatures_monthly AS
SELECT sensor_name,
       toStartOfMonth(timestamp) AS date,
       avg(value)                AS avg_temperature
FROM sensors.temperatures
GROUP BY sensor_name, date;

-- Daily temperatures
CREATE TABLE sensors.temperatures_daily
(
    sensor_name         String,
    date                Date,
    avg_temperature     Float32,
    insertion_timestamp DateTime64 DEFAULT now()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.temperatures_daily_mv
    TO sensors.temperatures_daily AS
SELECT sensor_name,
       toStartOfDay(timestamp) AS date,
       avg(value)              AS avg_temperature
FROM sensors.temperatures
GROUP BY sensor_name, date;
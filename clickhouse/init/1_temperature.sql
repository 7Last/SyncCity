CREATE TABLE sensors.temperature_kafka
(
    data String
) ENGINE = Kafka('redpanda:9092', 'temperature', 'ch_group_1', 'JSONAsString');

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

CREATE MATERIALIZED VIEW sensors.temperature_topic_mv TO sensors.temperatures as
SELECT JSONExtractString(data, 'sensor_name')                             AS sensor_name,
       toUUID(JSONExtractString(data, 'sensor_uuid'))                     AS sensor_uuid,
       parseDateTime64BestEffort(JSONExtractString(data, 'timestamp')) AS timestamp,
       JSONExtractFloat(data, 'value')                                    AS value,
       JSONExtractFloat(data, 'latitude')                                 AS latitude,
       JSONExtractFloat(data, 'longitude')                                AS longitude
FROM sensors.temperature_kafka;

-- 5m averages
CREATE TABLE sensors.temperatures_5m
(
    sensor_name         String,
    date                DateTime64,
    avg_temperature     Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.temperatures_5m_mv
            TO sensors.temperatures_5m AS
SELECT sensor_name,
       toStartOfFiveMinutes(timestamp) AS date,
       avg(value)                      AS avg_temperature
FROM sensors.temperatures
GROUP BY sensor_name, date;

-- Weekly temperatures
CREATE TABLE sensors.temperatures_weekly
(
    sensor_name         String,
    date                DateTime64,
    avg_temperature     Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.temperatures_weekly_mv
    TO sensors.temperatures_weekly AS
SELECT sensor_name,
       toStartOfWeek(timestamp) AS date,
       avg(value)               AS avg_temperature
FROM sensors.temperatures
GROUP BY sensor_name, date;

-- Daily temperatures
CREATE TABLE sensors.temperatures_daily
(
    sensor_name         String,
    date                Date,
    avg_temperature     Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.temperatures_daily_mv
    TO sensors.temperatures_daily AS
SELECT sensor_name,
       toStartOfDay(timestamp) AS date,
       avg(value)              AS avg_temperature
FROM sensors.temperatures
GROUP BY sensor_name, date;
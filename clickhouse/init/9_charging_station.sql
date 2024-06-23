CREATE TABLE sensors.charging_station
(
    sensor_uuid           UUID,
    sensor_name           String,
    group_name            Nullable(String) default null,
    timestamp             DateTime64,
    vehicle_type          Nullable(String) default null,
    battery_level         Nullable(Float32) default null,
    kwh_supplied          Float32,
    remaining_charge_time Nullable(int) default null,
    elapsed_time          Nullable(int) default null,
    latitude              Float64,
    longitude             Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- 5m averages
CREATE TABLE sensors.charging_station_5m
(
    sensor_name         String,
    date                DateTime64,
    avg_kwh_supplied    Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.charging_station_5m_mv
            TO sensors.charging_station_5m AS
SELECT sensor_name,
       toStartOfFiveMinutes(timestamp) AS date,
       avg(kwh_supplied)               AS avg_kwh_supplied
FROM sensors.charging_station
GROUP BY sensor_name, date;

-- Weekly charging_station
CREATE TABLE sensors.charging_station_weekly
(
    sensor_name         String,
    date                DateTime64,
    avg_kwh_supplied    Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.charging_station_weekly_mv
    TO sensors.charging_station_weekly AS
SELECT sensor_name,
       toStartOfWeek(timestamp) AS date,
       avg(kwh_supplied)        AS avg_kwh_supplied
FROM sensors.charging_station
GROUP BY sensor_name, date;

-- Daily charging_station
CREATE TABLE sensors.charging_station_daily
(
    sensor_name         String,
    date                Date,
    avg_kwh_supplied    Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.charging_station_daily_mv
    TO sensors.charging_station_daily AS
SELECT sensor_name,
       toStartOfDay(timestamp) AS date,
       avg(kwh_supplied)       AS avg_kwh_supplied
FROM sensors.charging_station
GROUP BY sensor_name, date;
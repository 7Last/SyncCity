CREATE TABLE sensors.traffic
(
    sensor_uuid UUID,
    sensor_name String,
    timestamp   DateTime64,
    latitude    Float64,
    longitude   Float64,
    vehicles    Int32,
    avg_speed   Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- Real-time data
CREATE TABLE sensors.traffic_realtime
(
    sensor_name         String,
    vehicles            Int32,
    speed               Float32,
    insertion_timestamp DateTime64 DEFAULT now()
) ENGINE = MergeTree()
      ORDER BY (sensor_name);

CREATE MATERIALIZED VIEW sensors.traffic_realtime_mv TO sensors.traffic_realtime
AS
SELECT sensor_name,
       avg(vehicles)  as vehicles,
       avg(avg_speed) as speed
FROM sensors.traffic
WHERE (timestamp >= subtractMinutes(now(), 5) and timestamp <= now())
GROUP BY sensor_name;

-- Hourly vehicles
CREATE TABLE sensors.vehicles_hourly
(
    sensor_name         String,
    timestamp           DateTime64,
    vehicles            Int32,
    insertion_timestamp DateTime64 DEFAULT now()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, timestamp);

CREATE MATERIALIZED VIEW sensors.vehicles_hourly_mv TO sensors.vehicles_hourly
AS
SELECT sensor_name,
       toStartOfHour(timestamp) as timestamp,
       avg(vehicles)            as vehicles -- TODO: convert in sum
FROM sensors.traffic
GROUP BY sensor_name, timestamp;

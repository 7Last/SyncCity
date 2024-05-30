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

-- 1h traffic
CREATE TABLE sensors.traffic_1h
(
    sensor_name         String,
    date           DateTime64,
    vehicles            Int32,
    speed               Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.traffic_1h_mv TO sensors.traffic_1h
AS
SELECT sensor_name,
       toStartOfHour(timestamp) as date,
       avg(vehicles)                  as vehicles,
       avg(avg_speed)                 as speed
FROM sensors.traffic
GROUP BY sensor_name, date;
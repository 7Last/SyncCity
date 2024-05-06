CREATE TABLE sensors.traffic
(
    sensor_uuid       UUID,
    sensor_name       String,
    timestamp         DateTime64,
    latitude          Float64,
    longitude         Float64,
    vehicles_per_hour Float32,
    avg_speed         Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

CREATE TABLE sensors.traff1c
(
    sensor_uuid          UUID,
    sensor_name          String,
    timestamp1m          DATETIME64,
    latitude             Float64,
    longitude            Float64,
    avg_vehicles_per_hour Float32,
    avg_speed            Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp1m);

CREATE MATERIALIZED VIEW sensors.traffic1m_mv
    TO sensors.traff1c
AS
SELECT toStartOfMinute(timestamp) AS timestamp1m,
       sensor_uuid,
       sensor_name,
       avg(vehicles_per_hour)     as avg_vehicles_per_hour,
       avg(avg_speed)             as avg_speed,
       latitude,
       longitude
FROM sensors.traffic
GROUP BY (timestamp1m, sensor_uuid, sensor_name, latitude, longitude);

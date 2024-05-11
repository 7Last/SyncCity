CREATE TABLE sensors.ecological_island
(
    sensor_uuid       UUID,
    sensor_name       String,
    timestamp         DateTime64,
    latitude          Float64,
    longitude         Float64,
    starting_filling  Float32,
    max_filling       Float32,
    min_filling       Float32,
    filling_speed     Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

CREATE TABLE sensors.ecological_island1m
(
    sensor_uuid          UUID,
    sensor_name          String,
    timestamp1m          DATETIME64,
    latitude             Float64,
    longitude            Float64,
    --???
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp1m);

CREATE MATERIALIZED VIEW sensors.ecological_island1m_mv
    TO sensors.ecological_island1m
AS
SELECT toStartOfMinute(timestamp) AS timestamp1m,
       sensor_uuid,
       sensor_name,
       --avg(vehicles_per_hour)     as avg_vehicles_per_hour,
       --avg(avg_speed)             as avg_speed,
       latitude,
       longitude
FROM sensors.ecological_island
GROUP BY (timestamp1m, sensor_uuid, sensor_name, latitude, longitude);

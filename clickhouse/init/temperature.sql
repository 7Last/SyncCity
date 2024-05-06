CREATE TABLE sensors.temperature
(
    sensor_uuid UUID,
    sensor_name String,
    timestamp   DateTime64,
    value       Float32,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

CREATE TABLE sensors.temperatures1m
(
    sensor_uuid         UUID,
    sensor_name String,
    timestamp1m         DATETIME64,
    avgTemperature      Float32,
    latitude            Float64,
    longitude           Float64,
    insertion_timestamp DATETIME DEFAULT now()
)
    ENGINE = MergeTree()
        ORDER BY (timestamp1m, longitude, latitude);

CREATE MATERIALIZED VIEW sensors.temperatures1m_mv
    TO sensors.temperatures1m
AS
SELECT 
    sensor_uuid,
    sensor_name,
    toStartOfMinute(timestamp) AS timestamp1m,
    avg(value) as avgTemperature,
    latitude,
    longitude,
    now() AS insertion_timestamp
FROM sensors.temperature
GROUP BY (sensor_uuid, sensor_name, timestamp1m, latitude, longitude);

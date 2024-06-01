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
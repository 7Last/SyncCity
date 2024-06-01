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
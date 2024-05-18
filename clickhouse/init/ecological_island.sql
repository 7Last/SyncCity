CREATE TABLE sensors.ecological_island
(
    sensor_uuid       UUID,
    sensor_name       String,
    timestamp         DateTime64,
    latitude          Float64,
    longitude         Float64,
    filling_value     Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

CREATE TABLE sensors.traffic
(
    sensor_uuid       UUID,
    timestamp         DateTime64,
    latitude          Float64,
    longitude         Float64,
    vehicles_per_hour Float32,
    avg_speed         Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

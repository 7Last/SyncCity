CREATE TABLE sensors.air_quality
(
    sensor_uuid UUID,
    sensor_name String,
    group_name  Nullable(String) default null,
    timestamp   DateTime64,
    latitude    Float64,
    longitude   Float64,
    pm25        Float32,
    pm10        Float32,
    no2         Float32,
    o3          Float32,
    so2         Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

CREATE TABLE sensors.recycling_point
(
    sensor_uuid   UUID,
    sensor_name   String,
    group_name    Nullable(String) default null,
    timestamp     DateTime64,
    latitude      Float64,
    longitude     Float64,
    filling       Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

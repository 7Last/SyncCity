CREATE TABLE sensors.parking
(
    sensor_uuid UUID,
    sensor_name String,
    group_name Nullable(String) default null,
    timestamp   DateTime64,
    is_occupied Bool,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);
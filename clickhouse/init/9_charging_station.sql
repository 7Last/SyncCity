CREATE TABLE sensors.charging_station
(
    sensor_uuid     UUID,
    sensor_name     String,
    group_name      Nullable(String) default null,
    timestamp       DateTime64,
    is_being_used   Bool,
    kwh_consumption Float32,
    latitude        Float64,
    longitude       Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

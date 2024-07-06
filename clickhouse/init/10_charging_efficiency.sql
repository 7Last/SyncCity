CREATE TABLE sensors.charging_efficiency
(
    sensor_uuid      UUID,
    sensor_names     Array(String),
    group_name       String,
    timestamp        DateTime64,
    efficiency_rate  Float64,
    utilization_rate Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);
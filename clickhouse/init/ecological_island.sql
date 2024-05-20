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

-- prev_value
/*
CREATE TABLE sensors.ecological_island_prev_value
(
    sensor_uuid       UUID,
    sensor_name         String,
    timestamp         DateTime64,
    insertion_timestamp DateTime64(6) default now64(),
    filling_value     Float32,
    prev_value        Nullable(Float32)
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

CREATE MATERIALIZED VIEW sensors.ecological_island_prev_value_mv
    TO sensors.ecological_island_prev_value AS
SELECT
    ecological_island.sensor_uuid,
    ecological_island.sensor_name,
    ecological_island.timestamp,
    ecological_island.filling_value,
    prev.filling_value AS prev_value
FROM sensors.ecological_island
JOIN sensors.ecological_island AS prev
ON ecological_island.sensor_uuid = prev.sensor_uuid
WHERE prev.timestamp < ecological_island.timestamp
ORDER BY prev.timestamp DESC
LIMIT 1;
*/
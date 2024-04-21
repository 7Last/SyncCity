CREATE TABLE sensors.temperature
(
    sensor_uuid UUID,
    timestamp   DateTime64,
    value       Float32,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- CREATE MATERIALIZED VIEW sensors.temperatures_topic_mv TO sensors.temperatures AS
-- SELECT JSONExtractString(data, 'sensor_uuid')               AS sensor_uuid,
--        toDateTime64(JSONExtractString(data, 'timestamp'), 0) AS timestamp,
--        JSONExtractFloat(data, 'readings', 1, 'value')        AS value, -- arrays start from 1
--        JSONExtractFloat(data, 'location', 'coordinates', 1)  AS latitude,
--        JSONExtractFloat(data, 'location', 'coordinates', 2)  AS longitude
-- FROM sensors.temperatures_topic_kafka;

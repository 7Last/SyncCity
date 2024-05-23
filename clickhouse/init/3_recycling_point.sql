CREATE TABLE sensors.recycling_point_kafka
(
    data String
) ENGINE = Kafka('redpanda:9092', 'recycling_point', 'ch_group_1', 'JSONAsString');

CREATE TABLE sensors.recycling_point
(
    sensor_uuid   UUID,
    sensor_name   String,
    timestamp     DateTime64,
    latitude      Float64,
    longitude     Float64,
    filling_value Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

CREATE MATERIALIZED VIEW sensors.recycling_point_topic_mv TO sensors.recycling_point as
SELECT JSONExtractString(data, 'sensor_name')                          AS sensor_name,
       toUUID(JSONExtractString(data, 'sensor_uuid'))                  AS sensor_uuid,
       parseDateTime64BestEffort(JSONExtractString(data, 'timestamp')) AS timestamp,
       JSONExtractFloat(data, 'filling_value')                         AS filling_value,
       JSONExtractFloat(data, 'latitude')                              AS latitude,
       JSONExtractFloat(data, 'longitude')                             AS longitude
FROM sensors.recycling_point_kafka;

CREATE TABLE sensors.recycling_point_5m
(
    sensor_name         String,
    date                DateTime64,
    avg_filling_value   Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.recycling_point_5m_mv
    TO sensors.recycling_point_5m AS
SELECT sensor_name,
       toStartOfFiveMinutes(timestamp) AS date,
       avg(filling_value)              AS avg_filling_value
from sensors.recycling_point
GROUP BY sensor_name, date;

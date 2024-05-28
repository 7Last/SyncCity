CREATE TABLE sensors.traffic_kafka
(
    data String
) ENGINE = Kafka('redpanda:9092', 'traffic', 'ch_group_1', 'JSONAsString');

CREATE TABLE sensors.traffic
(
    sensor_uuid UUID,
    sensor_name String,
    timestamp   DateTime64,
    latitude    Float64,
    longitude   Float64,
    vehicles    Int32,
    avg_speed   Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

CREATE MATERIALIZED VIEW sensors.traffic_topic_mv TO sensors.traffic as
SELECT JSONExtractString(data, 'sensor_name')                AS sensor_name,
       toUUID(JSONExtractString(data, 'sensor_uuid'))        AS sensor_uuid,
       parseDateTime64BestEffort(JSONExtractString(data, 'timestamp')) AS timestamp,
       JSONExtractFloat(data, 'vehicles')                    AS vehicles,
       JSONExtractFloat(data, 'avg_speed')                   AS avg_speed,
       JSONExtractFloat(data, 'latitude')                    AS latitude,
       JSONExtractFloat(data, 'longitude')                   AS longitude
FROM sensors.traffic_kafka;

-- 1h traffic
CREATE TABLE sensors.traffic_1h
(
    sensor_name         String,
    date           DateTime64,
    vehicles            Int32,
    speed               Float32,
    insertion_timestamp DateTime64(6) default now64()
) ENGINE = MergeTree()
      ORDER BY (sensor_name, date);

CREATE MATERIALIZED VIEW sensors.traffic_1h_mv TO sensors.traffic_1h
AS
SELECT sensor_name,
       toStartOfHour(timestamp) as date,
       avg(vehicles)                  as vehicles,
       avg(avg_speed)                 as speed
FROM sensors.traffic
GROUP BY sensor_name, date;
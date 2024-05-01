CREATE TABLE sensors.humidity
(
    sensor_uuid UUID,
    timestamp DATETIME64,
    value     Float64,
    type      String,
    latitude  Float64,
    longitude Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);

-- --------------------------
--      START AGGREGATE 
-- --------------------------
CREATE TABLE sensors.humidity1m
(
    sensor_uuid         UUID,
    timestamp1m         DATETIME64,
    avgHumidity         Float64,
    latitude            Float64,
    longitude           Float64,
    insertion_timestamp DATETIME DEFAULT now()
)
    ENGINE = MergeTree()
        ORDER BY (timestamp1m, longitude, latitude);

CREATE MATERIALIZED VIEW sensors.humidity1m_mv
    TO sensors.humidity1m
AS
SELECT sensor_uuid,
       toStartOfMinute(timestamp) AS timestamp1m,
       avg(value)                 as avgHumidity,
       latitude,
       longitude,
       now()                      AS insertion_timestamp
FROM sensors.humidity
GROUP BY (sensor_uuid, timestamp1m, latitude, longitude);
-- ------------------------
--      END AGGREGATE
-- ------------------------
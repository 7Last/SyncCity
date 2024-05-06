CREATE TABLE sensors.traffic
(
    sensor_uuid       UUID,
    timestamp         DateTime64,
    latitude          Float64,
    longitude         Float64,
    vehicles_per_hour Float32,
    avg_speed         Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);


-- --------------------------
--      START AGGREGATE 
-- --------------------------
CREATE TABLE sensors.traff1c
(
    sensor_uuid          UUID,
    timestamp1m          DATETIME64,
    latitude             Float64,
    longitude            Float64,
    avg_vehicles_per_hour Float32,
    avg_speed            Float32
) ENGINE = MergeTree()
      ORDER BY (timestamp1m, sensor_uuid, latitude, longitude);

CREATE MATERIALIZED VIEW sensors.traff1c_mv
    TO sensors.traff1c
AS
SELECT toStartOfMinute(timestamp) AS timestamp1m,
       sensor_uuid,
       avg(vehicles_per_hour)     as avg_vehicles_per_hour,
       avg(avg_speed)             as avg_speed,
       latitude,
       longitude
FROM sensors.traffic
GROUP BY (timestamp1m, sensor_uuid, latitude, longitude);
-- ------------------------
--      END AGGREGATE
-- ------------------------

-- -------------------------------------------------------
--VISTA CHE RESTITUISCE LAT E LON ALLA TABELLA MAP
-- -------------------------------------------------------
CREATE MATERIALIZED VIEW sensors.map1_mv
    TO sensors.map
AS
SELECT DISTINCT
    sensor_uuid,
    latitude,
    longitude
FROM sensors.traffic
GROUP BY (sensor_uuid, latitude, longitude);
-- -------------------------------------------------------
--TAVOLA CONTENENTE LE COORDINATE DI TUTTI I SENSORI
-- -------------------------------------------------------
CREATE TABLE sensors.map
(
    sensor_uuid UUID,
    latitude    Float64,
    longitude   Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid);



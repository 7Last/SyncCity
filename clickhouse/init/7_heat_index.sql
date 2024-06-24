CREATE TABLE sensors.heat_index
(
    sensor_names             Array(String),
    group_name               String,
    timestamp                DateTime64,
    heat_index               Float32,
    avg_temperature          Float32,
    avg_humidity             Float32,
    center_of_mass_latitude  Float32,
    center_of_mass_longitude Float32,
    radius_in_km             Float32
) ENGINE = MergeTree()
      ORDER BY (group_name, timestamp);

-- daily heat index
CREATE TABLE sensors.heat_index_daily
(
    sensor_names    Array(String),
    group_name      String,
    date            Date,
    heat_index      Float32,
    avg_temperature Float32,
    avg_humidity    Float32
) ENGINE = MergeTree()
      ORDER BY (group_name, date);

CREATE MATERIALIZED VIEW sensors.heat_index_daily_mv TO sensors.heat_index_daily
AS
SELECT sensor_names,
       group_name,
       toDate(timestamp)    AS date,
       avg(heat_index)      AS heat_index,
       avg(avg_temperature) AS avg_temperature,
       avg(avg_humidity)    AS avg_humidity
FROM sensors.heat_index
GROUP BY sensor_names, group_name, date;


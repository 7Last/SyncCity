CREATE TABLE sensors.recycling_points
(
    sensor_uuid   UUID,
    sensor_name   String,
    timestamp     DateTime64,
    latitude      Float64,
    longitude     Float64,
    filling Float32
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);


select timestamp, filling
from sensors.recycling_points
where sensor_name = 'campus-ca-foscari'
order by timestamp;

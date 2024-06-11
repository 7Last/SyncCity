create table sensors
(
    sensor_name         String,
    type                String,
    last_message        DateTime64,
    latitude            Float64,
    longitude           Float64,
    insertion_timestamp DateTime64(6) default now64()
) engine = MergeTree()
      order by insertion_timestamp;

create materialized view air_quality_sensor_mv to sensors
as
select sensor_name,
       'air_quality' as type,
       timestamp           as last_message,
       latitude,
       longitude
from sensors.air_quality;

create materialized view parking_sensor_mv to sensors
as
select sensor_name,
       'parking' as type,
       timestamp as last_message,
       latitude,
       longitude
from sensors.parking;

create materialized view recycling_points_sensor_mv to sensors
as
select sensor_name,
       'recycling_points' as type,
       timestamp           as last_message,
       latitude,
       longitude
from sensors.recycling_points;

create materialized view temperatures_sensor_mv to sensors
as
select sensor_name,
       'temperature' as type,
       timestamp     as last_message,
       latitude,
       longitude
from sensors.temperatures;

create materialized view traffic_sensor_mv to sensors
as
select sensor_name,
       'traffic' as type,
       timestamp as last_message,
       latitude,
       longitude
from sensors.traffic;

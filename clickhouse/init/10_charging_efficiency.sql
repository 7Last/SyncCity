CREATE TABLE sensors.charging_efficiency
(
    sensor_uuid           UUID,
    sensor_name           String,
    group_name            Nullable(String) default null,
    timestamp             DateTime64,
    vehicle_type          Nullable(String) default null,
    battery_level         Nullable(Float32) default null,
    kwh_supplied          Float32,
    remaining_charge_time Nullable(int) default null,
    elapsed_time          Nullable(int) default null,
    latitude              Float64,
    longitude             Float64
) ENGINE = MergeTree()
      ORDER BY (sensor_uuid, timestamp);
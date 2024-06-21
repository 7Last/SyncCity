# Adding new sensor types to the simulator
This documents provides a step-by-step guide on how to add new sensor types to the simulator.

> Suppose that the new sensor type is named `NewSensorType`. This name
> will be used throughout the document to refer to it. Replace it with the actual name.

## Step 1: Create a `RawData` class
The `RawData` class is used to represent a generic raw message sent by the sensor.
Each sensor type **must** provide its own concrete `RawData` class implementation,
which inherits from the `RawData`.

Therefore, define a new class named `NewSensorTypeRawData` in the 
[src/models/raw_data](../src/models/raw_data) folder. It should contain the
fields for the measurements that the sensor provides (e.g. if the sensor
measures temperature, the class should contain `value` in Celsius degree).

For the moment, just implement the `topic()` method. It should return a simple and
short name for the Kafka topic in which `NewSensorType` data will be published.
From now on, the string which is returned from the `topic()` method will be called
`<new_sensor_type>`. Replace `<new_sensor_type>` everywhere with the actual string.

More info about the `accept` method will be provided later.

## Step 2: Add a value to the `SensorType` enum
Add the new type to the `SensorType` enum in the [src/models/sensor_type.py](../src/models/sensor_type.py)
file.

## Step 3: Write the Avro schema definition for the new sensor type
Create a new file in [src/schemas](../../redpanda/schemas). The file should be named as follows:
`<new_sensor_type>-value.avsc`, where `<new_sensor_type>` must be replaced with the sensor type
which is being created.

Keep `sensor_uuid`, `sensor_name`, `timestamp`, `latitude` and `longitude` fields exactly the same as in
the `.avsc` files which are already defined.

**NOTE**:

> It is mandatory to keep `-value` in the filename

> `<new_sensor_type>` **must be the exactly same string** which is returned from the 
> `topic()` method of the `NewSensorTypeRawData` class, otherwise data will not be
> stored in ClickHouse

## Step 4: Implement the method in the `SerializerVisitor` class
In the file [src/serializers/serializer_visitor.py](../src/serializers/visitor/json_converter_visitor.py)
implement a new public method to serialize the new sensor type.

> The method should be called `serialize_<new_sensor_type>`.

> The method should make use of `**(SerializerVisitor._serialize_raw_data(raw_data))`
to serialize fields which are common to all the `RawData` classes.

## Step 5: Implement the `accept` method in `NewSensorTypeRawData`
The `accept` method has to call the `serialize_<new_sensor_type>` method just implemented
in the `SerializerVisitor` as follows:

```python
def accept(self, visitor) -> Dict[str, any]:  # noqa: ANN001
    return visitor.serialize_<new_sensor_type>(self)
```

## Step 6: Implement the `Simulator` for the new sensor type
In the [src/simulators](../src/simulators) folder implement a new `Simulator`.
The `NewSensorTypeSimulator` class must extend `Simulator` and implement the `stream()`
method.

Copy the `stream()` function from either the `TemperatureSimulator` or `TrafficSimulator`
and change the `yield` statement to return a new instance of `NewSensorTypeRawData`.

If any support method is needed to generate the realistic values for the simulated
measurement, create a **private** function on the bottom of the file.

## Step 7: Edit ClickHouse connector config
In the [connectors/configs/clickhouse.json](../../redpanda/connectors/configs/clickhouse.json)
file add `<new_sensor_type>` to the list of `topics` in `config` and in the `topics2TableMap`.

## Step 8: Create ClickHouse Table
Create the table for the new topic in the [clickhouse/init](../../clickhouse/init) 
folder. The file should be called `<new_sensor_type>.sql`.
The table should be called `<new_sensor_type>`.
In this file define also the materialized views for `<new_sensor_type>`.

## Step 9: Add the new sensor type to the simulator factory
In the [src/models/config/simulator_factory.py](../src/models/config/simulator_factory.py) file,
add a new `match` case for the new sensor type in the `_simulator_factory` method.

## Step 10: Create sensors in the configuration
In the [sensors.toml](../sensors.toml) file, create sensors of the new type.
You can create as many sensors as you wish, each of them is totally independent
and will be run in a separate thread.

> More sensors of the same type can obviously exist at the same time.

To add a new sensor, add a new line with `[sensors.<name>]` at the bottom. Replace
`<name>` with any name you like.

Below this line, add the other params. Possible params are:
- `uuid` (generate a new unique uuid and add it)
- `type`: should match `<new_sensor_type>`
- `points_spacing`: how spaced in time are the points. Express it in the ISO8601 standard
- `generation_delay` (optional): how often a new data is generated. Express it in the ISO8601 standard.
Default: 1s.
- `limit`: How many raw data messages to generate before stopping. Default: infinite
- `begin_date` (optional): date from which timestamps of raw data start. Default: now
- `latitude` and `longitude`
- 
## Step 11: Define Grafana dashboards for the new sensor type


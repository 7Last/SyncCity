package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.apache.avro.generic.GenericRecord;

import javax.annotation.Nullable;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Supplier;

@Data
@AllArgsConstructor
public class ChargingStationRawData extends RawData {
    private final UUID sensorUuid;
    private final String sensorName;
    private final String groupName;
    private final double latitude;
    private final double longitude;
    private final ZonedDateTime timestamp;
    private final String vehicleType;
    private final double batteryLevel;
    private final double kwhSupplied;
    private final Duration remainingChargeTime;
    private final Duration elapsedTime;

    public static ChargingStationRawData fromGenericRecord(GenericRecord record) {
        return new ChargingStationRawData(
                UUID.fromString(record.get("sensor_uuid").toString()),
                record.get("sensor_name").toString(),
                Optional.ofNullable(record.get("group_name")).map(Object::toString).orElse(null),
                (double) record.get("latitude"),
                (double) record.get("longitude"),
                ZonedDateTime.parse(record.get("timestamp").toString()),
                record.get("vehicle_type").toString(),
                (double) record.get("battery_level"),
                (double) record.get("kwh_supplied"),
                Optional.ofNullable(record.get("remaining_charge_time"))
                        .map((obj) -> Duration.ofSeconds((long) obj))
                        .orElse(null),
                Optional.ofNullable(record.get("elapsed_time"))
                        .map((obj) -> Duration.ofSeconds((long) obj))
                        .orElse(null)
        );
    }

    @Override
    public Boolean get() {
        return batteryLevel > 0;
    }
}

package com.sevenlast.synccity.models;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.apache.avro.generic.GenericRecord;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.Optional;
import java.util.UUID;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChargingStationRawData extends RawData {
    private UUID sensorUuid;
    private String sensorName;
    private String groupName;
    private double latitude;
    private double longitude;
    private ZonedDateTime timestamp;
    private String vehicleType;
    private double batteryLevel;
    private double kwhSupplied;
    private Duration remainingChargeTime;
    private Duration elapsedTime;

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
        return kwhSupplied <= 0; // kwhSupplied should always be >= 0 (check for safety)
    }
}

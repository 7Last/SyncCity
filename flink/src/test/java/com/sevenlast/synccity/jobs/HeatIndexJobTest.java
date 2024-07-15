package com.sevenlast.synccity.jobs;

import com.sevenlast.synccity.HeatIndexJob;
import com.sevenlast.synccity.models.HumTempRawData;
import com.sevenlast.synccity.models.results.HeatIndexResult;
import com.sevenlast.synccity.serialization.HeatIndexRecordSerializableAdapter;
import com.sevenlast.synccity.serialization.RecordSerializable;
import com.sevenlast.synccity.utils.CollectionSink;
import com.sevenlast.synccity.utils.SimpleGenericRecord;
import org.apache.avro.generic.GenericRecord;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Set;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

public class HeatIndexJobTest {

    private final WatermarkStrategy<GenericRecord> watermark = WatermarkStrategy.<GenericRecord>forBoundedOutOfOrderness(Duration.ofSeconds(10))
            .withTimestampAssigner((event, timestamp) -> {
                var eventTimestamp = event.get("timestamp").toString();
                return LocalDateTime.parse(eventTimestamp).atZone(ZoneId.of("UTC")).toInstant().toEpochMilli();


            });

    @BeforeEach
    public void before() {
        CollectionSink.values.clear();
    }

    @Test
    public void testSingleSensor() throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        var temperatureUuid = "00000000-0000-0000-0000-000000000000";
        var temperatureName = "Temperature";
        var groupName = "Group";
        var beginDate = LocalDateTime.parse("2021-01-01T00:00:00");

        var temperatureData = Stream.of(
                new HumTempRawData(temperatureUuid, temperatureName, groupName, 0.0, 0.0, beginDate, 25.0f),
                new HumTempRawData(temperatureUuid, temperatureName, groupName, 0.0, 0.0, beginDate.plusMinutes(5), 30.0f),
                new HumTempRawData(temperatureUuid, temperatureName, groupName, 0.0, 0.0, beginDate.plusMinutes(10), 27.5f)
        ).map(this::toRecord).toList();

        var humidityUuid = "00000000-0000-0000-0000-000000000001";
        var humidityName = "Humidity";
        var humidityData = Stream.of(
                new HumTempRawData(humidityUuid, humidityName, groupName, 0.0, 0.0, beginDate, 50.0f),
                new HumTempRawData(humidityUuid, humidityName, groupName, 0.0, 0.0, beginDate.plusMinutes(5), 60.0f),
                new HumTempRawData(humidityUuid, humidityName, groupName, 0.0, 0.0, beginDate.plusMinutes(10), 55.0f)
        ).map(this::toRecord).toList();

        var mockSink = new CollectionSink<RecordSerializable>();

        var job = new HeatIndexJob(
                env.fromCollection(temperatureData),
                env.fromCollection(humidityData),
                mockSink,
                watermark
        );

        job.execute(env);

        var expected = new HeatIndexResult(
                Set.of(temperatureName, humidityName),
                groupName,
                28.30425060554499,
                27.5,
                55.0,
                0.0,
                0.0,
                0.0,
                beginDate
        );

        assertEquals(1, CollectionSink.values.size());
        var actual = ((HeatIndexRecordSerializableAdapter) CollectionSink.values.get(0)).getAdaptee();
        assertEquals(expected, actual);
    }

    @Test
    public void testMultipleSensors() throws Exception {
        var env = StreamExecutionEnvironment.getExecutionEnvironment();
        var temperature1Uuid = "00000000-0000-0000-0000-000000000000";
        var temperature2Uuid = "00000000-0000-0000-0000-000000000001";
        var groupName = "Group";
        var beginDate = LocalDateTime.parse("2021-01-01T00:00:00");

        var temperatureData = Stream.of(
                new HumTempRawData(temperature1Uuid, "temperature-1", groupName, 12.0, 45.0, beginDate, 25.0f),
                new HumTempRawData(temperature1Uuid, "temperature-1", groupName, 12.0, 45.0, beginDate.plusMinutes(5), 30.0f),
                new HumTempRawData(temperature1Uuid, "temperature-1", groupName, 12.0, 45.0, beginDate.plusMinutes(10), 27.5f),

                new HumTempRawData(temperature2Uuid, "temperature-2", groupName, 12.5, 45.5, beginDate, 24.0f),
                new HumTempRawData(temperature2Uuid, "temperature-2", groupName, 12.5, 45.5, beginDate.plusMinutes(5), 26.0f),
                new HumTempRawData(temperature2Uuid, "temperature-2", groupName, 12.5, 45.5, beginDate.plusMinutes(10), 27.5f)
        ).map(this::toRecord).toList();

        var humidity1Uuid = "00000000-0000-0000-0000-000000000002";
        var humidity2Uuid = "00000000-0000-0000-0000-000000000003";

        var humidityData = Stream.of(
                new HumTempRawData(humidity1Uuid, "humidity-1", groupName, 12.25, 45.20, beginDate, 77.0f),
                new HumTempRawData(humidity1Uuid, "humidity-1", groupName, 12.25, 45.20, beginDate.plusMinutes(5), 79.0f),
                new HumTempRawData(humidity1Uuid, "humidity-1", groupName, 12.25, 45.20, beginDate.plusMinutes(10), 78.0f),

                new HumTempRawData(humidity2Uuid, "humidity-2", groupName, 12.15, 45.1, beginDate, 80.0f),
                new HumTempRawData(humidity2Uuid, "humidity-2", groupName, 12.15, 45.1, beginDate.plusMinutes(5), 82.0f),
                new HumTempRawData(humidity2Uuid, "humidity-2", groupName, 12.15, 45.1, beginDate.plusMinutes(10), 81.0f)
        ).map(this::toRecord).toList();

        var mockSink = new CollectionSink<RecordSerializable>();

        var job = new HeatIndexJob(
                env.fromCollection(temperatureData),
                env.fromCollection(humidityData),
                mockSink,
                watermark
        );

        job.execute(env);

        var expected = new HeatIndexResult(
                Set.of(
                        "temperature-1",
                        "humidity-1",
                        "humidity-2",
                        "temperature-2"
                ),
                groupName,
                28.97965137355458,
                26.666666666666668,
                79.5,
                12.225063069171808,
                45.19987168826055,
                44.69126354786348,
                beginDate
        );

        assertEquals(1, CollectionSink.values.size());
        var actual = ((HeatIndexRecordSerializableAdapter) CollectionSink.values.get(0)).getAdaptee();

        assertEquals(expected.getGroupName(), actual.getGroupName());
        assertTrue(
            expected.getSensorNames().containsAll(actual.getSensorNames()) &&
            actual.getSensorNames().containsAll(expected.getSensorNames())
        );
        assertEquals(expected.getHeatIndex(), actual.getHeatIndex());
        assertEquals(expected.getAverageTemperature(), actual.getAverageTemperature());
        assertEquals(expected.getAverageHumidity(), actual.getAverageHumidity());
        assertEquals(expected.getCenterOfMassLatitude(), actual.getCenterOfMassLatitude());
        assertEquals(expected.getCenterOfMassLongitude(), actual.getCenterOfMassLongitude());
        assertEquals(expected.getGroupName(), actual.getGroupName());
        assertEquals(expected.getRadius(), actual.getRadius());
        assertEquals(expected.getWindowStart(), actual.getWindowStart());
    }

    private GenericRecord toRecord(HumTempRawData data) {
        var simpleRecord = new SimpleGenericRecord();
        simpleRecord.put("sensor_uuid", data.getSensorUuid());
        simpleRecord.put("sensor_name", data.getSensorName());
        simpleRecord.put("group_name", data.getGroupName());
        simpleRecord.put("latitude", data.getLatitude());
        simpleRecord.put("longitude", data.getLongitude());
        simpleRecord.put("timestamp", data.getTimestamp().format(DateTimeFormatter.ISO_LOCAL_DATE_TIME));
        simpleRecord.put("value", data.getValue());
        return simpleRecord;
    }
}

package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.HumTempRawData;
import com.sevenlast.synccity.models.results.AverageResult;
import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.util.Collector;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.List;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ChargingEfficiencyJoinFunctionTest {
    @Test
    public void testJoinZeroTotalSeconds() {
        var uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");
        var parkingDiff = new TimestampDifferenceResult(Duration.ZERO, Duration.ZERO, uuid);
        var chargingDiff = new TimestampDifferenceResult( Duration.ZERO, Duration.ZERO, uuid );

        var function = new ChargingEfficiencyJoinFunction();

        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, ChargingEfficiencyResult.zero(uuid));
    }

    @Test
    public void testJoinChargingOccupiedGreaterThanParkingOccupied() {
        var uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");

        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(10), // occupied for
                Duration.ofSeconds(10), // free for
                uuid
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(20), // used for
                Duration.ofSeconds(10), // free for
                uuid
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, new ChargingEfficiencyResult(1, 1, uuid));
    }

    @Test
    public void testEfficiencyRateGreaterThanUtilizationRate() {
        var uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");
        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofHours(3).plusMinutes(10), // occupied for
                Duration.ofHours(1).plusMinutes(10), // free for
                uuid
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofHours(1), // used for
                Duration.ofHours(1).plusMinutes(20), // free for
                uuid
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, new ChargingEfficiencyResult(0.23076923076923078, 0.3157894736842105, uuid));
    }

    @Test
    public void testEfficiencyRateLessThanUtilizationRate() {
        var uuid = UUID.fromString("00000000-0000-0000-0000-000000000000");
        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(10), // occupied for
                Duration.ofSeconds(10), // free for
                uuid
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(5), // used for
                Duration.ofSeconds(10), // free for
                uuid
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, new ChargingEfficiencyResult(0.25, 0.5, uuid));
    }
}

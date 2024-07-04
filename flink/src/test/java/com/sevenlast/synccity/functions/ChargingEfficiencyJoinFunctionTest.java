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
        var parkingDiff = new TimestampDifferenceResult(
                Duration.ZERO,
                Duration.ZERO,
                UUID.fromString("00000000-0000-0000-0000-000000000000")
        );
        var chargingDiff = new TimestampDifferenceResult(
                Duration.ZERO,
                Duration.ZERO,
                UUID.fromString("00000000-0000-0000-0000-000000000000")
        );

        var function = new ChargingEfficiencyJoinFunction();

        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, ChargingEfficiencyResult.zero());
    }

    @Test
    public void testJoinChargingOccupiedGreaterThanParkingOccupied() {
        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(10), // occupied for
                Duration.ofSeconds(10), // free for
                UUID.fromString("00000000-0000-0000-0000-000000000000")
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(20), // used for
                Duration.ofSeconds(10), // free for
                UUID.fromString("00000000-0000-0000-0000-000000000000")
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, new ChargingEfficiencyResult(1, 1));
    }

    @Test
    public void testEfficiencyRateGreaterThanUtilizationRate() {
        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(10), // occupied for
                Duration.ofSeconds(10), // free for
                UUID.fromString("00000000-0000-0000-0000-000000000000")
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(10), // used for
                Duration.ofSeconds(5), // free for
                UUID.fromString("00000000-0000-0000-0000-000000000000")
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, new ChargingEfficiencyResult(0.5, 1));
    }

    @Test
    public void testEfficiencyRateLessThanUtilizationRate() {
        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(10), // occupied for
                Duration.ofSeconds(10), // free for
                UUID.fromString("00000000-0000-0000-0000-000000000000")
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(5), // used for
                Duration.ofSeconds(10), // free for
                UUID.fromString("00000000-0000-0000-0000-000000000000")
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, new ChargingEfficiencyResult(0.25, 0.5));
    }
}

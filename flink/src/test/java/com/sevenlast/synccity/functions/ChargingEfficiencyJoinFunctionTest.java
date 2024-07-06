package com.sevenlast.synccity.functions;

import com.sevenlast.synccity.models.results.ChargingEfficiencyResult;
import com.sevenlast.synccity.models.results.TimestampDifferenceResult;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;

public class ChargingEfficiencyJoinFunctionTest {
    @Test
    public void testJoinZeroTotalSeconds() {
        var uuid = "00000000-0000-0000-0000-000000000000";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");
        var parkingDiff = new TimestampDifferenceResult(Duration.ZERO, Duration.ZERO, uuid, timestamp);
        var chargingDiff = new TimestampDifferenceResult(Duration.ZERO, Duration.ZERO, uuid, timestamp);

        var function = new ChargingEfficiencyJoinFunction();

        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, ChargingEfficiencyResult.zero(uuid, timestamp));
    }

    @Test
    public void testJoinChargingOccupiedGreaterThanParkingOccupied() {
        var uuid = "00000000-0000-0000-0000-000000000000";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(10), // occupied for
                Duration.ofSeconds(10), // free for
                uuid,
                timestamp
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(20), // used for
                Duration.ofSeconds(10), // free for
                uuid,
                timestamp
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, new ChargingEfficiencyResult(1, 1, uuid, timestamp));
    }

    @Test
    public void testEfficiencyRateGreaterThanUtilizationRate() {
        var uuid = "00000000-0000-0000-0000-000000000000";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofHours(3).plusMinutes(10), // occupied for
                Duration.ofHours(1).plusMinutes(10), // free for
                uuid,
                timestamp
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofHours(1), // used for
                Duration.ofHours(1).plusMinutes(20), // free for
                uuid,
                timestamp
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        var expected = new ChargingEfficiencyResult(0.23076923076923078, 0.3157894736842105, uuid, timestamp);
        assertEquals(expected, result);
    }

    @Test
    public void testEfficiencyRateLessThanUtilizationRate() {
        var uuid = "00000000-0000-0000-0000-000000000000";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(10), // occupied for
                Duration.ofSeconds(10), // free for
                uuid,
                timestamp
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(5), // used for
                Duration.ofSeconds(10), // free for
                uuid,
                timestamp
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, new ChargingEfficiencyResult(0.25, 0.5, uuid, timestamp));
    }

    @Test
    public void testParkingNeverOccupied() {
        var uuid = "00000000-0000-0000-0000-000000000000";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var parkingDiff = new TimestampDifferenceResult(
                Duration.ZERO, // occupied for
                Duration.ofSeconds(15), // free for
                uuid,
                timestamp
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(5), // used for
                Duration.ofSeconds(10), // free for
                uuid,
                timestamp
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, ChargingEfficiencyResult.zero(uuid, timestamp));
    }

    @Test
    public void testChargingStationNeverOccupied() {
        var uuid = "00000000-0000-0000-0000-000000000000";
        var timestamp = LocalDateTime.parse("2021-01-01T00:00:00");

        var parkingDiff = new TimestampDifferenceResult(
                Duration.ofSeconds(5), // used for
                Duration.ofSeconds(10), // free for
                uuid,
                timestamp
        );

        var chargingDiff = new TimestampDifferenceResult(
                Duration.ZERO, // occupied for
                Duration.ofSeconds(15), // free for
                uuid,
                timestamp
        );

        var function = new ChargingEfficiencyJoinFunction();
        var result = function.join(parkingDiff, chargingDiff);
        assertEquals(result, ChargingEfficiencyResult.zero(uuid, timestamp));
    }
}

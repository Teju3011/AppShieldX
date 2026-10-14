package com.framework.threat.service;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

@DisplayName("RiskEvaluationEngine Unit Tests")
class RiskEvaluationEngineTest {

    private RiskEvaluationEngine engine;

    @BeforeEach
    void setUp() {
        engine = new RiskEvaluationEngine(40, 50, 30, 35, 15, 20, 10);
    }

    @Test
    @DisplayName("Should evaluate clean device with score 0 and LOW risk")
    void testCleanDevice() {
        RiskEvaluationEngine.EvaluationResult result = engine.evaluateRisk(Set.of(), 1);

        assertEquals(0, result.score());
        assertEquals("LOW", result.riskLevel());
        assertTrue(result.threatFlags().isEmpty());
    }

    @Test
    @DisplayName("Should score ROOT_DETECTED as 40 and MEDIUM risk")
    void testRootDetection() {
        RiskEvaluationEngine.EvaluationResult result = engine.evaluateRisk(Set.of("ROOT_DETECTED"), 2);

        assertEquals(40, result.score());
        assertEquals("MEDIUM", result.riskLevel());
        assertTrue(result.threatFlags().contains("ROOT_OR_JAILBREAK"));
    }

    @Test
    @DisplayName("Should score FRIDA_DETECTED as 50 and MEDIUM risk")
    void testFridaDetection() {
        RiskEvaluationEngine.EvaluationResult result = engine.evaluateRisk(Set.of("FRIDA_HOOK_INJECTION"), 1);

        assertEquals(50, result.score());
        assertEquals("MEDIUM", result.riskLevel());
        assertTrue(result.threatFlags().contains("FRIDA_HOOK_INJECTION"));
    }

    @Test
    @DisplayName("Should accumulate ROOT + FRIDA = 90 as CRITICAL risk")
    void testCompoundCriticalThreat() {
        RiskEvaluationEngine.EvaluationResult result = engine.evaluateRisk(
                Set.of("ROOT_DETECTED", "FRIDA_DETECTED"),
                3
        );

        assertEquals(90, result.score());
        assertEquals("CRITICAL", result.riskLevel());
        assertEquals(2, result.threatFlags().size());
    }

    @Test
    @DisplayName("Should add velocity burst penalty when frequency exceeds threshold")
    void testVelocityBurstPenalty() {
        // Root (40) + burst (>10 events/min => +20) = 60
        RiskEvaluationEngine.EvaluationResult result = engine.evaluateRisk(
                Set.of("ROOT_DETECTED"),
                15
        );

        assertEquals(60, result.score());
        assertTrue(result.threatFlags().contains("ANOMALOUS_EVENT_BURST"));
    }

    @Test
    @DisplayName("Should clamp risk score at maximum 100")
    void testScoreClamping() {
        // Root (40) + Frida (50) + Debugger (30) + Velocity (20) = 140 => clamped to 100
        RiskEvaluationEngine.EvaluationResult result = engine.evaluateRisk(
                Set.of("ROOT_DETECTED", "FRIDA_DETECTED", "DEBUGGER_ATTACHED"),
                25
        );

        assertEquals(100, result.score());
        assertEquals("CRITICAL", result.riskLevel());
    }
}

package com.framework.threat.entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "device_risk_profiles")
public class DeviceRiskProfile {

    @Id
    @Column(name = "device_id", nullable = false, length = 100)
    private String deviceId;

    @Column(name = "risk_score", nullable = false)
    private int riskScore; // 0 - 100

    @Column(name = "risk_level", nullable = false, length = 20)
    private String riskLevel; // LOW, MEDIUM, HIGH, CRITICAL

    @Column(name = "active_threats", length = 255)
    private String activeThreats; // e.g. "ROOT_DETECTED,FRIDA_DETECTED"

    @Column(name = "total_events_recorded", nullable = false)
    private long totalEventsRecorded = 0;

    @Column(name = "last_evaluated_at", nullable = false)
    private Instant lastEvaluatedAt = Instant.now();

    public DeviceRiskProfile() {}

    public DeviceRiskProfile(String deviceId, int riskScore, String riskLevel, String activeThreats) {
        this.deviceId = deviceId;
        this.riskScore = Math.min(100, Math.max(0, riskScore));
        this.riskLevel = riskLevel;
        this.activeThreats = activeThreats;
        this.totalEventsRecorded = 1;
        this.lastEvaluatedAt = Instant.now();
    }

    public String getDeviceId() {
        return deviceId;
    }

    public void setDeviceId(String deviceId) {
        this.deviceId = deviceId;
    }

    public int getRiskScore() {
        return riskScore;
    }

    public void setRiskScore(int riskScore) {
        this.riskScore = Math.min(100, Math.max(0, riskScore));
    }

    public String getRiskLevel() {
        return riskLevel;
    }

    public void setRiskLevel(String riskLevel) {
        this.riskLevel = riskLevel;
    }

    public String getActiveThreats() {
        return activeThreats;
    }

    public void setActiveThreats(String activeThreats) {
        this.activeThreats = activeThreats;
    }

    public long getTotalEventsRecorded() {
        return totalEventsRecorded;
    }

    public void setTotalEventsRecorded(long totalEventsRecorded) {
        this.totalEventsRecorded = totalEventsRecorded;
    }

    public Instant getLastEvaluatedAt() {
        return lastEvaluatedAt;
    }

    public void setLastEvaluatedAt(Instant lastEvaluatedAt) {
        this.lastEvaluatedAt = lastEvaluatedAt;
    }
}

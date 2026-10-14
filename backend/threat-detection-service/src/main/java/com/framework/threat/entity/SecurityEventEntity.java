package com.framework.threat.entity;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "security_events")
public class SecurityEventEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "event_id", length = 100)
    private String eventId;

    @Column(name = "device_id", nullable = false, length = 100)
    private String deviceId;

    @Column(name = "user_id")
    private UUID userId;

    @Column(name = "event_type", nullable = false, length = 60)
    private String eventType;

    @Column(nullable = false, length = 20)
    private String severity; // INFO, LOW, MEDIUM, HIGH, CRITICAL

    @Column(name = "threat_category", nullable = false, length = 60)
    private String threatCategory;

    @Column(columnDefinition = "TEXT")
    private String details;

    @Column(name = "client_ip", length = 45)
    private String clientIp;

    @Column(nullable = false)
    private Instant timestamp = Instant.now();

    // Extended Common Security Event Schema Fields
    @Column(name = "event_timestamp")
    private Instant eventTimestamp;

    @Column(name = "received_timestamp")
    private Instant receivedTimestamp;

    @Column(name = "platform", length = 30)
    private String platform = "UNKNOWN"; // ANDROID, IOS, API_GATEWAY, AUTH_SERVICE, BUSINESS_API

    @Column(name = "app_version", length = 20)
    private String appVersion = "1.0.0";

    @Column(name = "confidence")
    private Double confidence = 1.0;

    @Column(name = "auth_user_ref", length = 100)
    private String authUserRef;

    @Column(name = "verified_session_ref", length = 100)
    private String verifiedSessionRef;

    @Column(name = "registered_device_ref", length = 100)
    private String registeredDeviceRef;

    @Column(name = "correlation_id", length = 100)
    private String correlationId;

    @Column(name = "endpoint_category", length = 60)
    private String endpointCategory = "MOBILE_RASP";

    @Column(name = "detection_reason", length = 255)
    private String detectionReason;

    @Column(name = "evidence_source", length = 60)
    private String evidenceSource = "CLIENT_TELEMETRY";

    @Column(name = "verification_status", length = 40)
    private String verificationStatus = "UNVERIFIED_CLIENT"; // UNVERIFIED_CLIENT, SERVER_VERIFIED, REJECTED, SUSPICIOUS

    @Column(name = "event_expiry")
    private Instant eventExpiry;

    @Column(name = "event_hash", length = 64)
    private String eventHash;

    public SecurityEventEntity() {}

    public SecurityEventEntity(
            String deviceId,
            UUID userId,
            String eventType,
            String severity,
            String threatCategory,
            String details,
            String clientIp,
            Instant timestamp
    ) {
        this.deviceId = deviceId;
        this.userId = userId;
        this.eventType = eventType;
        this.severity = severity;
        this.threatCategory = threatCategory;
        this.details = details;
        this.clientIp = clientIp;
        this.timestamp = timestamp != null ? timestamp : Instant.now();
        this.eventId = UUID.randomUUID().toString();
        this.eventTimestamp = this.timestamp;
        this.receivedTimestamp = Instant.now();
        this.registeredDeviceRef = deviceId;
        this.authUserRef = userId != null ? userId.toString() : null;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getEventId() {
        return eventId != null ? eventId : (id != null ? id.toString() : null);
    }

    public void setEventId(String eventId) {
        this.eventId = eventId;
    }

    public String getDeviceId() {
        return deviceId;
    }

    public void setDeviceId(String deviceId) {
        this.deviceId = deviceId;
    }

    public UUID getUserId() {
        return userId;
    }

    public void setUserId(UUID userId) {
        this.userId = userId;
    }

    public String getEventType() {
        return eventType;
    }

    public void setEventType(String eventType) {
        this.eventType = eventType;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }

    public String getThreatCategory() {
        return threatCategory;
    }

    public void setThreatCategory(String threatCategory) {
        this.threatCategory = threatCategory;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    public String getClientIp() {
        return clientIp;
    }

    public void setClientIp(String clientIp) {
        this.clientIp = clientIp;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }

    public Instant getEventTimestamp() {
        return eventTimestamp != null ? eventTimestamp : timestamp;
    }

    public void setEventTimestamp(Instant eventTimestamp) {
        this.eventTimestamp = eventTimestamp;
    }

    public Instant getReceivedTimestamp() {
        return receivedTimestamp != null ? receivedTimestamp : timestamp;
    }

    public void setReceivedTimestamp(Instant receivedTimestamp) {
        this.receivedTimestamp = receivedTimestamp;
    }

    public String getPlatform() {
        return platform;
    }

    public void setPlatform(String platform) {
        this.platform = platform;
    }

    public String getAppVersion() {
        return appVersion;
    }

    public void setAppVersion(String appVersion) {
        this.appVersion = appVersion;
    }

    public Double getConfidence() {
        return confidence;
    }

    public void setConfidence(Double confidence) {
        this.confidence = confidence;
    }

    public String getAuthUserRef() {
        return authUserRef;
    }

    public void setAuthUserRef(String authUserRef) {
        this.authUserRef = authUserRef;
    }

    public String getVerifiedSessionRef() {
        return verifiedSessionRef;
    }

    public void setVerifiedSessionRef(String verifiedSessionRef) {
        this.verifiedSessionRef = verifiedSessionRef;
    }

    public String getRegisteredDeviceRef() {
        return registeredDeviceRef;
    }

    public void setRegisteredDeviceRef(String registeredDeviceRef) {
        this.registeredDeviceRef = registeredDeviceRef;
    }

    public String getCorrelationId() {
        return correlationId;
    }

    public void setCorrelationId(String correlationId) {
        this.correlationId = correlationId;
    }

    public String getEndpointCategory() {
        return endpointCategory;
    }

    public void setEndpointCategory(String endpointCategory) {
        this.endpointCategory = endpointCategory;
    }

    public String getDetectionReason() {
        return detectionReason;
    }

    public void setDetectionReason(String detectionReason) {
        this.detectionReason = detectionReason;
    }

    public String getEvidenceSource() {
        return evidenceSource;
    }

    public void setEvidenceSource(String evidenceSource) {
        this.evidenceSource = evidenceSource;
    }

    public String getVerificationStatus() {
        return verificationStatus;
    }

    public void setVerificationStatus(String verificationStatus) {
        this.verificationStatus = verificationStatus;
    }

    public Instant getEventExpiry() {
        return eventExpiry;
    }

    public void setEventExpiry(Instant eventExpiry) {
        this.eventExpiry = eventExpiry;
    }

    public String getEventHash() {
        return eventHash;
    }

    public void setEventHash(String eventHash) {
        this.eventHash = eventHash;
    }
}

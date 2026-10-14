package com.framework.threat.service;

import com.framework.threat.dto.CommonSecurityEventRequest;
import com.framework.threat.entity.SecurityEventEntity;
import org.springframework.stereotype.Service;

import java.time.Duration;
import java.time.Instant;
import java.util.UUID;

@Service
public class EventEnrichmentService {

    private static final Duration DEFAULT_EVENT_EXPIRY = Duration.ofMinutes(15);

    public SecurityEventEntity enrich(
            CommonSecurityEventRequest request,
            UUID authenticatedUserId,
            String clientIp,
            String eventHash
    ) {
        Instant now = Instant.now();
        Instant eventTime = request.eventTimestamp() != null ? request.eventTimestamp() : now;
        Instant expiryTime = request.eventExpiry() != null ? request.eventExpiry() : now.plus(DEFAULT_EVENT_EXPIRY);

        String correlationId = request.correlationId();
        if (correlationId == null || correlationId.isBlank()) {
            correlationId = UUID.randomUUID().toString();
        }

        String eventId = request.eventId();
        if (eventId == null || eventId.isBlank()) {
            eventId = UUID.randomUUID().toString();
        }

        String platform = request.platform() != null && !request.platform().isBlank()
                ? request.platform().trim().toUpperCase()
                : "ANDROID";

        // Determine verification status
        String verificationStatus;
        if (authenticatedUserId != null && request.verifiedSessionReference() != null && !request.verifiedSessionReference().isBlank()) {
            verificationStatus = "SERVER_VERIFIED";
        } else if ("API_GATEWAY".equals(platform) || "AUTH_SERVICE".equals(platform) || "BUSINESS_API".equals(platform)) {
            verificationStatus = "SERVER_VERIFIED";
        } else {
            verificationStatus = "UNVERIFIED_CLIENT";
        }

        String evidenceSource = request.evidenceSource() != null && !request.evidenceSource().isBlank()
                ? request.evidenceSource()
                : ("SERVER_VERIFIED".equals(verificationStatus) ? "GATEWAY_FILTER" : "CLIENT_TELEMETRY");

        SecurityEventEntity entity = new SecurityEventEntity();
        entity.setEventId(eventId);
        entity.setDeviceId(request.registeredDeviceReference().trim());
        entity.setUserId(authenticatedUserId);
        entity.setEventType(request.eventType().trim().toUpperCase());
        entity.setSeverity(request.severity() != null ? request.severity().trim().toUpperCase() : "MEDIUM");
        entity.setThreatCategory(request.endpointCategory() != null ? request.endpointCategory().trim().toUpperCase() : "MOBILE_SECURITY");
        entity.setDetails(request.details() != null ? request.details().trim() : "");
        entity.setClientIp(clientIp != null ? clientIp.trim() : "127.0.0.1");
        entity.setTimestamp(eventTime);
        entity.setEventTimestamp(eventTime);
        entity.setReceivedTimestamp(now);
        entity.setPlatform(platform);
        entity.setAppVersion(request.appVersion() != null ? request.appVersion().trim() : "1.0.0");
        entity.setConfidence(request.confidence() != null ? request.confidence() : 1.0);
        entity.setAuthUserRef(authenticatedUserId != null ? authenticatedUserId.toString() : request.authenticatedUserReference());
        entity.setVerifiedSessionRef(request.verifiedSessionReference());
        entity.setRegisteredDeviceRef(request.registeredDeviceReference().trim());
        entity.setCorrelationId(correlationId);
        entity.setEndpointCategory(request.endpointCategory() != null ? request.endpointCategory() : "MOBILE_RASP");
        entity.setDetectionReason(request.detectionReason() != null ? request.detectionReason() : request.eventType());
        entity.setEvidenceSource(evidenceSource);
        entity.setVerificationStatus(verificationStatus);
        entity.setEventExpiry(expiryTime);
        entity.setEventHash(eventHash);

        return entity;
    }
}

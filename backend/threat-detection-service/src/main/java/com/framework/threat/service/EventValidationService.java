package com.framework.threat.service;

import com.framework.threat.dto.CommonSecurityEventRequest;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.time.Duration;
import java.time.Instant;
import java.util.HexFormat;
import java.util.regex.Pattern;

@Service
public class EventValidationService {

    private static final Logger log = LoggerFactory.getLogger(EventValidationService.class);
    private static final Duration MAX_FUTURE_SKEW = Duration.ofSeconds(60);
    private static final Duration MAX_EVENT_AGE = Duration.ofHours(24);
    private static final Pattern SENSITIVE_TOKEN_PATTERN = Pattern.compile("(?i)(password|secret|bearer|eyj[a-z0-9_-]{10,}|refresh_token)");

    public record ValidationResult(boolean isValid, String rejectionReason, String eventHash) {}

    public ValidationResult validate(CommonSecurityEventRequest request) {
        if (request == null) {
            return new ValidationResult(false, "Event payload is null", null);
        }

        if (request.eventType() == null || request.eventType().isBlank()) {
            return new ValidationResult(false, "eventType is missing", null);
        }

        if (request.registeredDeviceReference() == null || request.registeredDeviceReference().isBlank()) {
            return new ValidationResult(false, "registeredDeviceReference is missing", null);
        }

        Instant now = Instant.now();
        Instant eventTime = request.eventTimestamp() != null ? request.eventTimestamp() : now;

        // Reject events with timestamps excessively in the future
        if (eventTime.isAfter(now.plus(MAX_FUTURE_SKEW))) {
            log.warn("VALIDATION_REJECT: Event timestamp is too far in future: {}", eventTime);
            return new ValidationResult(false, "Event timestamp is in the future beyond allowed clock skew", null);
        }

        // Reject excessively stale events
        if (eventTime.isBefore(now.minus(MAX_EVENT_AGE))) {
            log.warn("VALIDATION_REJECT: Event timestamp is too old: {}", eventTime);
            return new ValidationResult(false, "Event is too old (> 24 hours)", null);
        }

        // Check for sensitive credentials leaking into details or detectionReason
        if (containsSensitiveCredentials(request.details()) || containsSensitiveCredentials(request.detectionReason())) {
            log.warn("VALIDATION_REJECT: Sensitive credentials detected in event payload. Dropping.");
            return new ValidationResult(false, "Payload contains sensitive tokens or credentials", null);
        }

        // Compute deterministic SHA-256 hash for deduplication
        String hash = computeEventHash(request);

        return new ValidationResult(true, null, hash);
    }

    private boolean containsSensitiveCredentials(String text) {
        if (text == null || text.isBlank()) return false;
        return SENSITIVE_TOKEN_PATTERN.matcher(text).find();
    }

    public String computeEventHash(CommonSecurityEventRequest request) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            String raw = String.join(":",
                    request.registeredDeviceReference() != null ? request.registeredDeviceReference().trim() : "",
                    request.verifiedSessionReference() != null ? request.verifiedSessionReference().trim() : "",
                    request.eventType() != null ? request.eventType().trim().toUpperCase() : "",
                    request.detectionReason() != null ? request.detectionReason().trim() : ""
            );
            byte[] encoded = digest.digest(raw.getBytes(StandardCharsets.UTF_8));
            return HexFormat.of().formatHex(encoded);
        } catch (NoSuchAlgorithmException e) {
            throw new IllegalStateException("SHA-256 algorithm not available", e);
        }
    }
}

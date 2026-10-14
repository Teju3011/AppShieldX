package com.framework.threat.dto;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;
import java.time.Instant;

public record CommonSecurityEventRequest(
        String eventId,

        Instant eventTimestamp,

        String platform, // ANDROID, IOS, API_GATEWAY, AUTH_SERVICE, BUSINESS_API

        String appVersion,

        @NotBlank(message = "eventType is required")
        @Size(max = 60, message = "eventType cannot exceed 60 characters")
        String eventType,

        @NotBlank(message = "severity is required")
        @Size(max = 20, message = "severity cannot exceed 20 characters")
        String severity, // INFO, LOW, MEDIUM, HIGH, CRITICAL

        Double confidence,

        String authenticatedUserReference,

        String verifiedSessionReference,

        @NotBlank(message = "registeredDeviceReference is required")
        @Size(max = 100, message = "registeredDeviceReference cannot exceed 100 characters")
        String registeredDeviceReference,

        String correlationId,

        String endpointCategory, // MOBILE_RASP, AUTH_GATEWAY, BUSINESS_TX, ADMIN_API

        String detectionReason,

        String evidenceSource, // CLIENT_TELEMETRY, GATEWAY_FILTER, AUTH_SERVICE, AUTHORIZATION_INTERCEPTOR

        String verificationStatus, // UNVERIFIED_CLIENT, SERVER_VERIFIED, REJECTED, SUSPICIOUS

        Instant eventExpiry,

        String details
) {}

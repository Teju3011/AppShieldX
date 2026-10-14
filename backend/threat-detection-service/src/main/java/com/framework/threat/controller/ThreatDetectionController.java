package com.framework.threat.controller;

import com.framework.threat.dto.*;
import com.framework.threat.service.ThreatDetectionService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

@RestController
@RequestMapping("/api/security")
public class ThreatDetectionController {

    private final ThreatDetectionService threatService;

    public ThreatDetectionController(ThreatDetectionService threatService) {
        this.threatService = threatService;
    }

    @PostMapping("/events")
    public ResponseEntity<SecurityEventResponse> reportSecurityEvent(
            @Valid @RequestBody SecurityEventRequest request,
            Authentication authentication,
            HttpServletRequest servletRequest
    ) {
        UUID userId = extractUserId(authentication);
        String clientIp = servletRequest.getRemoteAddr();
        SecurityEventResponse response = threatService.ingestEvent(request, userId, clientIp);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @PostMapping("/events/common")
    public ResponseEntity<CorrelationResultResponse> reportCommonSecurityEvent(
            @Valid @RequestBody CommonSecurityEventRequest request,
            Authentication authentication,
            HttpServletRequest servletRequest
    ) {
        UUID userId = extractUserId(authentication);
        String clientIp = servletRequest.getRemoteAddr();
        CorrelationResultResponse response = threatService.ingestCommonEvent(request, userId, clientIp);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/devices/{deviceId}/risk")
    public ResponseEntity<DeviceRiskResponse> getDeviceRisk(@PathVariable String deviceId) {
        return ResponseEntity.ok(threatService.getDeviceRisk(deviceId));
    }

    @GetMapping("/threats/summary")
    public ResponseEntity<ThreatSummaryResponse> getThreatSummary() {
        return ResponseEntity.ok(threatService.getThreatSummary());
    }

    @GetMapping("/events")
    public ResponseEntity<List<SecurityEventResponse>> getRecentEvents(
            @RequestParam(defaultValue = "50") int limit
    ) {
        return ResponseEntity.ok(threatService.getRecentEvents(limit));
    }

    @GetMapping("/correlations")
    public ResponseEntity<List<CorrelationResultResponse>> getRecentCorrelations(
            @RequestParam(defaultValue = "50") int limit
    ) {
        return ResponseEntity.ok(threatService.getRecentCorrelations(limit));
    }

    @GetMapping("/correlations/{correlationId}")
    public ResponseEntity<CorrelationResultResponse> getCorrelationById(
            @PathVariable String correlationId
    ) {
        return ResponseEntity.ok(threatService.getCorrelationById(correlationId));
    }

    @GetMapping("/policies")
    public ResponseEntity<Map<String, String>> getPolicyConfigurations() {
        return ResponseEntity.ok(threatService.getPolicyConfigurations());
    }

    @PutMapping("/policies")
    public ResponseEntity<Map<String, String>> updatePolicyConfigurations(
            @RequestBody Map<String, String> configs,
            Authentication authentication
    ) {
        String actor = authentication != null ? authentication.getName() : "ADMIN";
        threatService.updatePolicyConfigurations(configs, actor);
        return ResponseEntity.ok(threatService.getPolicyConfigurations());
    }

    @GetMapping("/experiments/config")
    public ResponseEntity<ExperimentConfigDto> getActiveExperimentConfig() {
        return ResponseEntity.ok(threatService.getActiveExperimentConfig());
    }

    @PostMapping("/experiments/config")
    public ResponseEntity<ExperimentConfigDto> setActiveExperimentConfig(
            @RequestBody Map<String, String> body,
            Authentication authentication
    ) {
        String mode = body.get("mode");
        if (mode == null || mode.isBlank()) {
            return ResponseEntity.badRequest().build();
        }
        String actor = authentication != null ? authentication.getName() : "ADMIN";
        threatService.setActiveExperimentConfig(mode, actor);
        return ResponseEntity.ok(threatService.getActiveExperimentConfig());
    }

    @GetMapping("/experiments/metrics")
    public ResponseEntity<ResearchMetricsResponse> getExperimentMetrics() {
        return ResponseEntity.ok(threatService.getExperimentMetrics());
    }

    @PostMapping("/experiments/reset")
    public ResponseEntity<Map<String, String>> resetExperimentMetrics() {
        threatService.resetExperimentMetrics();
        return ResponseEntity.ok(Map.of("status", "RESET_SUCCESSFUL", "message", "Experiment evaluation metrics reset."));
    }

    private UUID extractUserId(Authentication authentication) {
        if (authentication != null && authentication.isAuthenticated() && !"anonymousUser".equals(authentication.getName())) {
            try {
                return UUID.fromString(authentication.getName());
            } catch (IllegalArgumentException ignored) {}
        }
        return null;
    }
}

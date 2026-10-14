package com.framework.threat.service;

import com.framework.threat.dto.*;

import java.util.List;
import java.util.Map;
import java.util.UUID;

public interface ThreatDetectionService {

    SecurityEventResponse ingestEvent(SecurityEventRequest request, UUID userId, String clientIp);

    CorrelationResultResponse ingestCommonEvent(CommonSecurityEventRequest request, UUID userId, String clientIp);

    DeviceRiskResponse getDeviceRisk(String deviceId);

    ThreatSummaryResponse getThreatSummary();

    List<SecurityEventResponse> getRecentEvents(int limit);

    List<CorrelationResultResponse> getRecentCorrelations(int limit);

    CorrelationResultResponse getCorrelationById(String correlationId);

    ExperimentConfigDto getActiveExperimentConfig();

    void setActiveExperimentConfig(String configMode, String updatedBy);

    ResearchMetricsResponse getExperimentMetrics();

    void resetExperimentMetrics();

    Map<String, String> getPolicyConfigurations();

    void updatePolicyConfigurations(Map<String, String> configs, String updatedBy);
}

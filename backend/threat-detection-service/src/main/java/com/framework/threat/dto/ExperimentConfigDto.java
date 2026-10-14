package com.framework.threat.dto;

public record ExperimentConfigDto(
        String activeConfiguration, // CONFIG_A_API_ONLY, CONFIG_B_MOBILE_ONLY, CONFIG_C_INDEPENDENT, CONFIG_D_FULL_APPSHIELDX
        String description,
        boolean correlationEnabled,
        boolean adaptiveEnforcementEnabled,
        boolean mobileTelemetryIngested
) {}

package com.framework.threat.dto;

import java.util.Map;

public record PolicyConfigurationDto(
        Map<String, String> configurations,
        String updatedBy
) {}

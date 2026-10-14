package com.framework.threat.service;

import com.framework.threat.dto.ExperimentConfigDto;
import com.framework.threat.entity.PolicyConfigurationEntity;
import com.framework.threat.repository.PolicyConfigurationRepository;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.*;
import java.util.concurrent.ConcurrentHashMap;

@Service
public class PolicyConfigurationService {

    private static final Logger log = LoggerFactory.getLogger(PolicyConfigurationService.class);

    private final PolicyConfigurationRepository repository;
    private final Map<String, String> cache = new ConcurrentHashMap<>();

    public PolicyConfigurationService(PolicyConfigurationRepository repository) {
        this.repository = repository;
    }

    @PostConstruct
    public void init() {
        loadConfigurations();
    }

    public synchronized void loadConfigurations() {
        try {
            List<PolicyConfigurationEntity> entities = repository.findAll();
            for (PolicyConfigurationEntity entity : entities) {
                cache.put(entity.getConfigKey(), entity.getConfigValue());
            }
        } catch (Exception e) {
            log.warn("Could not load configurations from database (might be using default H2 schema): {}", e.getMessage());
        }

        // Populate defaults if missing
        setIfAbsent("risk.weights.root_jailbreak", "40");
        setIfAbsent("risk.weights.frida_hook", "50");
        setIfAbsent("risk.weights.debugger", "30");
        setIfAbsent("risk.weights.signature_tamper", "35");
        setIfAbsent("risk.weights.emulator", "15");
        setIfAbsent("risk.weights.auth_failure", "15");
        setIfAbsent("risk.weights.authz_denial", "20");
        setIfAbsent("risk.weights.rate_limit_burst", "20");
        setIfAbsent("risk.weights.cross_layer_bonus", "25");
        setIfAbsent("risk.bands.allow_max", "24");
        setIfAbsent("risk.bands.monitor_max", "49");
        setIfAbsent("risk.bands.step_up_max", "74");
        setIfAbsent("risk.bands.restrict_max", "100");
        setIfAbsent("correlation.sliding_window_seconds", "300");
        setIfAbsent("correlation.dedup_ttl_seconds", "600");
        setIfAbsent("experiment.active_configuration", "CONFIG_D_FULL_APPSHIELDX");
    }

    private void setIfAbsent(String key, String value) {
        cache.putIfAbsent(key, value);
    }

    public int getInt(String key, int defaultValue) {
        String val = cache.get(key);
        if (val == null) return defaultValue;
        try {
            return Integer.parseInt(val.trim());
        } catch (NumberFormatException e) {
            return defaultValue;
        }
    }

    public String getString(String key, String defaultValue) {
        return cache.getOrDefault(key, defaultValue);
    }

    public Map<String, String> getAllConfigurations() {
        return Collections.unmodifiableMap(new HashMap<>(cache));
    }

    @Transactional
    public void updateConfigurations(Map<String, String> updates, String updatedBy) {
        for (Map.Entry<String, String> entry : updates.entrySet()) {
            cache.put(entry.getKey(), entry.getValue());
            try {
                PolicyConfigurationEntity entity = repository.findByConfigKey(entry.getKey())
                        .orElseGet(() -> new PolicyConfigurationEntity(entry.getKey(), entry.getValue(), "Updated via Admin API", updatedBy));
                entity.setConfigValue(entry.getValue());
                entity.setUpdatedBy(updatedBy != null ? updatedBy : "ADMIN");
                entity.setUpdatedAt(java.time.Instant.now());
                repository.save(entity);
            } catch (Exception e) {
                log.warn("Failed to persist config key {} to DB: {}", entry.getKey(), e.getMessage());
            }
        }
        log.info("POLICY_CONFIG_UPDATED: {} keys modified by {}", updates.size(), updatedBy);
    }

    public ExperimentConfigDto getActiveExperimentConfig() {
        String active = getString("experiment.active_configuration", "CONFIG_D_FULL_APPSHIELDX");
        boolean correlationEnabled = "CONFIG_D_FULL_APPSHIELDX".equals(active);
        boolean adaptiveEnforcement = "CONFIG_D_FULL_APPSHIELDX".equals(active) || "CONFIG_C_INDEPENDENT".equals(active);
        boolean mobileTelemetry = !"CONFIG_A_API_ONLY".equals(active);

        String description = switch (active) {
            case "CONFIG_A_API_ONLY" -> "Baseline API Security: JWT validation, basic rate-limiting, and independent API error logging. Mobile correlation and adaptive risk engine DISABLED.";
            case "CONFIG_B_MOBILE_ONLY" -> "Mobile Telemetry Only: Client RASP detection and telemetry reporting. Backend correlation and adaptive risk enforcement DISABLED.";
            case "CONFIG_C_INDEPENDENT" -> "Combined Independent Security: Mobile RASP and API protections operate independently without cross-layer threat correlation.";
            case "CONFIG_D_FULL_APPSHIELDX" -> "Full AppShieldX Framework: Cross-layer threat correlation, server-side risk scoring, and adaptive policy enforcement active.";
            default -> "Custom / Unspecified Configuration";
        };

        return new ExperimentConfigDto(active, description, correlationEnabled, adaptiveEnforcement, mobileTelemetry);
    }

    @Transactional
    public void setActiveExperimentConfig(String configMode, String updatedBy) {
        String normalized = configMode.trim().toUpperCase();
        if (!List.of("CONFIG_A_API_ONLY", "CONFIG_B_MOBILE_ONLY", "CONFIG_C_INDEPENDENT", "CONFIG_D_FULL_APPSHIELDX").contains(normalized)) {
            throw new IllegalArgumentException("Invalid experimental configuration mode: " + configMode);
        }
        updateConfigurations(Map.of("experiment.active_configuration", normalized), updatedBy);
    }
}

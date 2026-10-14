package com.framework.threat.entity;

import jakarta.persistence.*;
import java.time.Instant;

@Entity
@Table(name = "policy_configurations")
public class PolicyConfigurationEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "config_key", nullable = false, unique = true, length = 80)
    private String configKey;

    @Column(name = "config_value", nullable = false, length = 255)
    private String configValue;

    @Column(name = "description", length = 255)
    private String description;

    @Column(name = "updated_by", length = 80)
    private String updatedBy = "SYSTEM";

    @Column(name = "updated_at", nullable = false)
    private Instant updatedAt = Instant.now();

    public PolicyConfigurationEntity() {}

    public PolicyConfigurationEntity(String configKey, String configValue, String description, String updatedBy) {
        this.configKey = configKey;
        this.configValue = configValue;
        this.description = description;
        this.updatedBy = updatedBy;
        this.updatedAt = Instant.now();
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getConfigKey() {
        return configKey;
    }

    public void setConfigKey(String configKey) {
        this.configKey = configKey;
    }

    public String getConfigValue() {
        return configValue;
    }

    public void setConfigValue(String configValue) {
        this.configValue = configValue;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getUpdatedBy() {
        return updatedBy;
    }

    public void setUpdatedBy(String updatedBy) {
        this.updatedBy = updatedBy;
    }

    public Instant getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(Instant updatedAt) {
        this.updatedAt = updatedAt;
    }
}

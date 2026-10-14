package com.framework.audit.entity;

import jakarta.persistence.*;
import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "audit_logs")
public class AuditLog {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "correlation_id", nullable = false, length = 100)
    private String correlationId;

    @Column(name = "service_name", nullable = false, length = 60)
    private String serviceName;

    @Column(nullable = false, length = 60)
    private String action; // AUTH_LOGIN, TOKEN_REFRESH, USER_PROFILE_UPDATE, RECORD_MUTATION, THREAT_BLOCKED

    @Column(name = "actor_id", length = 100)
    private String actorId;

    @Column(name = "actor_role", length = 50)
    private String actorRole;

    @Column(name = "client_ip", length = 45)
    private String clientIp;

    @Column(nullable = false, length = 20)
    private String status; // SUCCESS, FAILURE, BLOCKED

    @Column(columnDefinition = "TEXT")
    private String details;

    @Column(nullable = false, updatable = false)
    private Instant timestamp = Instant.now();

    public AuditLog() {}

    public AuditLog(
            String correlationId,
            String serviceName,
            String action,
            String actorId,
            String actorRole,
            String clientIp,
            String status,
            String details,
            Instant timestamp
    ) {
        this.correlationId = correlationId != null ? correlationId : UUID.randomUUID().toString();
        this.serviceName = serviceName;
        this.action = action;
        this.actorId = actorId;
        this.actorRole = actorRole;
        this.clientIp = clientIp;
        this.status = status;
        this.details = details;
        this.timestamp = timestamp != null ? timestamp : Instant.now();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public String getCorrelationId() {
        return correlationId;
    }

    public void setCorrelationId(String correlationId) {
        this.correlationId = correlationId;
    }

    public String getServiceName() {
        return serviceName;
    }

    public void setServiceName(String serviceName) {
        this.serviceName = serviceName;
    }

    public String getAction() {
        return action;
    }

    public void setAction(String action) {
        this.action = action;
    }

    public String getActorId() {
        return actorId;
    }

    public void setActorId(String actorId) {
        this.actorId = actorId;
    }

    public String getActorRole() {
        return actorRole;
    }

    public void setActorRole(String actorRole) {
        this.actorRole = actorRole;
    }

    public String getClientIp() {
        return clientIp;
    }

    public void setClientIp(String clientIp) {
        this.clientIp = clientIp;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getDetails() {
        return details;
    }

    public void setDetails(String details) {
        this.details = details;
    }

    public Instant getTimestamp() {
        return timestamp;
    }

    public void setTimestamp(Instant timestamp) {
        this.timestamp = timestamp;
    }
}

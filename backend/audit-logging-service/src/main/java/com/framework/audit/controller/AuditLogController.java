package com.framework.audit.controller;

import com.framework.audit.dto.AuditLogResponse;
import com.framework.audit.dto.AuditStatsResponse;
import com.framework.audit.dto.CreateAuditLogRequest;
import com.framework.audit.service.AuditLogService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/audit")
public class AuditLogController {

    private final AuditLogService auditLogService;

    public AuditLogController(AuditLogService auditLogService) {
        this.auditLogService = auditLogService;
    }

    @PostMapping("/logs")
    public ResponseEntity<AuditLogResponse> createAuditLog(@Valid @RequestBody CreateAuditLogRequest request) {
        AuditLogResponse response = auditLogService.recordLog(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(response);
    }

    @GetMapping("/logs")
    public ResponseEntity<List<AuditLogResponse>> getRecentLogs(
            @RequestParam(defaultValue = "50") int limit
    ) {
        return ResponseEntity.ok(auditLogService.getRecentLogs(limit));
    }

    @GetMapping("/logs/correlation/{correlationId}")
    public ResponseEntity<List<AuditLogResponse>> getLogsByCorrelationId(@PathVariable String correlationId) {
        return ResponseEntity.ok(auditLogService.getLogsByCorrelationId(correlationId));
    }

    @GetMapping("/stats")
    public ResponseEntity<AuditStatsResponse> getAuditStats() {
        return ResponseEntity.ok(auditLogService.getAuditStats());
    }
}

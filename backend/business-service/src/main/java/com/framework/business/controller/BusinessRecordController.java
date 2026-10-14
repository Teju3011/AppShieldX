package com.framework.business.controller;

import com.framework.business.dto.*;
import com.framework.business.service.BusinessService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.UUID;

@RestController
@RequestMapping("/api/business/records")
public class BusinessRecordController {

    private final BusinessService businessService;

    public BusinessRecordController(BusinessService businessService) {
        this.businessService = businessService;
    }

    @PostMapping
    public ResponseEntity<BusinessRecordResponse> createRecord(
            Authentication authentication,
            @Valid @RequestBody CreateRecordRequest request,
            @RequestHeader(value = "X-Device-Risk-Score", required = false) String riskHeader
    ) {
        UUID userId = extractUserId(authentication);
        BusinessRecordResponse created = businessService.createRecord(userId, request, riskHeader);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @GetMapping
    public ResponseEntity<List<RecordSummaryResponse>> listRecords(Authentication authentication) {
        UUID userId = extractUserId(authentication);
        boolean isAdmin = checkIsAdmin(authentication);
        return ResponseEntity.ok(businessService.getRecordsForUser(userId, isAdmin));
    }

    @GetMapping("/{id}")
    public ResponseEntity<BusinessRecordResponse> getRecord(
            Authentication authentication,
            @PathVariable UUID id
    ) {
        UUID userId = extractUserId(authentication);
        boolean isAdmin = checkIsAdmin(authentication);
        return ResponseEntity.ok(businessService.getRecordById(id, userId, isAdmin));
    }

    @PutMapping("/{id}")
    public ResponseEntity<BusinessRecordResponse> updateRecord(
            Authentication authentication,
            @PathVariable UUID id,
            @Valid @RequestBody UpdateRecordRequest request
    ) {
        UUID userId = extractUserId(authentication);
        boolean isAdmin = checkIsAdmin(authentication);
        return ResponseEntity.ok(businessService.updateRecord(id, userId, request, isAdmin));
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<MessageResponse> deleteRecord(
            Authentication authentication,
            @PathVariable UUID id,
            @RequestHeader(value = "X-Correlation-ID", defaultValue = "") String correlationId
    ) {
        UUID userId = extractUserId(authentication);
        boolean isAdmin = checkIsAdmin(authentication);
        businessService.deleteRecord(id, userId, isAdmin);
        return ResponseEntity.ok(MessageResponse.of("Business record deleted successfully", correlationId));
    }

    private UUID extractUserId(Authentication authentication) {
        return UUID.fromString(authentication.getName());
    }

    private boolean checkIsAdmin(Authentication authentication) {
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(a -> a.equals("ROLE_ADMIN"));
    }
}

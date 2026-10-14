package com.framework.business.service.impl;

import com.framework.business.dto.BusinessRecordResponse;
import com.framework.business.dto.CreateRecordRequest;
import com.framework.business.dto.RecordSummaryResponse;
import com.framework.business.dto.UpdateRecordRequest;
import com.framework.business.entity.BusinessRecord;
import com.framework.business.repository.BusinessRecordRepository;
import com.framework.business.service.BusinessService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@Service
public class BusinessServiceImpl implements BusinessService {

    private static final Logger log = LoggerFactory.getLogger(BusinessServiceImpl.class);

    private final BusinessRecordRepository recordRepository;

    public BusinessServiceImpl(BusinessRecordRepository recordRepository) {
        this.recordRepository = recordRepository;
    }

    @Override
    @Transactional
    public BusinessRecordResponse createRecord(UUID userId, CreateRecordRequest request, String riskHeader) {
        String riskLevel = "LOW";
        if (riskHeader != null && !riskHeader.isBlank()) {
            try {
                int score = Integer.parseInt(riskHeader.trim());
                if (score >= 70) riskLevel = "HIGH";
                else if (score >= 40) riskLevel = "MEDIUM";
            } catch (NumberFormatException ignored) {}
        }

        BusinessRecord record = new BusinessRecord(
                userId,
                request.title().trim(),
                request.category().trim().toUpperCase(),
                request.sensitiveData(),
                request.amount(),
                riskLevel
        );

        BusinessRecord saved = recordRepository.save(record);
        log.info("Business record created [RecordId: {}, UserId: {}, RiskLevel: {}]", saved.getId(), userId, riskLevel);

        return mapToResponse(saved);
    }

    @Override
    @Transactional(readOnly = true)
    public List<RecordSummaryResponse> getRecordsForUser(UUID userId, boolean isAdmin) {
        List<BusinessRecord> records;
        if (isAdmin) {
            records = recordRepository.findAll();
        } else {
            records = recordRepository.findAllByUserIdOrderByCreatedAtDesc(userId);
        }

        return records.stream()
                .map(this::mapToSummary)
                .toList();
    }

    @Override
    @Transactional(readOnly = true)
    public BusinessRecordResponse getRecordById(UUID recordId, UUID userId, boolean isAdmin) {
        BusinessRecord record = findRecordAndCheckAccess(recordId, userId, isAdmin);
        return mapToResponse(record);
    }

    @Override
    @Transactional
    public BusinessRecordResponse updateRecord(UUID recordId, UUID userId, UpdateRecordRequest request, boolean isAdmin) {
        BusinessRecord record = findRecordAndCheckAccess(recordId, userId, isAdmin);

        record.setTitle(request.title().trim());
        record.setCategory(request.category().trim().toUpperCase());
        record.setSensitiveData(request.sensitiveData());
        record.setAmount(request.amount());
        if (request.status() != null && !request.status().isBlank()) {
            record.setStatus(request.status().trim().toUpperCase());
        }

        BusinessRecord saved = recordRepository.save(record);
        log.info("Business record updated [RecordId: {}, UserId: {}]", saved.getId(), userId);

        return mapToResponse(saved);
    }

    @Override
    @Transactional
    public void deleteRecord(UUID recordId, UUID userId, boolean isAdmin) {
        BusinessRecord record = findRecordAndCheckAccess(recordId, userId, isAdmin);
        recordRepository.delete(record);
        log.info("Business record deleted [RecordId: {}, UserId: {}]", recordId, userId);
    }

    private BusinessRecord findRecordAndCheckAccess(UUID recordId, UUID userId, boolean isAdmin) {
        BusinessRecord record = recordRepository.findById(recordId)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Business record not found"));

        if (!isAdmin && !record.getUserId().equals(userId)) {
            throw new ResponseStatusException(HttpStatus.FORBIDDEN, "Access denied: You do not own this business record");
        }

        return record;
    }

    private BusinessRecordResponse mapToResponse(BusinessRecord record) {
        return new BusinessRecordResponse(
                record.getId(),
                record.getUserId(),
                record.getTitle(),
                record.getCategory(),
                record.getSensitiveData(),
                record.getAmount(),
                record.getStatus(),
                record.getRiskLevel(),
                record.getCreatedAt(),
                record.getUpdatedAt()
        );
    }

    private RecordSummaryResponse mapToSummary(BusinessRecord record) {
        return new RecordSummaryResponse(
                record.getId(),
                record.getTitle(),
                record.getCategory(),
                record.getAmount(),
                record.getStatus(),
                record.getRiskLevel(),
                record.getCreatedAt()
        );
    }
}

package com.framework.business.service;

import com.framework.business.dto.BusinessRecordResponse;
import com.framework.business.dto.CreateRecordRequest;
import com.framework.business.dto.RecordSummaryResponse;
import com.framework.business.dto.UpdateRecordRequest;
import com.framework.business.entity.BusinessRecord;
import com.framework.business.repository.BusinessRecordRepository;
import com.framework.business.service.impl.BusinessServiceImpl;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.web.server.ResponseStatusException;

import java.math.BigDecimal;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("BusinessService Unit Tests")
class BusinessServiceTest {

    @Mock
    private BusinessRecordRepository recordRepository;

    private BusinessServiceImpl businessService;

    private UUID userId;
    private UUID otherUserId;
    private UUID recordId;
    private BusinessRecord sampleRecord;

    @BeforeEach
    void setUp() {
        businessService = new BusinessServiceImpl(recordRepository);

        userId = UUID.randomUUID();
        otherUserId = UUID.randomUUID();
        recordId = UUID.randomUUID();

        sampleRecord = new BusinessRecord(
                userId,
                "Q3 Financial Statement",
                "FINANCIAL",
                "Sensitive corporate ledger hash: 8f9b2a...",
                new BigDecimal("12500.00"),
                "LOW"
        );
        sampleRecord.setId(recordId);
    }

    @Test
    @DisplayName("Should successfully create business record with risk classification")
    void testCreateRecordSuccess() {
        CreateRecordRequest request = new CreateRecordRequest(
                "Health Metric Log",
                "HEALTH",
                "Encrypted health telemetry",
                new BigDecimal("0.00")
        );

        when(recordRepository.save(any(BusinessRecord.class))).thenReturn(sampleRecord);

        BusinessRecordResponse response = businessService.createRecord(userId, request, "15");

        assertNotNull(response);
        verify(recordRepository, times(1)).save(any(BusinessRecord.class));
    }

    @Test
    @DisplayName("Should retrieve records for specific user when not admin")
    void testGetRecordsForUserNonAdmin() {
        when(recordRepository.findAllByUserIdOrderByCreatedAtDesc(userId))
                .thenReturn(List.of(sampleRecord));

        List<RecordSummaryResponse> records = businessService.getRecordsForUser(userId, false);

        assertNotNull(records);
        assertEquals(1, records.size());
        assertEquals("Q3 Financial Statement", records.get(0).title());
        verify(recordRepository, times(1)).findAllByUserIdOrderByCreatedAtDesc(userId);
        verify(recordRepository, never()).findAll();
    }

    @Test
    @DisplayName("Should retrieve all records across organization when admin")
    void testGetRecordsForUserAdmin() {
        when(recordRepository.findAll()).thenReturn(List.of(sampleRecord));

        List<RecordSummaryResponse> records = businessService.getRecordsForUser(userId, true);

        assertNotNull(records);
        assertEquals(1, records.size());
        verify(recordRepository, times(1)).findAll();
    }

    @Test
    @DisplayName("Should reject access to record if user is neither owner nor admin")
    void testGetRecordByIdForbidden() {
        when(recordRepository.findById(recordId)).thenReturn(Optional.of(sampleRecord));

        assertThrows(ResponseStatusException.class, () ->
                businessService.getRecordById(recordId, otherUserId, false)
        );
    }

    @Test
    @DisplayName("Should allow update if user is owner")
    void testUpdateRecordOwner() {
        UpdateRecordRequest request = new UpdateRecordRequest(
                "Updated Statement",
                "FINANCIAL",
                "Updated ledger",
                new BigDecimal("15000.00"),
                "ACTIVE"
        );

        when(recordRepository.findById(recordId)).thenReturn(Optional.of(sampleRecord));
        when(recordRepository.save(any(BusinessRecord.class))).thenReturn(sampleRecord);

        BusinessRecordResponse response = businessService.updateRecord(recordId, userId, request, false);

        assertNotNull(response);
        verify(recordRepository, times(1)).save(sampleRecord);
    }

    @Test
    @DisplayName("Should delete record if user is owner or admin")
    void testDeleteRecord() {
        when(recordRepository.findById(recordId)).thenReturn(Optional.of(sampleRecord));

        assertDoesNotThrow(() -> businessService.deleteRecord(recordId, userId, false));
        verify(recordRepository, times(1)).delete(sampleRecord);
    }
}

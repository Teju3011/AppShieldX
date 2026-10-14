package com.framework.business.service;

import com.framework.business.dto.BusinessRecordResponse;
import com.framework.business.dto.CreateRecordRequest;
import com.framework.business.dto.RecordSummaryResponse;
import com.framework.business.dto.UpdateRecordRequest;

import java.util.List;
import java.util.UUID;

public interface BusinessService {

    BusinessRecordResponse createRecord(UUID userId, CreateRecordRequest request, String riskHeader);

    List<RecordSummaryResponse> getRecordsForUser(UUID userId, boolean isAdmin);

    BusinessRecordResponse getRecordById(UUID recordId, UUID userId, boolean isAdmin);

    BusinessRecordResponse updateRecord(UUID recordId, UUID userId, UpdateRecordRequest request, boolean isAdmin);

    void deleteRecord(UUID recordId, UUID userId, boolean isAdmin);
}

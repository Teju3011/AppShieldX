package com.framework.business.repository;

import com.framework.business.entity.BusinessRecord;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface BusinessRecordRepository extends JpaRepository<BusinessRecord, UUID> {
    List<BusinessRecord> findAllByUserIdOrderByCreatedAtDesc(UUID userId);
    Optional<BusinessRecord> findByIdAndUserId(UUID id, UUID userId);
    long countByUserId(UUID userId);
}

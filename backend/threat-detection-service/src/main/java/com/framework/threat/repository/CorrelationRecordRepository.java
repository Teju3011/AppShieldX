package com.framework.threat.repository;

import com.framework.threat.entity.CorrelationRecordEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface CorrelationRecordRepository extends JpaRepository<CorrelationRecordEntity, UUID> {

    Optional<CorrelationRecordEntity> findByCorrelationId(String correlationId);

    List<CorrelationRecordEntity> findTop50ByOrderByTimestampDesc();

    List<CorrelationRecordEntity> findBySessionReferenceOrderByTimestampDesc(String sessionReference);

    List<CorrelationRecordEntity> findByDeviceReferenceOrderByTimestampDesc(String deviceReference);

    List<CorrelationRecordEntity> findByCorrelationRuleIdOrderByTimestampDesc(String correlationRuleId);

    long countByFinalEnforcedAction(String finalEnforcedAction);

    @Query("SELECT r.correlationRuleId, COUNT(r) FROM CorrelationRecordEntity r GROUP BY r.correlationRuleId")
    List<Object[]> countGroupedByRuleId();
}

package com.framework.audit.repository;

import com.framework.audit.entity.AuditLog;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLog, UUID> {

    List<AuditLog> findByCorrelationIdOrderByTimestampAsc(String correlationId);

    List<AuditLog> findTop100ByOrderByTimestampDesc();

    List<AuditLog> findByServiceNameOrderByTimestampDesc(String serviceName);

    long countByAction(String action);

    long countByStatus(String status);

    @Query("SELECT a.action, COUNT(a) FROM AuditLog a GROUP BY a.action")
    List<Object[]> countGroupedByAction();
}

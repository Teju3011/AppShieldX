package com.framework.threat.repository;

import com.framework.threat.entity.SecurityEventEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.time.Instant;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@Repository
public interface SecurityEventRepository extends JpaRepository<SecurityEventEntity, UUID> {

    List<SecurityEventEntity> findTop50ByOrderByTimestampDesc();

    List<SecurityEventEntity> findByDeviceIdOrderByTimestampDesc(String deviceId);

    List<SecurityEventEntity> findBySeverityOrderByTimestampDesc(String severity);

    long countBySeverity(String severity);

    @Query("SELECT e.threatCategory, COUNT(e) FROM SecurityEventEntity e GROUP BY e.threatCategory")
    List<Object[]> countGroupedByThreatCategory();

    // Cross-Layer Correlation Queries
    List<SecurityEventEntity> findByVerifiedSessionRefAndTimestampAfterOrderByTimestampDesc(
            String verifiedSessionRef, Instant after);

    List<SecurityEventEntity> findByDeviceIdAndTimestampAfterOrderByTimestampDesc(
            String deviceId, Instant after);

    List<SecurityEventEntity> findByAuthUserRefAndTimestampAfterOrderByTimestampDesc(
            String authUserRef, Instant after);

    Optional<SecurityEventEntity> findFirstByEventHashAndTimestampAfter(String eventHash, Instant after);

    @Query("SELECT e FROM SecurityEventEntity e WHERE (e.deviceId = :deviceId OR e.verifiedSessionRef = :sessionRef OR e.authUserRef = :userRef) AND e.timestamp >= :since ORDER BY e.timestamp ASC")
    List<SecurityEventEntity> findCorrelatableEvents(
            @Param("deviceId") String deviceId,
            @Param("sessionRef") String sessionRef,
            @Param("userRef") String userRef,
            @Param("since") Instant since);
}

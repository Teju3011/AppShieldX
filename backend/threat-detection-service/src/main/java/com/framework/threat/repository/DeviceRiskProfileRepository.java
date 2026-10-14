package com.framework.threat.repository;

import com.framework.threat.entity.DeviceRiskProfile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface DeviceRiskProfileRepository extends JpaRepository<DeviceRiskProfile, String> {

    List<DeviceRiskProfile> findByRiskLevel(String riskLevel);

    long countByRiskLevel(String riskLevel);

    long countByRiskScoreGreaterThanEqual(int minScore);
}

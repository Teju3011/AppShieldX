package com.framework.threat.repository;

import com.framework.threat.entity.PolicyConfigurationEntity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface PolicyConfigurationRepository extends JpaRepository<PolicyConfigurationEntity, Long> {

    Optional<PolicyConfigurationEntity> findByConfigKey(String configKey);
}

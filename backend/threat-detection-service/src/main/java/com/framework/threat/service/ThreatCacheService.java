package com.framework.threat.service;

import java.time.Duration;

public interface ThreatCacheService {

    long incrementDeviceVelocity(String deviceId, Duration window);

    long getDeviceVelocity(String deviceId);

    void cacheRiskScore(String deviceId, int score, Duration ttl);

    Integer getCachedRiskScore(String deviceId);
}

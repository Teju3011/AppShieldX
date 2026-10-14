package com.framework.threat.service.impl;

import com.framework.threat.service.ThreatCacheService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;

@Service
public class RedisThreatCacheServiceImpl implements ThreatCacheService {

    private static final Logger log = LoggerFactory.getLogger(RedisThreatCacheServiceImpl.class);

    private final StringRedisTemplate redisTemplate;

    public RedisThreatCacheServiceImpl(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @Override
    public long incrementDeviceVelocity(String deviceId, Duration window) {
        try {
            String key = "threat_velocity:" + deviceId;
            Long count = redisTemplate.opsForValue().increment(key);
            if (count != null && count == 1) {
                redisTemplate.expire(key, window);
            }
            return count != null ? count : 0L;
        } catch (Exception e) {
            log.debug("Redis increment velocity error: {}", e.getMessage());
            return 0L;
        }
    }

    @Override
    public long getDeviceVelocity(String deviceId) {
        try {
            String key = "threat_velocity:" + deviceId;
            String val = redisTemplate.opsForValue().get(key);
            return val != null ? Long.parseLong(val) : 0L;
        } catch (Exception e) {
            log.debug("Redis get velocity error: {}", e.getMessage());
            return 0L;
        }
    }

    @Override
    public void cacheRiskScore(String deviceId, int score, Duration ttl) {
        try {
            String key = "device_risk_score:" + deviceId;
            redisTemplate.opsForValue().set(key, String.valueOf(score), ttl);
        } catch (Exception e) {
            log.debug("Redis set risk score error: {}", e.getMessage());
        }
    }

    @Override
    public Integer getCachedRiskScore(String deviceId) {
        try {
            String key = "device_risk_score:" + deviceId;
            String val = redisTemplate.opsForValue().get(key);
            return val != null ? Integer.parseInt(val) : null;
        } catch (Exception e) {
            log.debug("Redis get cached risk score error: {}", e.getMessage());
            return null;
        }
    }
}

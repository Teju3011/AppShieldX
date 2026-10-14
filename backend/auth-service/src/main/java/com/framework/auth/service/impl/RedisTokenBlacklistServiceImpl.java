package com.framework.auth.service.impl;

import com.framework.auth.service.TokenBlacklistService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.stereotype.Service;

import java.time.Duration;

@Service
public class RedisTokenBlacklistServiceImpl implements TokenBlacklistService {

    private static final Logger log = LoggerFactory.getLogger(RedisTokenBlacklistServiceImpl.class);

    private final StringRedisTemplate redisTemplate;

    public RedisTokenBlacklistServiceImpl(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
    }

    @Override
    public void blacklistToken(String token, Duration ttl) {
        try {
            redisTemplate.opsForValue().set("token_blacklist:" + token, "revoked", ttl);
            log.info("Token successfully blacklisted in Redis cache");
        } catch (Exception e) {
            log.error("Failed adding token to Redis blacklist: {}", e.getMessage());
        }
    }

    @Override
    public boolean isBlacklisted(String token) {
        try {
            return Boolean.TRUE.equals(redisTemplate.hasKey("token_blacklist:" + token));
        } catch (Exception e) {
            log.error("Error querying Redis blacklist: {}", e.getMessage());
            return false;
        }
    }

    @Override
    public void recordFailedAttempt(String ipAddress) {
        try {
            String counterKey = "auth_fail_counter:" + ipAddress;
            redisTemplate.opsForValue().increment(counterKey);
            redisTemplate.expire(counterKey, Duration.ofMinutes(15));
        } catch (Exception e) {
            log.debug("Redis rate counter increment skipped: {}", e.getMessage());
        }
    }
}

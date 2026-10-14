package com.framework.auth.service;

import java.time.Duration;

/**
 * Abstraction for token revocation lists and brute-force authentication telemetry.
 */
public interface TokenBlacklistService {

    /**
     * Commits a revoked token to the persistent blacklist with a specified TTL.
     */
    void blacklistToken(String token, Duration ttl);

    /**
     * Checks if a token is marked as revoked.
     */
    boolean isBlacklisted(String token);

    /**
     * Records a failed authentication attempt against an IP address.
     */
    void recordFailedAttempt(String ipAddress);
}

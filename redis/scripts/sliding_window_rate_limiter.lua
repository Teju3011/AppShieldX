-- =============================================================================
-- Redis Lua Script: High-Precision Sliding Window Rate Limiter
-- KEYS[1]: Rate limit key (e.g., "ratelimit:ip:192.168.1.100")
-- ARGV[1]: Current epoch timestamp in milliseconds
-- ARGV[2]: Window size in milliseconds (e.g., 60000 for 1 minute)
-- ARGV[3]: Maximum allowed requests within the window (e.g., 100)
-- =============================================================================

local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])

local clearBefore = now - window

-- 1. Evict elements outside the current sliding window
redis.call('ZREMRANGEBYSCORE', key, '-inf', clearBefore)

-- 2. Count surviving requests inside the active window
local currentRequests = redis.call('ZCARD', key)

-- 3. Check threshold
if currentRequests < limit then
    -- Record this request with timestamp as both score and unique member
    redis.call('ZADD', key, now, now .. '-' .. currentRequests)
    -- Set TTL on key to auto-cleanup inactive windows
    redis.call('PEXPIRE', key, window)
    return {1, limit - currentRequests - 1} -- Allowed, Remaining
else
    return {0, 0} -- Blocked, 0 remaining
end

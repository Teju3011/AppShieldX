-- =============================================================================
-- Redis Lua Script: Token Blacklist Verification
-- KEYS[1]: Token blacklist key (e.g., "token_blacklist:<token>")
-- =============================================================================

local key = KEYS[1]
local exists = redis.call('EXISTS', key)

if exists == 1 then
    return 1 -- Revoked / Blacklisted
else
    return 0 -- Active / Valid
end

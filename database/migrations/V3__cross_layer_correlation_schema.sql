-- =============================================================================
-- Migration V3: Cross-Layer Threat Correlation and Risk-Adaptive Policy Schema
-- =============================================================================

-- Add Common Security Event Schema fields to security_events table
ALTER TABLE security_events
    ADD COLUMN IF NOT EXISTS event_id VARCHAR(100),
    ADD COLUMN IF NOT EXISTS event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS received_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ADD COLUMN IF NOT EXISTS platform VARCHAR(30) DEFAULT 'UNKNOWN',
    ADD COLUMN IF NOT EXISTS app_version VARCHAR(20) DEFAULT '1.0.0',
    ADD COLUMN IF NOT EXISTS confidence DOUBLE PRECISION DEFAULT 1.0,
    ADD COLUMN IF NOT EXISTS auth_user_ref VARCHAR(100),
    ADD COLUMN IF NOT EXISTS verified_session_ref VARCHAR(100),
    ADD COLUMN IF NOT EXISTS registered_device_ref VARCHAR(100),
    ADD COLUMN IF NOT EXISTS correlation_id VARCHAR(100),
    ADD COLUMN IF NOT EXISTS endpoint_category VARCHAR(60) DEFAULT 'MOBILE_RASP',
    ADD COLUMN IF NOT EXISTS detection_reason VARCHAR(255),
    ADD COLUMN IF NOT EXISTS evidence_source VARCHAR(60) DEFAULT 'CLIENT_TELEMETRY',
    ADD COLUMN IF NOT EXISTS verification_status VARCHAR(40) DEFAULT 'UNVERIFIED_CLIENT',
    ADD COLUMN IF NOT EXISTS event_expiry TIMESTAMP WITH TIME ZONE,
    ADD COLUMN IF NOT EXISTS event_hash VARCHAR(64);

-- Populate existing rows with default values where null
UPDATE security_events
SET event_id = id::text,
    event_timestamp = timestamp,
    received_timestamp = timestamp,
    registered_device_ref = device_id,
    auth_user_ref = user_id::text
WHERE event_id IS NULL;

-- Correlation Records Table: Stores evaluated cross-layer correlation results
CREATE TABLE IF NOT EXISTS correlation_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    correlation_id VARCHAR(100) NOT NULL UNIQUE,
    correlation_rule_id VARCHAR(60) NOT NULL,
    matched_conditions TEXT NOT NULL,
    related_event_ids TEXT NOT NULL,
    time_window_seconds INT NOT NULL DEFAULT 300,
    risk_score_before INT NOT NULL DEFAULT 0,
    risk_score_after INT NOT NULL DEFAULT 0,
    risk_contribution INT NOT NULL DEFAULT 0,
    confidence VARCHAR(20) NOT NULL DEFAULT 'HIGH',
    explanation TEXT NOT NULL,
    recommended_policy_action VARCHAR(40) NOT NULL,
    final_enforced_action VARCHAR(40) NOT NULL,
    user_reference VARCHAR(100),
    session_reference VARCHAR(100),
    device_reference VARCHAR(100),
    platform VARCHAR(30) DEFAULT 'MULTI_LAYER',
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Policy Configurations Table: Restricted server-side risk weights & thresholds
CREATE TABLE IF NOT EXISTS policy_configurations (
    id BIGSERIAL PRIMARY KEY,
    config_key VARCHAR(80) NOT NULL UNIQUE,
    config_value VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    updated_by VARCHAR(80) DEFAULT 'SYSTEM',
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Seed initial policy configuration parameters
INSERT INTO policy_configurations (config_key, config_value, description)
VALUES 
    ('risk.weights.root_jailbreak', '40', 'Weight for confirmed root or jailbreak indicator'),
    ('risk.weights.frida_hook', '50', 'Weight for runtime dynamic hooking tool injection'),
    ('risk.weights.debugger', '30', 'Weight for attached debugger detected'),
    ('risk.weights.signature_tamper', '35', 'Weight for package certificate tampering'),
    ('risk.weights.emulator', '15', 'Weight for virtual device execution environment'),
    ('risk.weights.auth_failure', '15', 'Weight for verified authentication failure'),
    ('risk.weights.authz_denial', '20', 'Weight for repeated authorization denial'),
    ('risk.weights.rate_limit_burst', '20', 'Weight for confirmed API rate limit violation'),
    ('risk.weights.cross_layer_bonus', '25', 'Bounded additional risk bonus for cross-layer correlation'),
    ('risk.bands.allow_max', '24', 'Upper bound for ALLOW response band'),
    ('risk.bands.monitor_max', '49', 'Upper bound for MONITOR response band'),
    ('risk.bands.step_up_max', '74', 'Upper bound for STEP_UP_AUTHENTICATION response band'),
    ('risk.bands.restrict_max', '100', 'Upper bound for RESTRICT_SENSITIVE_ACTIONS response band'),
    ('correlation.sliding_window_seconds', '300', 'Sliding correlation time window in seconds (5 min)'),
    ('correlation.dedup_ttl_seconds', '600', 'Event deduplication hash window in seconds (10 min)'),
    ('experiment.active_configuration', 'CONFIG_D_FULL_APPSHIELDX', 'Active experimental evaluation mode')
ON CONFLICT (config_key) DO NOTHING;

-- Indexes for Correlation Query Optimization
CREATE INDEX IF NOT EXISTS idx_security_events_event_id ON security_events(event_id);
CREATE INDEX IF NOT EXISTS idx_security_events_session ON security_events(verified_session_ref);
CREATE INDEX IF NOT EXISTS idx_security_events_user ON security_events(auth_user_ref);
CREATE INDEX IF NOT EXISTS idx_security_events_hash ON security_events(event_hash);
CREATE INDEX IF NOT EXISTS idx_correlation_records_corr_id ON correlation_records(correlation_id);
CREATE INDEX IF NOT EXISTS idx_correlation_records_time ON correlation_records(timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_correlation_records_rule ON correlation_records(correlation_rule_id);

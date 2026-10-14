-- =============================================================================
-- Migration V2: Seed Roles, Demo Users, Baseline Telemetry & Audit Logs
-- =============================================================================

-- 1. Roles
INSERT INTO roles (name, description) VALUES
    ('ROLE_USER', 'Standard mobile application user'),
    ('ROLE_ADMIN', 'Enterprise security operations administrator')
ON CONFLICT (name) DO NOTHING;

-- 2. Initial Admin User (Username: admin, Password: AdminP@ssw0rd2026!)
INSERT INTO users (id, username, email, password_hash, enabled, account_locked)
VALUES (
    'a0000000-0000-0000-0000-000000000001',
    'admin',
    'admin@enterprise.internal',
    crypt('AdminP@ssw0rd2026!', gen_salt('bf', 12)),
    TRUE,
    FALSE
)
ON CONFLICT (username) DO NOTHING;

-- Assign ROLE_ADMIN and ROLE_USER to admin
INSERT INTO user_roles (user_id, role_id)
SELECT 'a0000000-0000-0000-0000-000000000001', id FROM roles WHERE name IN ('ROLE_ADMIN', 'ROLE_USER')
ON CONFLICT DO NOTHING;

-- 3. Demo Standard User (Username: alice, Password: AliceP@ssw0rd2026!)
INSERT INTO users (id, username, email, password_hash, enabled, account_locked)
VALUES (
    'a0000000-0000-0000-0000-000000000002',
    'alice',
    'alice@enterprise.internal',
    crypt('AliceP@ssw0rd2026!', gen_salt('bf', 12)),
    TRUE,
    FALSE
)
ON CONFLICT (username) DO NOTHING;

-- Assign ROLE_USER to alice
INSERT INTO user_roles (user_id, role_id)
SELECT 'a0000000-0000-0000-0000-000000000002', id FROM roles WHERE name = 'ROLE_USER'
ON CONFLICT DO NOTHING;

-- 4. Initial Protected Business Records for Alice
INSERT INTO business_records (id, user_id, title, category, sensitive_data, amount, status, risk_level)
VALUES
    (
        'b0000000-0000-0000-0000-000000000001',
        'a0000000-0000-0000-0000-000000000002',
        'Quarterly Payroll Ledger',
        'FINANCIAL',
        'Encrypted Salary Hash: AES256-GCM:89f4b3917a...',
        84500.00,
        'ACTIVE',
        'LOW'
    ),
    (
        'b0000000-0000-0000-0000-000000000002',
        'a0000000-0000-0000-0000-000000000002',
        'Executive Medical Records',
        'HEALTH',
        'HIPAA Compliant Health Telemetry: Patient #9182',
        0.00,
        'ACTIVE',
        'LOW'
    )
ON CONFLICT DO NOTHING;

-- 5. Baseline Device Risk Profile
INSERT INTO device_risk_profiles (device_id, risk_score, risk_level, active_threats, total_events_recorded)
VALUES
    ('android-pixel-simulator-001', 15, 'LOW', 'VIRTUAL_DEVICE', 1),
    ('compromised-rooted-device-999', 90, 'CRITICAL', 'ROOT_OR_JAILBREAK,FRIDA_HOOK_INJECTION', 4)
ON CONFLICT DO NOTHING;

-- 6. Initial Audit Log Entry
INSERT INTO audit_logs (correlation_id, service_name, action, actor_id, actor_role, client_ip, status, details)
VALUES
    ('init-baseline-correlation-0001', 'database', 'SCHEMA_INITIALIZED', 'system', 'ROLE_SYSTEM', '127.0.0.1', 'SUCCESS', 'Flyway migrations V1 & V2 successfully committed');

# AppShieldX - REST API Specification & Endpoint Catalog

## 1. Gateway Routing Architecture

All client and administrative traffic enters through the **Spring Cloud API Gateway** on port `8080`.
The gateway performs TLS termination, JWT cryptographic validation, Redis sliding-window rate limiting, and response header hardening.

The complete machine-readable OpenAPI 3.0 specification is available at:
`docs/openapi.yaml`

---

## 2. API Endpoints by Service

### Authentication (`/api/v1/auth` & `/api/auth`)
- `POST /api/v1/auth/register`: Public registration of new user accounts.
- `POST /api/v1/auth/login`: Public login issuing access token (15m) and refresh token.
- `POST /api/v1/auth/refresh`: Token rotation issuing fresh access JWT.
- `POST /api/v1/auth/logout`: Revocation of refresh token and blacklisting of JWT in Redis.

### Users & Devices (`/api/v1/users` & `/api/v1/devices`)
- `GET /api/v1/users/me`: Authenticated profile retrieval.
- `PATCH /api/v1/users/me`: Authenticated profile updates.
- `POST /api/v1/devices/register`: Device hardware fingerprint and posture binding.
- `GET /api/v1/devices/me`: List registered mobile devices for caller.

### Threat Detection & Telemetry (`/api/v1/security`)
- `POST /api/v1/security/events`: Mobile RASP telemetry ingestion (Root, Jailbreak, Frida, Debugger, Tampering).
- `GET /api/v1/security/events/me`: Recent security event logs for user devices.
- `GET /api/v1/security/status`: Current real-time risk posture and policy status.

### Business Resources (`/api/v1/resources` & `/api/business/records`)
- `GET /api/v1/resources`: User-owned business resources. Enforces Zero-Trust filter (HTTP 403 if device risk score $\ge 70$).
- `GET /api/v1/resources/{id}`: Single resource retrieval with Anti-IDOR ownership validation.
- `POST /api/v1/resources`: Create confidential business record.

### Administration (`/api/v1/admin`)
- `GET /api/v1/admin/overview`: System-wide KPI metrics and threat statistics.
- `GET /api/v1/admin/events`: Filterable paginated security events table.
- `GET /api/v1/admin/alerts`: Active threat alerts for SOC triage.
- `PATCH /api/v1/admin/alerts/{id}`: Alert acknowledgement and status transitions.
- `GET /api/v1/admin/audit-logs`: Immutable audit trail with `X-Correlation-ID` tracing.
- `GET /api/v1/admin/threat-rules`: Configurable threat detection rules and severity weights.

---

## 3. Standard Headers & Error Codes

### Injected Security Headers
- `X-Correlation-ID`: Trace UUID injected on every request and response.
- `Strict-Transport-Security`: `max-age=31536000; includeSubDomains`
- `X-Content-Type-Options`: `nosniff`
- `Content-Security-Policy`: Default restrictive policy.

### Common Response Status Codes
- `200 OK`: Request succeeded.
- `201 Created`: Resource successfully registered or created.
- `202 Accepted`: Asynchronous threat telemetry ingested and queued.
- `400 Bad Request`: Validation failure or malformed payload.
- `401 Unauthorized`: Missing, invalid, or expired JWT token.
- `403 Forbidden`: Insufficient role (`ROLE_ADMIN` required) or Zero-Trust device block (Risk $\ge 70$).
- `404 Not Found`: Resource does not exist or access forbidden (Anti-IDOR).
- `429 Too Many Requests`: Sliding-window rate limit threshold exceeded.
